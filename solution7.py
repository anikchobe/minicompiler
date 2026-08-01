from __future__ import annotations

from solution4 import (
    BinaryExpr,
    Expr,
    ExprStmt,
    IntegerExpr,
    LetStmt,
    PrintStmt,
    VariableExpr,
)
from solution5 import execute_bytecode
from solution6 import (
    LoopProgram,
    LoopStatement,
    RepeatStmt,
    compile_program as compile_to_bytecode,
    execute_program,
    parse_program,
)


class PythonCompiler:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.next_loop_id = 0

    @staticmethod
    def mangle_variable(name: str) -> str:
        # Source names are validated identifiers, but mangling still protects the
        # backend's locals and makes compiler-created names visibly distinct.
        return "_ans" if name == "ans" else f"_v_{name}"

    def expression(self, expression: Expr) -> str:
        if isinstance(expression, IntegerExpr):
            return str(expression.value)
        if isinstance(expression, VariableExpr):
            return self.mangle_variable(expression.name)
        if isinstance(expression, BinaryExpr):
            left = self.expression(expression.left)
            right = self.expression(expression.right)
            # Parentheses preserve the AST meaning even after the language grows
            # to support larger expressions with precedence.
            return f"({left} {expression.operator} {right})"
        raise TypeError(type(expression).__name__)

    def emit(self, indentation: int, text: str) -> None:
        self.lines.append("    " * indentation + text)

    def statement(self, statement: LoopStatement, indentation: int) -> None:
        if isinstance(statement, LetStmt):
            self.emit(
                indentation,
                f"{self.mangle_variable(statement.name)} = "
                f"{self.expression(statement.expression)}",
            )
            return

        if isinstance(statement, PrintStmt):
            self.emit(
                indentation,
                f"_output.append({self.expression(statement.expression)})",
            )
            return

        if isinstance(statement, ExprStmt):
            self.emit(
                indentation,
                f"_ans = {self.expression(statement.expression)}",
            )
            return

        if isinstance(statement, RepeatStmt):
            loop_id = self.next_loop_id
            self.next_loop_id += 1
            loop_variable = f"_loop_{loop_id}"
            count = self.expression(statement.count)
            self.emit(
                indentation,
                f"for {loop_variable} in range(max(0, {count})):",
            )
            if statement.body:
                for body_statement in statement.body:
                    self.statement(body_statement, indentation + 1)
            else:
                self.emit(indentation + 1, "pass")
            return

        raise TypeError(type(statement).__name__)

    def compile(self, program: LoopProgram) -> str:
        self.emit(0, "def run():")
        self.emit(1, "_output = []")
        for statement in program:
            self.statement(statement, 1)
        self.emit(1, "return _output")
        return "\n".join(self.lines) + "\n"


def compile_to_python(program: LoopProgram) -> str:
    return PythonCompiler().compile(program)


def execute_generated_python(source: str) -> list[int]:
    namespace: dict[str, object] = {}
    code_object = compile(source, "<generated MiniCalc Python>", "exec")
    exec(code_object, namespace)
    run = namespace.get("run")
    if not callable(run):
        raise RuntimeError("generated Python did not define a callable run()")
    result = run()
    if not isinstance(result, list) or not all(isinstance(x, int) for x in result):
        raise RuntimeError("generated run() returned an invalid output value")
    return result


def compile_and_run(program: LoopProgram) -> list[int]:
    return execute_generated_python(compile_to_python(program))


if __name__ == "__main__":
    demo_source = """
    let x = 1
    repeat 5
        print x
        let x = x * 2
    end
    print x
    """
    demo_program = parse_program(demo_source)
    generated_source = compile_to_python(demo_program)
    print(generated_source)
    python_output = execute_generated_python(generated_source)

    direct = execute_program(demo_program).output
    bytecode = compile_to_bytecode(demo_program)
    vm = execute_bytecode(bytecode).output

    assert direct == python_output == vm == [1, 2, 4, 8, 16, 32]
    print("output:", python_output)


# Notes:
#
# Each repeat becomes a Python for loop with a fresh _loop_N name.  Using
# range(max(0, count)) matches the MiniCalc rule that a nonpositive count runs
# zero times, and it evaluates the count once, just like the VM lowering.
#
# Parentheses around every binary expression mean Python's precedence can never
# change the shape of the MiniCalc AST.  That is boring, and it is the point.
#
# exec() is only used on the Python text this compiler just generated.  It is
# never used to evaluate MiniCalc source directly.
