def parse_int(input: str) -> int:
    try:
        num = int(input)
    except ValueError:
        print("Got non integer argument: ", input)
    return num


def execute_one(text: str) -> int:
    tokens = text.split()
    if len(tokens) != 3:
        print(f"Wrong token coun, expected 3 got {len(tokens)}")
        return 0

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
        print("Unknown Operator")
        return 0
    pass


if __name__ == "__main__":
    assert execute_one("17 * 3") == 51
    assert execute_one("20 // 6") == 3
    assert execute_one("20 % 6") == 2
    assert execute_one("-7 - -2") == -5
