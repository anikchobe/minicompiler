## Problem 8 — Perform work at compile time

### Part A: constant folding

Rewrite an expression whose operands are both integer constants:

```text
17 * 3  ->  51
```

Do not fold division or remainder by zero; leave the operation so normal runtime
behavior is preserved.

### Part B: constant propagation

Track variables whose values are known constants in straight-line code:

```text
let a = 17 * 3
let b = a + 1
print b
```

can become conceptually:

```text
let a = 51
let b = 52
print 52
```

### Part C: safe behavior around loops

A variable assigned inside a loop must generally be considered unknown both while
optimizing the body and after the loop.  Otherwise this incorrect transformation
could happen:

```text
let x = 0
repeat 3
    let x = x + 1
end
```

It is wrong to replace every `x + 1` with `1`; later iterations see changed values.
Constants that are not assigned in the loop may still be propagated into the body.

### Requirements

* The optimizer takes an AST and returns a new AST.
* Do not mutate the original AST.
* Compare unoptimized and optimized outputs in all three execution backends.
* Compare generated Python before and after optimization.
* Compare VM instruction counts before and after optimization.

### Example expected effect

For:

```text
let a = 17 * 3
let b = a + 1
print b
```

an unoptimized VM executes arithmetic opcodes at runtime.  The optimized program
contains constants instead, so those arithmetic opcodes disappear.

### Questions to answer

1. What proof obligation does every optimization have?
2. Under what assumptions would `x * 0 -> 0` be safe?  Why can the rewrite be
   unsafe if evaluating `x` could have a side effect or raise an error?
3. What is conservative analysis?
4. Does fewer source lines necessarily mean less runtime work?

### Stretch ideas

* Algebraic identities such as `x + 0`, `x * 1`, and `x // 1`; state the
  error/side-effect assumptions required by any rule that skips an operand.
* Dead constant assignment elimination.
* Loop unrolling for a small constant repeat count.
* A pass that counts arithmetic operations before and after optimization.
* Differential fuzz testing: generate random valid programs and compare all
  backends.

---

## Optional next projects

Choose only one at a time; each changes the shape of the front end substantially.

1. **Real expression parsing:** support `2 + 3 * 4`, parentheses, and unary minus
   with recursive descent or precedence climbing.
2. **Conditionals:** add comparisons and `if ... end`, then lower them to jumps.
3. **Static checking:** reject undefined variables before execution using a symbol
   table pass.
4. **Functions:** add parameters, call frames, and return values.
5. **Registers:** translate stack bytecode to a tiny register machine and discuss
   register allocation.
6. **Binary encoding:** assign numeric opcodes and encode instructions into bytes.
7. **Profiling:** count how often each opcode executes and use the data to choose an
   optimization.
