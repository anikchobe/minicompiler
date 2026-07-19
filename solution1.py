class MiniCompilerSyntaxError(ValueError):
    """Raised when source does not match the grammar"""


def parse_int(input: str) -> int:
    try:
        return int(input)
    except ValueError:
        raise MiniCompilerSyntaxError(f"Expected integer, got {input}")

def execute_one(text: str) -> int:
    """execute source of the form INTEGER OP INTEGER """

    tokens = text.split()
    if len(tokens) != 3:
        raise MiniCompilerSyntaxError(f"Wrong token count, expected 3 got {len(tokens)}")
        
    left, operator, right = tokens
    left = parse_int(left)
    right = parse_int(right)

    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "//":
        return left // right
    if operator == "%":
        return left % right
    else:
        raise MiniCompilerSyntaxError("Unknown Operator")
        
    


if __name__ == "__main__":
    assert execute_one("17 * 3") == 51
    assert execute_one("20 // 6") == 3
    assert execute_one("20 % 6") == 2
    assert execute_one("-7 - -2") == -5

    try:
        execute_one("3 ** 4")
    except MiniCompilerSyntaxError:
        pass
    else:
        raise AssertionError("unknown operator should fail")

