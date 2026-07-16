## Variables, assignment, and a symbol table

### New syntax

Expressions may now contain either one atom or one binary operation:

```text
5
x
x + 3
```

Statements are:

```text
let NAME = EXPRESSION
print EXPRESSION
EXPRESSION
```

A bare expression stores its result in `ans`.  `let` stores a value under a name.
`print` appends a value to the program's output.

### Problem

Write:

```python
def run_program(lines: list[str]) -> tuple[dict[str, int], list[int]]:
    ...
```

Use a dictionary as the environment/symbol table.

### Example

```text
let width = 17 * 3
let height = 4
let area = width * height
print area
area + 5
print ans
```

Output:

```python
[204, 209]
```

Final environment includes:

```python
{"width": 51, "height": 4, "area": 204, "ans": 209}
```

### Requirements

* A name must be a valid identifier.
* A read of an undefined name is a runtime error.
* Do not allow `let ans = ...`; `ans` is a language-defined name.
* Keep `parse_atom`, `evaluate_expression`, and `execute_statement` separate.

### Questions to answer

1. What does the dictionary correspond to in a real implementation?
2. At what point is a misspelled variable discovered?
3. What would static name checking have to do differently?
