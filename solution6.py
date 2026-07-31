from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from solution4 import MiniCalcSyntaxError
from solution4 import MiniCalcRuntimeError
from solution4 import (
    BinaryExpr,
    ExecutionResult,
    Expr,
    ExprStmt,
    IntegerExpr,
    LetStmt,
    PrintStmt,
    Stmt,
    VariableExpr,
    evaluate_expression,
    execute_statement as execute_flat_statement,
    parse_expression_tokens,
    parse_statement_tokens,
    strip_comment,
)
from solution5 import (
    Bytecode,
    VMResult,
    compile_expression,
    compile_statement as compile_flat_statement,
    disassemble,
    execute_bytecode,
)


@dataclass(frozen=True)
class RepeatStmt:
    count: Expr
    body: tuple[LoopStatement, ...]
    lineNum: int


LoopStatement: TypeAlias = Stmt | RepeatStmt
LoopProgram: TypeAlias = list[LoopStatement]


# --------------------------------- Parser ----------------------------------


def parse_program(source: str) -> LoopProgram:
    logical_lines: list[tuple[int, list[str]]] = []
    for line_number, raw_line in enumerate(source.splitlines(), start=1):
        line = strip_comment(raw_line)
        if line.strip():
            logical_lines.append((line_number, line.split()))

    def parse_block(
        index: int, *, opening_repeat_line: int | None
    ) -> tuple[list[LoopStatement], int]:
        statements: list[LoopStatement] = []

        while index < len(logical_lines):
            line_number, tokens = logical_lines[index]
            first = tokens[0]

            if first == "end":
                if len(tokens) != 1:
                    raise MiniCalcSyntaxError(
                        f"line {line_number}: end does not take arguments"
                    )
                if opening_repeat_line is None:
                    raise MiniCalcSyntaxError(f"line {line_number}: unexpected end")
                return statements, index + 1

            if first == "repeat":
                if len(tokens) == 1:
                    raise MiniCalcSyntaxError(
                        f"line {line_number}: repeat requires a count expression"
                    )
                count = parse_expression_tokens(tokens[1:], line_number)
                body, index = parse_block(
                    index + 1, opening_repeat_line=line_number
                )
                statements.append(RepeatStmt(count, tuple(body), line_number))
                continue

            statements.append(parse_statement_tokens(tokens, line_number))
            index += 1

        if opening_repeat_line is not None:
            raise MiniCalcSyntaxError(
                f"line {opening_repeat_line}: repeat block is missing a matching end"
            )
        return statements, index

    program, final_index = parse_block(0, opening_repeat_line=None)
    assert final_index == len(logical_lines)
    return program


# ------------------------------- Interpreter -------------------------------


def execute_program(
    program: LoopProgram,
    initial_environment: dict[str, int] | None = None,
) -> ExecutionResult:
    environment = dict(initial_environment) if initial_environment is not None else {}
    output: list[int] = []

    def execute_block(statements: tuple[LoopStatement, ...] | list[LoopStatement]) -> None:
        for statement in statements:
            if isinstance(statement, RepeatStmt):
                try:
                    count = evaluate_expression(statement.count, environment)
                except (MiniCalcRuntimeError, ZeroDivisionError) as exc:
                    raise MiniCalcRuntimeError(
                        f"line {statement.lineNum}: {exc}"
                    ) from exc

                # A nonpositive count runs the body zero times.
                for _ in range(max(0, count)):
                    execute_block(statement.body)
            else:
                execute_flat_statement(statement, environment, output)

    execute_block(program)
    return ExecutionResult(environment, output)


# ---------------------------- Bytecode compiler ----------------------------


class BytecodeCompiler:
    def __init__(self) -> None:
        self.code: Bytecode = []
        self.next_loop_id = 0

    def emit(self, opcode: str, argument: int | str | None = None) -> int:
        address = len(self.code)
        self.code.append((opcode, argument))
        return address

    def patch_target(self, address: int, target: int) -> None:
        opcode, old_argument = self.code[address]
        if old_argument is not None:
            raise AssertionError(f"instruction {address} was already patched")
        self.code[address] = (opcode, target)

    def compile_statement(self, statement: LoopStatement) -> None:
        if not isinstance(statement, RepeatStmt):
            compile_flat_statement(statement, self.code)
            return

        loop_id = self.next_loop_id
        self.next_loop_id += 1
        counter_name = f"@loop{loop_id}"

        compile_expression(statement.count, self.code)
        self.emit("STORE", counter_name)

        loop_start = len(self.code)
        self.emit("LOAD", counter_name)
        exit_jump = self.emit("JUMP_IF_NONPOSITIVE", None)

        for body_statement in statement.body:
            self.compile_statement(body_statement)

        self.emit("LOAD", counter_name)
        self.emit("PUSH_CONST", 1)
        self.emit("SUB")
        self.emit("STORE", counter_name)
        self.emit("JUMP", loop_start)

        self.patch_target(exit_jump, len(self.code))

    def compile_program(self, program: LoopProgram) -> Bytecode:
        for statement in program:
            self.compile_statement(statement)
        self.emit("HALT")
        return list(self.code)


def compile_program(program: LoopProgram) -> Bytecode:
    return BytecodeCompiler().compile_program(program)


# ------------------------------- Formatting --------------------------------


def format_expression_source(expression: Expr) -> str:
    if isinstance(expression, IntegerExpr):
        return str(expression.value)
    if isinstance(expression, VariableExpr):
        return expression.name
    if isinstance(expression, BinaryExpr):
        return (
            f"{format_expression_source(expression.left)} "
            f"{expression.operator} "
            f"{format_expression_source(expression.right)}"
        )
    raise TypeError(type(expression).__name__)


def format_program_source(
    program: tuple[LoopStatement, ...] | list[LoopStatement], indent: int = 0
) -> str:
    prefix = "    " * indent
    lines: list[str] = []
    for statement in program:
        if isinstance(statement, LetStmt):
            lines.append(
                f"{prefix}let {statement.name} = "
                f"{format_expression_source(statement.expression)}"
            )
        elif isinstance(statement, PrintStmt):
            lines.append(
                f"{prefix}print {format_expression_source(statement.expression)}"
            )
        elif isinstance(statement, ExprStmt):
            lines.append(f"{prefix}{format_expression_source(statement.expression)}")
        elif isinstance(statement, RepeatStmt):
            lines.append(
                f"{prefix}repeat {format_expression_source(statement.count)}"
            )
            body_text = format_program_source(statement.body, indent + 1)
            if body_text:
                lines.extend(body_text.splitlines())
            lines.append(f"{prefix}end")
        else:
            raise TypeError(type(statement).__name__)
    return "\n".join(lines)


def _self_test() -> None:
    source = """
        let x = 1
        repeat 5
            print x
            let x = x * 2
        end
        print x
    """
    program = parse_program(source)
    direct = execute_program(program)
    code = compile_program(program)
    vm: VMResult = execute_bytecode(code)

    assert direct.output == [1, 2, 4, 8, 16, 32]
    assert vm.output == direct.output
    assert vm.visible_variables == direct.environment

    nested = parse_program("""
        repeat 3
            repeat 2
                print 7
            end
        end
    """)
    assert execute_program(nested).output == [7] * 6
    assert execute_bytecode(compile_program(nested)).output == [7] * 6


if __name__ == "__main__":
    _self_test()
    demo_source = """
    let x = 1
    repeat 5
        print x
        let x = x * 2
    end
    print x
    """
    demo_program = parse_program(demo_source)
    demo_code = compile_program(demo_program)
    print("Normalized source:\n")
    print(format_program_source(demo_program))
    print("\nBytecode:\n")
    print(disassemble(demo_code))
    result = execute_bytecode(demo_code)
    print("\noutput:", result.output)
    print("visible variables:", result.visible_variables)
    print("VM instructions executed:", result.steps)


# Notes:
#
# The count is evaluated once and stored in @loop0.  If it were an expression
# like x * 2, re-evaluating it every iteration would observe a changed x and
# loop the wrong number of times.
#
# The forward jump has no target yet when it is emitted.  compile_statement
# leaves None there, compiles the body, then patches the address.  That is
# backpatching, and it is the main thing loops add to the compiler.
#
# '@loop0' cannot be written by a user because '@' is not an identifier
# character.  visible_variables hides those compiler-private names later.
