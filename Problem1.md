## Stage 1 — Decode and execute one instruction

### Problem

Write:

```python
def execute_one(text: str) -> int:
    ...
```

The input has exactly three whitespace-separated tokens:

```text
INTEGER OPERATOR INTEGER
```

Support `+`, `-`, `*`, `//`, and `%`.  Use `text.split()` to tokenize.  Convert the
operands with `int()`.  Dispatch on the operator with `if`/`elif` or `match`.
Do not use `eval()`.

### Examples

```python
execute_one("17 * 3")   # 51
execute_one("20 // 6")  # 3
execute_one("-7 + 2")   # -5
```

### Required errors

* Wrong token count: syntax error.
* Unknown operator: syntax error.
* Non-integer operand: syntax error.
* Division by zero may use Python's normal `ZeroDivisionError`.

### Minimum tests

```python
assert execute_one("17 * 3") == 51
assert execute_one("20 // 6") == 3
assert execute_one("20 % 6") == 2
assert execute_one("-7 - -2") == -5
```

Also write tests that expect errors.

### Questions to answer

1. Which line is “fetch,” which part is “decode,” and which part is “execute”?
2. Why does requiring spaces make tokenization easy?
3. What new ambiguity appears if spaces are optional?
