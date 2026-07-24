"""Starter: expression records"""
from __future__ import annotations

from solution2 import execute_one

from dataclasses import dataclass

OPERATORS = {"+", "-", "*", "//", "%"}


class Expr:
    """Base class used only to group expression-node types."""


@dataclass(frozen=True)
class IntegerExpr(Expr):
    value: int

@dataclass(frozen=True)
class VariableExpr(Expr):
    name: str

@dataclass(frozen=True)
class BinaryExpr(Expr):
    left: Expr
    operator: str
    right: Expr

def parse_atom(token: str) -> Expr:
    if token.isdecimal():
        return IntegerExpr(int(token))
    elif token.isidentifier():
        return VariableExpr(token)
    raise ValueError(f"Invalid atom {token}")


def parse_expression(source: str) -> Expr:
    # TODO: accept one atom or ATOM OP ATOM.
    tokens = source.split()
    if len(tokens) == 1:
        return parse_atom(tokens)
    elif len(tokens) == 3:
        left = parse_atom(tokens[0])
        right = parse_atom(tokens[2])
        operator = tokens[1]
        if operator not in OPERATORS:
            raise ValueError(f"Unknown Operator {operator}")
        return BinaryExpr(left, operator, right)
    raise ValueError(f"Expression must contain 1 or 3 tokens but got {len(tokens)} in '{source}'")


def evaluate_expression(expression: Expr, environment: dict[str, int]) -> int:
    # TODO: recursively evaluate the object representation.
    if isinstance(expression, IntegerExpr):
        return expression.value
    
    if isinstance(expression, VariableExpr):
        if expression.name not in environment:
            raise NameError(f'Undefined Variable {expression.name}')
        return environment[expression.name] 
    
    if isinstance(expression, BinaryExpr):
        left = evaluate_expression(expression.left, environment)
        right = evaluate_expression(expression.right, environment)
        operator = expression.operator
        return execute_one(left, right, operator)

    raise TypeError(f'Unknown Node {type(expression).__name__}')


def _self_test() -> None:
    # Add tests here before completing the implementation.
    a = IntegerExpr(5)
    print(a)
    b = IntegerExpr(5)
    print(a == b)
    c = VariableExpr('x')
    print(c)
    d = VariableExpr('x')
    print(c == d)
    e = BinaryExpr(a, '+', c)
    print(e)
    f = BinaryExpr(IntegerExpr(5), '+', VariableExpr('x'))
    g = BinaryExpr(a, '+', f)
    print(g)
    print(e == f)
    print(parse_atom('55'))
    print(parse_atom('width'))
    #print(parse_atom('*'))
    print(parse_expression("a + 77"))
    #print(parse_expression("a ** 77"))
    #print(parse_expression("a + 77 + 7"))
    expression = parse_expression("width * 3")
    assert evaluate_expression(expression, {"width": 7}) == 21
    assert evaluate_expression(expression, {"width": 8}) == 24

    from dataclasses import FrozenInstanceError

    node = IntegerExpr(17)
    try:
        node.value = 99
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("a frozen AST node should reject mutation")
        

if __name__ == "__main__":
    _self_test()
