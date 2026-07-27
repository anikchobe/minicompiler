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
    pass

LoopStatement: TypeAlias = Stmt | RepeatStmt
LoopProgram: TypeAlias = list[LoopStatement]


# --------------------------------- Parser ----------------------------------


def parse_program(source: str) -> LoopProgram:
    logical_lines: list[tuple[int, list[str]]] = []
    for line_number, raw_line in enumerate(source.splitlines(), start=1):
        line = strip_comment(raw_line)
        if line:
            logical_lines.append((line_number, line.split()))

    def parse_block(
        index: int, *, opening_repeat_line: int | None
    ) -> tuple[list[LoopStatement], int]:
        pass

# ------------------------------- Interpreter -------------------------------


def execute_program(
    program: LoopProgram,
    initial_environment: dict[str, int] | None = None,
) -> ExecutionResult:


# ---------------------------- Bytecode compiler ----------------------------


class BytecodeCompiler:
    def __init__(self) -> None:
        self.code: Bytecode = []
        self.next_loop_id = 0

    def emit(self, opcode: str, argument: int | str | None = None) -> int:
        pass

    def patch_target(self, address: int, target: int) -> None:
        pass

    def compile_statement(self, statement: LoopStatement) -> None:
        pass

    def compile_program(self, program: LoopProgram) -> Bytecode:
        pass

def compile_program(program: LoopProgram) -> Bytecode:
    return BytecodeCompiler().compile_program(program)


# ------------------------------- Formatting --------------------------------


def format_expression_source(expression: Expr) -> str:
    pass

def format_program_source(
    program: tuple[LoopStatement, ...] | list[LoopStatement], indent: int = 0
) -> str:
    pass

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
