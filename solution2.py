from solution1 import MiniCompilerSyntaxError

def parse_int(input: str, result: list[int]) -> int:
    """Parse integer or ans identifier"""
    try:
        return int(input) if input != "ans" else result[-1]
    except ValueError:
        raise MiniCompilerSyntaxError("Got non integer argument: ", input)

def execute_one(left, right, operator):
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
        

def run_program(input: list[str]) -> list[int]:
    result = []
    for i in range(len(input)):
        tokens = input[i].split()
        if len(tokens) == 0:
            continue
        if len(tokens) != 3:
            raise MiniCompilerSyntaxError(f"Wrong token count on line {i}, expected 3 got {len(tokens)}")
        if i == 0 and "ans" in tokens:
            raise MiniCompilerSyntaxError("Cannot read ans before executing any instruction")
        left, operator, right = tokens
        left = parse_int(left, result)
        right = parse_int(right, result)
        result.append(execute_one(left, right, operator))
    return result


if __name__ == "__main__":
    assert run_program(["17 * 3", "", "ans + 9", "ans // 5"]) == [51, 60, 12]
