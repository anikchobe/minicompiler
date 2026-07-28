## Problem 5 — Compile to stack bytecode and build a VM

The direct interpreter walks the AST.  This stage translates the AST into a lower
level instruction sequence and then executes those instructions.

### Instruction set

Use instructions similar to:

```text
PUSH_CONST value
LOAD name
STORE name
ADD
SUB
MUL
DIV
MOD
PRINT
HALT
```

Every instruction can be represented as a fixed two-field tuple:

```python
("PUSH_CONST", 17)
("MUL", None)
```

### Problem A: compiler

Write:

```python
def compile_program(program: list[Statement]) -> list[Instruction]:
    ...
```

For a binary expression, compile the left operand, then the right operand, then the
operator.  For example:

```text
17 * 3
```

becomes:

```text
PUSH_CONST 17
PUSH_CONST 3
MUL
STORE ans
HALT
```

### Problem B: virtual machine

Write a VM with:

* a program counter (`pc`)
* an operand stack
* a variable dictionary
* an output list

The VM repeatedly fetches `code[pc]`, decodes its opcode, executes it, and advances
(or later changes) `pc`.

### Example

Source:

```text
let x = 17 * 3
print x
```

Possible disassembly:

```text
0000  PUSH_CONST  17
0001  PUSH_CONST  3
0002  MUL
0003  STORE       x
0004  LOAD        x
0005  PRINT
0006  HALT
```

### Requirements

* Verify stack underflow rather than crashing with a confusing list error.
* Undefined `LOAD` is a runtime error.
* Return the number of VM instructions executed.
* Direct interpretation and VM execution must produce the same output and visible
  variables for a collection of test programs.

### Questions to answer

1. Why must subtraction pop the right operand before the left operand?
2. Which VM state resembles registers, memory, and the instruction pointer?
3. What work moved from runtime into compilation?
4. Is this bytecode an AST, machine code, or an intermediate representation?

### Stretch

Add a tracing mode that prints `pc`, instruction, stack, and variables before every
step.  Hand-predict the trace before running it.

