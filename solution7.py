from __future__ import annotations

from solution4 import (
    BinaryExpr,
    Expr,
    ExprStmt,
    IntegerExpr,
    LetStmt,
    PrintStmt,
    Stmt,
    Program,
    VariableExpr,
)
from solution5 import execute_bytecode
from solution5 import (
    compile_program as compile_to_bytecode,
    execute_program,
    parse_program,
)


class PythonCompiler:
    def __init__(self) -> None:
        self.lines: list[str] = []

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

    def emit(self, indentation: int, text: str) -> None:
        self.lines.append("    " * indentation + text)

    def statement(self, statement: Stmt, indentation: int) -> None:
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


    def compile(self, program: Program) -> str:
        self.emit(0, "def run():")
        self.emit(1, "_output = []")
        for statement in program:
            self.statement(statement, 1)
        self.emit(1, "return _output")
        return "\n".join(self.lines) + "\n"


def compile_to_python(program: Program) -> str:
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


def compile_and_run(program: Program) -> list[int]:
    return execute_generated_python(compile_to_python(program))



if __name__ == "__main__":
    demo_source = """
    # Parsing this text must not execute it.
    let x = 17 * 3
    print x
    x + 1
    print ans
    """
    # demo_source = """
    # let x = 1
    # repeat 5
    #     print x
    #     let x = x * 2
    # end
    # print x
    # """
    demo_program = parse_program(demo_source) # AST
    generated_source = compile_to_python(demo_program) # Generate python from AST
    print(generated_source)
    python_output = execute_generated_python(generated_source) # Execute generated Python
    
    direct = execute_program(demo_program).output # Interpret AST
    bytecode = compile_to_bytecode(demo_program)  # Generate VM Bytecode
    vm = execute_bytecode(bytecode).output        # Run bytecode on VM

    assert direct == python_output == vm == [51, 52]
    
    print("output:", execute_generated_python(generated_source))
