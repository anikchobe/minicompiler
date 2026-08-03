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


def negate(expression: Expr) -> Expr:
    return BinaryExpr(IntegerExpr(0), "-", expression)


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


# --------------------------- Exceptions instead ---------------------------


class MiniCalcError(Exception):
    """Base class for errors caused by MiniCalc source or execution."""


class MiniCalcSyntaxError(MiniCalcError):
    """The input does not match the MiniCalc grammar."""


class MiniCalcRuntimeError(MiniCalcError):
    """The input is well formed but cannot execute."""


def read_operand(token: str, ans: int | None, line_number: int) -> int:
    if token == "ans":
        if ans is None:
            raise MiniCalcRuntimeError(
                f"line {line_number}: ans was read before it had a value"
            )
        return ans

    try:
        return int(token)
    except ValueError as cause:
        raise MiniCalcSyntaxError(
            f"line {line_number}: expected a signed integer or 'ans', "
            f"got {token!r}"
        ) from cause


def apply_operator(left: int, operator: str, right: int, line_number: int) -> int:
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "//":
        if right == 0:
            raise MiniCalcRuntimeError(
                f"line {line_number}: integer division by zero"
            )
        return left // right
    if operator == "%":
        if right == 0:
            raise MiniCalcRuntimeError(
                f"line {line_number}: integer modulo by zero"
            )
        return left % right
    raise MiniCalcSyntaxError(
        f"line {line_number}: unknown operator {operator!r}"
    )


def execute_line(source: str, ans: int | None, line_number: int) -> int:
    tokens = source.split()
    if len(tokens) != 3:
        raise MiniCalcSyntaxError(
            f"line {line_number}: expected exactly 3 tokens, got {len(tokens)}"
        )
    left_token, operator, right_token = tokens
    left = read_operand(left_token, ans, line_number)
    right = read_operand(right_token, ans, line_number)
    return apply_operator(left, operator, right, line_number)


def run_program(lines: list[str]) -> list[int]:
    ans: int | None = None
    values: list[int] = []
    for line_number, raw_line in enumerate(lines, start=1):
        source = raw_line.strip()
        if not source:
            continue
        ans = execute_line(source, ans, line_number)
        values.append(ans)
    return values


def display_program(lines: list[str]) -> None:
    try:
        values = run_program(lines)
    except MiniCalcError as error:
        print(f"error: {error}")
    else:
        print(values)


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
    assert evaluate_expression(negate(expression), {"width": 7}) == -21

    from dataclasses import FrozenInstanceError

    node = IntegerExpr(17)
    try:
        node.value = 99
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("a frozen AST node should reject mutation")

    assert run_program(["1 - 2", "ans * 3"]) == [-1, -3]

    try:
        run_program(["3 ** 4"])
    except MiniCalcSyntaxError as error:
        assert "unknown operator" in str(error)
    else:
        raise AssertionError("unknown operator should raise")

    try:
        run_program(["ans + 1"])
    except MiniCalcRuntimeError as error:
        assert "before it had a value" in str(error)
    else:
        raise AssertionError("missing ans should raise")

    try:
        run_program(["10 + 2", "ans // 0"])
    except MiniCalcRuntimeError as error:
        assert "line 2" in str(error)
    else:
        raise AssertionError("division by zero should raise")
        

if __name__ == "__main__":
    _self_test()
