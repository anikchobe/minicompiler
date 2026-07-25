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
    pass


def compile_statement(statement: Stmt, code: Bytecode) -> None:
    pass

def compile_program(program: Program) -> Bytecode:
    pass

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
        pass
    
    def require_int(argument: InstructionArgument, opcode: str) -> int:
        pass
    
    def require_name(argument: InstructionArgument, opcode: str) -> str:
        pass


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
