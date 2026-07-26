from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from solution4 import (
    BinaryExpr,
    Expr,
    ExprStmt,
    IntegerExpr,
    LetStmt,
    PrintStmt,
    Program,
    Stmt,
    VariableExpr,
    execute_program,
    parse_program,
)

InstructionArgument: TypeAlias = int | str | None
Instruction: TypeAlias = tuple[str, InstructionArgument]
Bytecode: TypeAlias = list[Instruction]

OPCODE_FOR_OPERATOR = {
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "//": "DIV",
    "%": "MOD",
}


class MiniCalcVMError(RuntimeError):
    """Raised when bytecode cannot be executed by the VM."""


@dataclass(frozen=True)
class VMResult:
    variables: dict[str, int]
    output: list[int]
    steps: int

    @property
    def visible_variables(self) -> dict[str, int]:
        """Hide compiler-private names such as loop counters."""
        return {
            name: value
            for name, value in self.variables.items()
            if not name.startswith("@")
        }


# -------------------------------- Compiler ---------------------------------


def compile_expression(expression: Expr, code: Bytecode) -> None:
    if isinstance(expression, IntegerExpr):
        code.append(("PUSH_CONST", expression.value))
        return
    if isinstance(expression, VariableExpr):
        code.append(("LOAD", expression.name))
        return
    if isinstance(expression, BinaryExpr):
        compile_expression(expression.left, code)
        compile_expression(expression.right, code)
        code.append((OPCODE_FOR_OPERATOR[expression.operator], None))
        return
    raise TypeError(f"Unknown Expression: {expression.__name__}")


def compile_statement(statement: Stmt, code: Bytecode) -> None:
    if isinstance(statement, LetStmt):
        compile_expression(statement.expression, code)
        code.append(("STORE", statement.name))
        return
    if isinstance(statement, PrintStmt):
        compile_expression(statement.expression, code)
        code.append(("PRINT", None))
        return
    if isinstance(statement, ExprStmt):
        compile_expression(statement.expression, code)
        code.append(("STORE", 'ans'))
        return
    raise TypeError(f"Unknown Statement: {statement.__name__}")
    

def compile_program(program: Program) -> Bytecode:
    code: Bytecode = []
    for statement in program:
        compile_statement(statement, code)
    code.append(("HALT", None))
    return code
    

# ------------------------------ Disassembler -------------------------------


def disassemble(code: Bytecode) -> str:
    pass

# ------------------------------ Virtual machine ----------------------------


def execute_bytecode(
    code: Bytecode,
    *,
    trace: bool = False,
    max_steps: int = 1_000_000,
) -> VMResult:
    pc = 0
    stack: list[int] = []
    variables: dict[str, int] = {}
    output: list[int] = []
    steps = 0

    def pop_value() -> int:
        if not stack:
            raise MiniCalcVMError(f"PC: {pc} operand stack underflow")
        return stack.pop()
        
    
    def require_int(argument: InstructionArgument, opcode: str) -> int:
        if not isinstance(argument, int):
            raise MiniCalcVMError(f'Pc {pc} {opcode} requires an integer argument')
        return argument
        
    
    def require_name(argument: InstructionArgument, opcode: str) -> str:
        if not isinstance(argument, str):
            raise MiniCalcVMError(f'Pc {pc} {opcode} requires an string argument')
        return argument

    while True:
        opcode, argument = code[pc]

        if opcode == "PUSH_CONST":
            stack.append(require_int(argument, opcode))
            pc += 1
            continue

        if opcode == "LOAD":
            name = require_name(argument, opcode)
            if name not in variables:
                raise MiniCalcVMError(f'pc {pc} underfined varibale {name}')
            stack.append(variables[name])
            pc += 1
            continue

        if opcode == "STORE":
            name = require_name(argument, opcode)
            variables[name] = pop_value()
            pc += 1
            continue

        if opcode in {'ADD', 'SUB', 'MUL', 'DIV', 'MOD'}:
            right = pop_value()
            left = pop_value()
            match opcode:
                case 'ADD':
                    result = left + right
                case 'SUB':
                    result = left - right
                case 'MUL':
                    result = left * right
                case 'DIV':
                    result = left // right
                case 'MOD':
                    result = left % right
            stack.append(result)
            pc += 1
            continue

        if opcode == 'PRINT':
            output.append(pop_value())
            pc += 1
            continue

        if opcode == 'HALT':
            if stack:
                raise MiniCalcVMError(f'pc {pc} HALT reached with non-empty stack {stack}')
            return VMResult(variables, output, steps)
            
        


def _self_test() -> None:
    source = """
        let x = 17 * 3
        print x
        x + 1
        print ans
    """
    program = parse_program(source)
    interpreted = execute_program(program)
    code = compile_program(program)
    vm = execute_bytecode(code)

    assert vm.output == interpreted.output == [51, 52]
    assert vm.visible_variables == interpreted.environment

    # Operand order matters: pop right first, then left.
    subtraction = execute_bytecode(
        [
            ("PUSH_CONST", 10),
            ("PUSH_CONST", 3),
            ("SUB", None),
            ("STORE", "answer"),
            ("HALT", None),
        ]
    )
    assert subtraction.variables["answer"] == 7


if __name__ == "__main__":
    _self_test()
    source = """
    let x = 17 * 3
    print x
    x + 1
    print ans
    """
    program = parse_program(source)
    code = compile_program(program)
    interpreted = execute_program(program)
    vm = execute_bytecode(code)
    assert vm.output == interpreted.output
    assert vm.visible_variables == interpreted.environment

    order_code: Bytecode = [
        ("PUSH_CONST", 10),
        ("PUSH_CONST", 3),
        ("SUB", None),
        ("STORE", "answer"),
        ("HALT", None),
    ]
    assert execute_bytecode(order_code).variables["answer"] == 7

    print(disassemble(code))
    print("output:", vm.output)
    print("variables:", vm.visible_variables)
    print("VM instructions executed:", vm.steps)
