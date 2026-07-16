def run_program(lines: list[str]) -> tuple[dict[str, int], list[int]]:
    resultDict = {}
    resultList = []
    for i in range(len(lines)):
        processLine(lines[i], i, resultDict, resultList)
    return resultDict, resultList
    

def processLine(line, lineNum, resultDict, resultList):
    tokens = line.split()
    if len(tokens) == 0:
        return
    if tokens[0] =='let':
        resultDict[tokens[1]] = processExpression(tokens[3:], lineNum, resultDict)
    elif tokens[0] == 'print':
        resultList.append(processExpression(tokens[1:], lineNum, resultDict))
    else:
        resultDict['ans'] = processExpression(tokens, lineNum, resultDict)




def processExpression(tokens, lineNum, resultDict):
    if len(tokens) == 1:
        return parse_int(tokens[0], resultDict)
    else:
        left, operator, right = tokens
        left = parse_int(left, resultDict)
        right = parse_int(right, resultDict)
        return execute_one(left, right, operator)

    


def parse_int(input: str, resultDict) -> int:
    try:
        num = int(input) if input not in resultDict else resultDict[input]
    except ValueError:
        print("Got non integer argument: ", input)
    return num


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
        print("Unknown Operator")
        return 0

def run_source(source: str) -> tuple[dict[str, int], list[int]]:
    return run_program(source.splitlines())


if __name__ == "__main__":
    demo = """
    let width = 17 * 3
    let height = 4
    let area = width * height
    print area
    area + 5
    print ans
    """
    env, values = run_source(demo)
    print("output:", values)
    print("environment:", env)
