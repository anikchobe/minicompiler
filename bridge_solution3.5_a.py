"""Starter: expression records"""

from __future__ import annotations

OPERATORS = {"+", "-", "*", "//", "%"}


class Expr:
    """Base class used only to group expression-node types."""


class IntegerExpr(Expr):
    # TODO: __init__, __repr__, and __eq__
    pass


class VariableExpr(Expr):
    # TODO: __init__, __repr__, and __eq__
    pass


class BinaryExpr(Expr):
    # TODO: __init__, __repr__, and __eq__
    pass


def parse_atom(token: str) -> Expr:
    # TODO: return IntegerExpr or VariableExpr.
    raise NotImplementedError


def parse_expression(source: str) -> Expr:
    # TODO: accept one atom or ATOM OP ATOM.
    raise NotImplementedError


def evaluate_expression(expression: Expr, environment: dict[str, int]) -> int:
    # TODO: recursively evaluate the object representation.
    raise NotImplementedError


def _self_test() -> None:
    # Add tests here before completing the implementation.
    pass


if __name__ == "__main__":
    _self_test()
