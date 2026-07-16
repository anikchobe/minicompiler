def run_program(lines: list[str]) -> tuple[dict[str, int], list[int]]:
    pass


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
