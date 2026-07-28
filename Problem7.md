## Stage 7 — Compile the same AST to Python

This backend emits Python source rather than executing MiniCalc itself.

### Problem

Write:

```python
def compile_to_python(program: list[Statement]) -> str:
    ...
```

Emit a function named `run` that returns a list of values produced by MiniCalc
`print` statements.

Example source: 
```
    # Parsing this text must not execute it.
    let x = 17 * 3
    print x
    x + 1
    print ans
```

Example target:

```python
def run():
    _output = []
    _v_x = (17 * 3)
    _output.append(_v_x)
    _ans = (_v_x + 1)
    _output.append(_ans)
    return _output
```

### Requirements

* Use indentation as compiler state.
* Mangle user variable names, for example `x` -> `_v_x`.
* Give every generated loop variable a unique name.
* Parenthesize generated binary expressions so Python precedence cannot alter the
  AST meaning.
* An empty loop body must emit `pass`.
* Use `exec()` only on the Python text your compiler generated.  Never use it to
  avoid parsing MiniCalc.
* Compare outputs from the direct interpreter, VM, and generated Python.

### Questions to answer

1. Why is this a compiler even though the target is another high-level language?
2. Why is it more accurately called a source-to-source compiler/transpiler?
3. What does name mangling protect against?
4. Which errors happen in the MiniCalc front end, and which are delegated to Python?

### Stretch

Use `dis.dis()` on the generated `run` function and compare CPython bytecode with
your own VM bytecode.
