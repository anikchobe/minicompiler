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


@dataclass(frozen=True)
class LetStmt:
    name: str
    expression: Expr
    lineNum: int


@dataclass(frozen=True)
class PrintStmt:
    expression: Expr
    lineNum: int


@dataclass(frozen=True)
class ExprStmt:
    expression: Expr
    lineNum: int


Stmt: TypeAlias = LetStmt | PrintStmt | ExprStmt
Program: TypeAlias = list[Stmt]


@dataclass(frozen=True)
class ExecutionResult:
    environment: dict[str, int]
    output: list[int]


# --------------------------------- Parser ----------------------------------


def strip_comment(raw_line: str) -> str:
    if '#' in raw_line:
        return raw_line[:raw_line.index("#")]
    return raw_line


def validate_identifier(name: str, line_number: int) -> None:
    if not name.isidentifier() or name in RESERVED_NAMES or keyword.iskeyword(name):
        raise NameError


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
    if tokens[0] == 'let':
        return LetStmt(tokens[1], parse_expression_tokens(tokens[3:], line_number), line_number)
    if tokens[0] == 'print':
        return PrintStmt(parse_expression_tokens(tokens[1:], line_number), line_number)
    return ExprStmt(parse_expression_tokens(tokens, line_number), line_number)
    


def parse_program(source: str) -> Program:
    program: Program = []
    for lineNum, line in enumerate(source.splitlines()):
        line = strip_comment(line)
        tokens = line.split()
        if len(tokens) == 0:
            continue
        program.append(parse_statement_tokens(tokens, lineNum))
    return program
    


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

    raise MiniCalcRuntimeError(f"unknown expression node: {type(expression).__name__}")


def execute_statement(
    statement: Stmt, environment: dict[str, int], output: list[int]
) -> None:
    if isinstance(statement, LetStmt):
        environment[statement.name] = evaluate_expression(statement.expression, environment)
    if isinstance(statement, PrintStmt):
        output.append(evaluate_expression(statement.expression, environment))
    environment['ans'] = evaluate_expression(statement.expression, environment)
    


def execute_program(
    program: Program, initial_environment: dict[str, int] | None = None
) -> ExecutionResult:
    environment = dict(initial_environment) if initial_environment else {}
    result: list[int] = []
    for statement in program:
        execute_statement(statement, environment, result)
    return ExecutionResult(environment, result)
    


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
    let height = 4 # is this enough?
    let area = width * height
    # this is a comment
    print area
    """
    ast = parse_program(demo)
    print("AST:")
    for node in ast:
        print("  ", node)
    print("result:", execute_program(ast))
