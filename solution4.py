from __future__ import annotations

import keyword
from dataclasses import dataclass
from typing import TypeAlias


class MiniCalcSyntaxError(ValueError):
    """Raised when MiniCalc source does not match the tiny grammar."""


class MiniCalcRuntimeError(RuntimeError):
    """Raised for a well-formed program that cannot execute."""


def apply_operator(left: int, operator: str, right: int) -> int:
    """Execute one already-decoded arithmetic operation."""
    match operator:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "//":
            return left // right
        case "%":
            return left % right
        case _:
            raise MiniCalcSyntaxError(f"unknown operator {operator!r}")


OPERATORS = {"+", "-", "*", "//", "%"}
RESERVED_NAMES = {"let", "print", "repeat", "end"}


# ------------------------------ AST node types ------------------------------


@dataclass(frozen=True)
class IntegerExpr:
    value: int


@dataclass(frozen=True)
class VariableExpr:
    name: str


@dataclass(frozen=True)
class BinaryExpr:
    left: Expr
    operator: str
    right: Expr


Expr: TypeAlias = IntegerExpr | VariableExpr | BinaryExpr


class LetStmt:
    pass


class PrintStmt:
    pass


class ExprStmt:
    pass


Stmt: TypeAlias = LetStmt | PrintStmt | ExprStmt
Program: TypeAlias = list[Stmt]


@dataclass(frozen=True)
class ExecutionResult:
    environment: dict[str, int]
    output: list[int]


# --------------------------------- Parser ----------------------------------


def strip_comment(raw_line: str) -> str:
    pass


def validate_identifier(name: str, line_number: int) -> None:
    pass


def parse_atom_token(token: str, line_number: int) -> Expr:
    try:
        return IntegerExpr(int(token))
    except ValueError:
        validate_identifier(token, line_number)
        return VariableExpr(token)


def parse_expression_tokens(tokens: list[str], line_number: int) -> Expr:
    if len(tokens) == 1:
        return parse_atom_token(tokens[0], line_number)

    if len(tokens) == 3:
        left_token, operator, right_token = tokens
        if operator not in OPERATORS:
            raise MiniCalcSyntaxError(
                f"line {line_number}: unknown operator {operator!r}"
            )
        return BinaryExpr(
            parse_atom_token(left_token, line_number),
            operator,
            parse_atom_token(right_token, line_number),
        )

    raise MiniCalcSyntaxError(
        f"line {line_number}: an expression must contain 1 or 3 tokens"
    )


def parse_statement_tokens(tokens: list[str], line_number: int) -> Stmt:
    if not tokens:
        raise MiniCalcSyntaxError(f"line {line_number}: empty statement")

    pass


def parse_program(source: str) -> Program:
    program: Program = []
    pass


# ------------------------------- Interpreter -------------------------------


def evaluate_expression(expression: Expr, environment: dict[str, int]) -> int:
    if isinstance(expression, IntegerExpr):
        return expression.value

    if isinstance(expression, VariableExpr):
        if expression.name not in environment:
            raise MiniCalcRuntimeError(f"undefined variable {expression.name!r}")
        return environment[expression.name]

    if isinstance(expression, BinaryExpr):
        left = evaluate_expression(expression.left, environment)
        right = evaluate_expression(expression.right, environment)
        return apply_operator(left, expression.operator, right)

    raise TypeError(f"unknown expression node: {type(expression).__name__}")


def execute_statement(
    statement: Stmt, environment: dict[str, int], output: list[int]
) -> None:
    pass

    raise TypeError(f"unknown statement node: {type(statement).__name__}")


def execute_program(
    program: Program, initial_environment: dict[str, int] | None = None
) -> ExecutionResult:
    pass


def run_source(
    source: str, initial_environment: dict[str, int] | None = None
) -> ExecutionResult:
    return execute_program(parse_program(source), initial_environment)




def _self_test() -> None:
    source = """
        # Parsing this text must not execute it.
        let x = 17 * 3
        print x
        x + 1
        print ans
    """
    program = parse_program(source)
    first = execute_program(program)
    second = execute_program(program)
    assert first.output == [51, 52]
    assert first == second
    assert first.environment is not second.environment


if __name__ == "__main__":
    _self_test()
    demo = """
    let width = 17 * 3
    let height = 4
    let area = width * height
    print area
    """
    ast = parse_program(demo)
    print("AST:")
    for node in ast:
        print("  ", node)
    print("result:", execute_program(ast))
