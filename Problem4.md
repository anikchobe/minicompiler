## Parse first, execute later

The earlier implementation parses and executes each line at the same
time.  Now split the front end from execution.

### Problem

Define AST node classes for:

* integer literal
* variable reference
* binary expression
* `let` statement
* `print` statement
* bare expression statement

Then write:

```python
def parse_program(source: str) -> list[Statement]:
    ...

def execute_program(program: list[Statement]) -> Result:
    ...
```

Parsing must not execute the program.  Execution must not inspect source strings or
call `split()`.

### Example AST shape

Source:

```text
let area = width * height
```

Conceptual AST:

```text
Let(name="area",
    expression=Binary("*", Variable("width"), Variable("height")))
```

### Requirements

* Keep the original source line number in each statement node.
* Ignore comments beginning with `#`.
* Reject malformed syntax during parsing.
* Detect undefined variables during execution.
* Parse once and execute the same AST twice with separate environments.

### Tests to add

* Parsing does not produce output.
* Reusing an AST with two independent environments produces independent results.
* A syntax error occurs even inside a line that would never be reached later.
* Comments and blank lines are ignored.

### Questions to answer

1. Why is an AST useful if the direct interpreter could run strings?
2. Which data is syntax, and which data is runtime state?
3. Why do compilers usually have multiple intermediate representations?

### Stretch

Write a pretty-printer that turns the AST back into normalized MiniCalc source.
