"""Expression records built without dataclasses."""
from __future__ import annotations

from solution2 import execute_one


OPERATORS = {"+", "-", "*", "//", "%"}


class Expr:
    """Base class used only to group expression-node types."""


class IntegerExpr(Expr):
    def __init__(self, value: int) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"IntegerExpr(value={self.value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntegerExpr):
            return NotImplemented
        return self.value == other.value


class VariableExpr(Expr):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"VariableExpr(name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VariableExpr):
            return NotImplemented
        return self.name == other.name


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: str, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        return (
            "BinaryExpr("
            f"left={self.left!r}, "
            f"operator={self.operator!r}, "
            f"right={self.right!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryExpr):
            return NotImplemented
        return (
            self.left == other.left
            and self.operator == other.operator
            and self.right == other.right
        )


def parse_atom(token: str) -> Expr:
    if token.isdecimal() or (
        len(token) > 1 and token[0] in "+-" and token[1:].isdecimal()
    ):
        return IntegerExpr(int(token))
    if token.isidentifier():
        return VariableExpr(token)
    raise ValueError(f"Invalid atom {token}")


def parse_expression(source: str) -> Expr:
    tokens = source.split()
    if len(tokens) == 1:
        return parse_atom(tokens[0])
    if len(tokens) == 3:
        left = parse_atom(tokens[0])
        right = parse_atom(tokens[2])
        operator = tokens[1]
        if operator not in OPERATORS:
            raise ValueError(f"Unknown Operator {operator}")
        return BinaryExpr(left, operator, right)
    raise ValueError(
        f"Expression must contain 1 or 3 tokens but got {len(tokens)} in '{source}'"
    )


def evaluate_expression(expression: Expr, environment: dict[str, int]) -> int:
    if isinstance(expression, IntegerExpr):
        return expression.value

    if isinstance(expression, VariableExpr):
        if expression.name not in environment:
            raise NameError(f"Undefined Variable {expression.name}")
        return environment[expression.name]

    if isinstance(expression, BinaryExpr):
        left = evaluate_expression(expression.left, environment)
        right = evaluate_expression(expression.right, environment)
        return execute_one(left, right, expression.operator)

    raise TypeError(f"Unknown Node {type(expression).__name__}")


def _self_test() -> None:
    a = IntegerExpr(17)
    b = IntegerExpr(17)
    assert a is not b
    assert a == b
    assert repr(a) == "IntegerExpr(value=17)"

    first = BinaryExpr(IntegerExpr(17), "*", VariableExpr("x"))
    second = BinaryExpr(IntegerExpr(17), "*", VariableExpr("x"))
    third = BinaryExpr(IntegerExpr(17), "+", VariableExpr("x"))
    assert first == second
    assert first != third
    assert repr(first) == (
        "BinaryExpr(left=IntegerExpr(value=17), operator='*', "
        "right=VariableExpr(name='x'))"
    )

    expression = parse_expression("width * 3")
    assert evaluate_expression(expression, {"width": 7}) == 21
    assert evaluate_expression(parse_expression("-7 + 2"), {}) == -5


if __name__ == "__main__":
    _self_test()
    demo = parse_expression("width * 3")
    print("parsed:", demo)
    print("value:", evaluate_expression(demo, {"width": 7}))
