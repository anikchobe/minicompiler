"""Stage 8: constant folding and conservative constant propagation."""

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
)
from solution5 import disassemble, execute_bytecode
from solution6 import (
    LoopProgram,
    LoopStatement,
    RepeatStmt,
    compile_program as compile_to_bytecode,
    execute_program,
    format_program_source,
    parse_program,
)
from solution7 import compile_and_run, compile_to_python


# ---------------------------- Expression rewriting -------------------------


def fold_expression(expression: Expr, constants: dict[str, int]) -> Expr:
    # TODO: this is where constant folding and propagation happen.
    if isinstance(expression, IntegerExpr):
        return expression

    if isinstance(expression, VariableExpr):
        if expression.name in constants:
            return IntegerExpr(constants[expression.name])
        return expression

    if not isinstance(expression, BinaryExpr):
        raise TypeError(type(expression).__name__)

    left = fold_expression(expression.left, constants)
    right = fold_expression(expression.right, constants)

    if isinstance(left, IntegerExpr) and isinstance(right, IntegerExpr):
        try:
            return IntegerExpr(
                apply_operator(left.value, expression.operator, right.value)
            )
        except ZeroDivisionError:
            # Leave division by zero for runtime; turning it into a compile-time
            # error here would change when the program fails.
            return BinaryExpr(left, expression.operator, right)

    if expression.operator == "+":
        if isinstance(right, IntegerExpr) and right.value == 0:
            return left
        if isinstance(left, IntegerExpr) and left.value == 0:
            return right

    if expression.operator == "-":
        if isinstance(right, IntegerExpr) and right.value == 0:
            return left

    if expression.operator == "*":
        if isinstance(right, IntegerExpr) and right.value == 1:
            return left
        if isinstance(left, IntegerExpr) and left.value == 1:
            return right

    if expression.operator == "//":
        if isinstance(right, IntegerExpr) and right.value == 1:
            return left

    return BinaryExpr(left, expression.operator, right)


# ------------------------------ Data-flow pass -----------------------------


def assigned_names(
    statements: tuple[LoopStatement, ...] | list[LoopStatement],
) -> set[str]:
    names: set[str] = set()
    for statement in statements:
        if isinstance(statement, LetStmt):
            names.add(statement.name)
        elif isinstance(statement, ExprStmt):
            names.add("ans")
        elif isinstance(statement, RepeatStmt):
            names.update(assigned_names(statement.body))
    return names


def optimize_block(
    statements: tuple[LoopStatement, ...] | list[LoopStatement],
    constants: dict[str, int],
) -> list[LoopStatement]:
    optimized: list[LoopStatement] = []

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

        if isinstance(statement, RepeatStmt):
            count = fold_expression(statement.count, constants)

            # A statically nonpositive loop has no runtime effects.
            if isinstance(count, IntegerExpr) and count.value <= 0:
                continue

            changed_in_loop = assigned_names(statement.body)

            # A value assigned somewhere in the loop cannot be treated as the
            # entry constant on every iteration.  Forget it before the body.
            body_constants = {
                name: value
                for name, value in constants.items()
                if name not in changed_in_loop
            }
            body = optimize_block(statement.body, body_constants)
            optimized.append(
                RepeatStmt(count, tuple(body), statement.lineNum)
            )

            # After a loop that may run zero or many times, changed names are
            # conservatively unknown.
            for name in changed_in_loop:
                constants.pop(name, None)
            continue

        raise TypeError(type(statement).__name__)

    return optimized


def optimize_program(program: LoopProgram) -> LoopProgram:
    return optimize_block(program, constants={})


# ---------------------------- Equivalence checks ---------------------------


def backend_outputs(program: LoopProgram) -> tuple[list[int], list[int], list[int]]:
    direct = execute_program(program).output
    vm = execute_bytecode(compile_to_bytecode(program)).output
    python_output = compile_and_run(program)
    return direct, vm, python_output


def assert_all_backends_agree(program: LoopProgram) -> list[int]:
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
    assert format_program_source(optimized).splitlines() == [
        "let a = 51",
        "let b = 52",
        "print 52",
    ]
    assert assert_all_backends_agree(straight_line) == [52]
    assert assert_all_backends_agree(optimized) == [52]

    mutating_loop = parse_program("""
        let x = 0
        repeat 3
            let x = x + 1
        end
        print x
    """)
    optimized_loop = optimize_program(mutating_loop)
    assert assert_all_backends_agree(optimized_loop) == [3]
    # The changing x must not be replaced with its entry value 0 in the body.
    assert "let x = x + 1" in format_program_source(optimized_loop)

    invariant = parse_program("""
        let scale = 6 * 7
        repeat 2
            print scale
        end
    """)
    optimized_invariant = optimize_program(invariant)
    assert "print 42" in format_program_source(optimized_invariant)
    assert assert_all_backends_agree(optimized_invariant) == [42, 42]


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
    print(format_program_source(original))
    print("\nOptimized MiniCalc:\n")
    print(format_program_source(optimized))

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


# Notes:
#
# Every rewrite has to preserve the observable behavior: same output, same
# variables, same errors, same timing of errors.  17 * 3 -> 51 is safe because
# both operands are already constants and the operator has no side effects.
#
# x * 0 -> 0 is deliberately not done.  Even though the arithmetic answer is
# always zero, evaluating x could raise an undefined-variable error.  Dropping
# it would make a failing program start succeeding.
#
# The loop rule is the conservative one: collect every name assigned anywhere
# in the body and forget those constants before optimizing the body.  Constants
# that the loop never touches stay available, which is why `print scale` can
# become `print 42` even inside a loop.
