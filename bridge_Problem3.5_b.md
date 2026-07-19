### Replace the boilerplate with data classes

Copy the completed file from the previous exercise and import:

```python
from dataclasses import dataclass
```

Replace each node class with a declaration like:

```python
@dataclass(frozen=True)
class IntegerExpr(Expr):
    value: int
```

Do the same for `VariableExpr` and `BinaryExpr`.  Delete your handwritten
`__init__`, `__repr__`, and `__eq__` methods.  Do not change the parser, evaluator,
or tests.

All old tests should still pass.

Add one new test:

```python
from dataclasses import FrozenInstanceError

node = IntegerExpr(17)
try:
    node.value = 99
except FrozenInstanceError:
    pass
else:
    raise AssertionError("a frozen AST node should reject mutation")
```
### Stretch

Add a `negate(expression)` function that returns a **new** expression equivalent
to `0 - expression`.  It must not alter the old expression.


### Exceptions

Python exceptions provide a separate
control path for failure.

Declare an exception hierarchy:

```python
class MiniCalcError(Exception):
    """Base class for errors caused by MiniCalc source or execution."""


class MiniCalcSyntaxError(MiniCalcError):
    """The input does not match the MiniCalc grammar."""


class MiniCalcRuntimeError(MiniCalcError):
    """The input is well formed but cannot execute."""
```

Do **not** catch and re-raise the exception at every level.  Let Python propagate it
through `execute_line` and `run_program` automatically.

Catch it once at the user-interface boundary:

```python
try:
    values = run_program(program)
except MiniCalcError as error:
    print(f"error: {error}")
else:
    print(values)
```

This catch handles both subclasses because they inherit from `MiniCalcError`.

### Required behavior

```python
assert run_program(["1 - 2", "ans * 3"]) == [-1, -3]
```

Malformed syntax raises `MiniCalcSyntaxError`; reading `ans` before it has a value
or dividing by zero raises `MiniCalcRuntimeError`.

Use tests such as:

```python
try:
    run_program(["3 ** 4"])
except MiniCalcSyntaxError as error:
    assert "unknown operator" in str(error)
else:
    raise AssertionError("an exception should have been raised")
```


