"""Stage 8 reference: constant folding and conservative constant propagation."""

from __future__ import annotations

from solution4 import apply_operator
from solution4 import (
    BinaryExpr,
    Expr,
    ExprStmt,
    IntegerExpr,
    LetStmt,
    PrintStmt,
    VariableExpr,
    Stmt,
    Program,
)
from solution5 import disassemble, execute_bytecode, compile_program as compile_to_bytecode, execute_program, parse_program

# from stage06_loops import (
#     LoopProgram,
#     LoopStatement,
#     RepeatStmt,
#     compile_program as compile_to_bytecode,
#     execute_program,
#     format_program_source,
#     parse_program,
# )

from solution7 import compile_and_run, compile_to_python


# ---------------------------- Expression rewriting -------------------------


def fold_expression(expression: Expr, constants: dict[str, int]) -> Expr:
    pass

# ------------------------------ Data-flow pass -----------------------------


def assigned_names(statements: list[Stmt]) -> set[str]:
    pass


def optimize_block(
    statements: list[Stmt],
    constants: dict[str, int],
) -> list[Stmt]:
    optimized: list[Stmt] = []

    for statement in statements:
        if isinstance(statement, LetStmt):
            expression = fold_expression(statement.expression, constants)
            optimized.append(
                LetStmt(statement.name, expression, statement.lineNum)
            )
            if isinstance(expression, IntegerExpr):
                constants[statement.name] = expression.value
            else:
                constants.pop(statement.name, None)
            continue

        if isinstance(statement, ExprStmt):
            expression = fold_expression(statement.expression, constants)
            optimized.append(ExprStmt(expression, statement.lineNum))
            if isinstance(expression, IntegerExpr):
                constants["ans"] = expression.value
            else:
                constants.pop("ans", None)
            continue

        if isinstance(statement, PrintStmt):
            optimized.append(
                PrintStmt(
                    fold_expression(statement.expression, constants),
                    statement.lineNum,
                )
            )
            continue

        raise TypeError(type(statement).__name__)

    return optimized


def optimize_program(program: Program) -> Program:
    return optimize_block(program, constants={})


# ---------------------------- Equivalence checks ---------------------------


def backend_outputs(program: Program) -> tuple[list[int], list[int], list[int]]:
    direct = execute_program(program).output
    vm = execute_bytecode(compile_to_bytecode(program)).output
    python_output = compile_and_run(program)
    return direct, vm, python_output


def assert_all_backends_agree(program: Program) -> list[int]:
    direct, vm, python_output = backend_outputs(program)
    assert direct == vm == python_output
    return direct


def _self_test() -> None:
    straight_line = parse_program("""
        let a = 17 * 3
        let b = a + 1
        print b
    """)
    optimized = optimize_program(straight_line)
    # assert optimized.splitlines() == [
    #     "let a = 51",
    #     "let b = 52",
    #     "print 52",
    # ]
    assert assert_all_backends_agree(straight_line) == [52]
    assert assert_all_backends_agree(optimized) == [52]

    mutating_loop = parse_program("""
        let x = 0
        let x = x + 1
        print x
    """)
    optimized_loop = optimize_program(mutating_loop)
    assert assert_all_backends_agree(optimized_loop) == [3]
    # The changing x must not be replaced with its entry value 0 in the body.
    # assert "let x = x + 1" in format_program_source(optimized_loop)


if __name__ == "__main__":
    _self_test()
    source = """
    let a = 17 * 3
    let b = a + 1
    print b
    """
    original = parse_program(source)
    optimized = optimize_program(original)

    original_code = compile_to_bytecode(original)
    optimized_code = compile_to_bytecode(optimized)
    original_vm = execute_bytecode(original_code)
    optimized_vm = execute_bytecode(optimized_code)

    assert assert_all_backends_agree(original) == [52]
    assert assert_all_backends_agree(optimized) == [52]

    print("Original MiniCalc:\n")
    print(original)
    print("\nOptimized MiniCalc:\n")
    print(optimized)

    print("\nOriginal bytecode:\n")
    print(disassemble(original_code))
    print("\nOptimized bytecode:\n")
    print(disassemble(optimized_code))
    print(
        f"\nDynamic VM instructions: {original_vm.steps} -> {optimized_vm.steps}"
    )

    print("\nOriginal generated Python:\n")
    print(compile_to_python(original))
    print("Optimized generated Python:\n")
    print(compile_to_python(optimized))
