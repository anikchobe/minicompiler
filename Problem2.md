## A sequence of instructions and one register

### Problem

Write:

```python
def run_program(lines: list[str]) -> list[int]:
    ...
```

Each line is still one binary arithmetic instruction, but either operand may now
be the word `ans`, meaning the result of the previous instruction.  Return every
result in order.

### Example

```text
17 * 3
ans + 9
ans // 5
```

Result:

```python
[51, 60, 12]
```

### Requirements

* Reading `ans` before any instruction has completed is a runtime error.
* Skip blank lines.
* Report the line number in syntax/runtime errors when practical.
* Keep tokenization and execution in separate helper functions.

### Questions to answer

1. Is `ans` closer to a variable, a CPU register, or both?
2. What state has to survive from one line to the next?
3. Could the lines be evaluated in parallel?  Why or why not?

### Stretch

Print a trace table after each instruction:

```text
line | source    | old ans | new ans
1    | 17 * 3    | None    | 51
2    | ans + 9   | 51      | 60
```
