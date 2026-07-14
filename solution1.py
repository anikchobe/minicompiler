def execute_one(text: str) -> int:
    tokens = text.split()
    if len(tokens) != 3:
        print(f'Wrong token coun, expected 3 got {len(tokens)}')
        return 0
    try:
        left = int(tokens[0])
    except ValueError:
        print("Non-integer operand token 0")
    try:
        right = int(tokens[2])
    except ValueError:
        print("Non-integer operand token 2")

    if "+" in tokens:
        return left + right
    if "-" in tokens:
        return left - right
    if "*" in tokens:
        return left * right
    if "//" == tokens[1]:
        return left // right
    if "%" == tokens[1]:
        return left % right
    else:
        print("Unknown Operator")
        return 0
    pass



assert execute_one("17 * 3") == 51
assert execute_one("20 // 6") == 3
assert execute_one("20 % 6") == 2
assert execute_one("-7 - -2") == -5