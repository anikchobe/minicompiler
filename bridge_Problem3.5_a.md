## Bridge A — Build expression objects by hand

Your Stage 3 interpreter reads tokens and immediately computes a value.  Before
building a complete AST, represent just an **expression** as an object.

The tiny expression grammar remains:

```text
EXPRESSION := ATOM
            | ATOM OPERATOR ATOM

ATOM       := INTEGER | NAME
OPERATOR   := + | - | * | // | %
```

Examples:

```text
17
width
17 * 3
width * height
```

### Part A1: ordinary classes only

Start with `starter/bridge_a_manual_ast.py`. 

Implement these classes:

```python
class IntegerExpr(Expr):
    # field: value

class VariableExpr(Expr):
    # field: name

class BinaryExpr(Expr):
    # fields: left, operator, right
```

For every class, implement all three pieces of machinery yourself:

1. `__init__` to save the fields,
2. `__repr__` to produce a useful debugging representation, and
3. `__eq__` so two separately created nodes compare by contents rather than by
   object identity.

Use these exact representation shapes:

```python
repr(IntegerExpr(17))
# "IntegerExpr(value=17)"

repr(VariableExpr("x"))
# "VariableExpr(name='x')"

repr(BinaryExpr(IntegerExpr(17), "*", VariableExpr("x")))
# "BinaryExpr(left=IntegerExpr(value=17), operator='*', right=VariableExpr(name='x'))"
```

Then implement:

```python
def parse_expression(source: str) -> Expr:
    ...

def evaluate_expression(expression: Expr,
                        environment: dict[str, int]) -> int:
    ...
```

`parse_expression` must create objects; it must not evaluate them.
`evaluate_expression` must consume objects; it must not call `split()` or inspect
source text.

### Tests to write before finishing

```python
a = IntegerExpr(17)
b = IntegerExpr(17)

assert a is not b       # different allocations
assert a == b           # same represented expression
assert repr(a) == "IntegerExpr(value=17)"
```

Also test structural equality recursively:

```python
first = BinaryExpr(IntegerExpr(17), "*", VariableExpr("x"))
second = BinaryExpr(IntegerExpr(17), "*", VariableExpr("x"))
third = BinaryExpr(IntegerExpr(17), "+", VariableExpr("x"))

assert first == second
assert first != third
```

Finally:

```python
expression = parse_expression("width * 3")
assert evaluate_expression(expression, {"width": 7}) == 21
```

### Observe the default behavior

Before implementing `__repr__` and `__eq__`, temporarily print and compare two
nodes.  Record what happens.
