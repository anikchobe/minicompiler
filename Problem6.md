## Problem 6 — Structured loops lowered to jumps

### New syntax

```text
repeat EXPRESSION
    STATEMENT*
end
```

Loops may nest.  The count is evaluated once.  A count less than or equal to zero
executes the body zero times.

### Example

```text
let x = 1
repeat 5
    print x
    let x = x * 2
end
print x
```

Output:

```python
[1, 2, 4, 8, 16, 32]
```

### Problem A: recursive block parser

Add a `Repeat` AST node containing a count expression and a list of body statements.
Write a parser that consumes statements until it reaches the matching `end`.
Report unexpected and missing `end` tokens.

### Problem B: direct interpreter

Evaluate the count once and execute the body repeatedly.  Nested loops should work
without special cases beyond recursion.

### Problem C: lower the loop to bytecode

Add:

```text
JUMP target
JUMP_IF_NONPOSITIVE target
```

The compiler may create a hidden counter variable such as `@loop0`.  One possible
lowering is:

```text
compile count
STORE @loop0
loop_start:
LOAD @loop0
JUMP_IF_NONPOSITIVE loop_end
compile body
LOAD @loop0
PUSH_CONST 1
SUB
STORE @loop0
JUMP loop_start
loop_end:
```

The forward jump target is not known when the conditional instruction is first
emitted.  Emit a placeholder, compile the body, and patch the target afterward.

### Required tests

* Zero iterations.
* Negative count.
* One iteration.
* Nested loops.
* A loop count that uses a variable.
* A loop body that changes a variable.
* Missing `end` and unexpected `end`.

### Questions to answer

1. How does structured control flow become changes to the program counter?
2. What is backpatching?
3. Why must the loop count be evaluated only once?
4. Why are compiler-generated names kept outside the user identifier namespace?

### Stretch

Instead of hidden variables, design dedicated loop-stack VM instructions.  Compare
which design makes the compiler simpler and which makes the VM simpler.
