from pytest import fixture


@fixture
def sample():
    return [
        'forward 5',
        'down 5',
        'forward 8',
        'up 3',
        'down 8',
        'forward 2',
    ]


def read(filename: str) -> list:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def main_part1(commands: list) -> int:
    x, depth = 0, 0
    for cmd in commands:
        direction, step = cmd.split()
        if direction == 'forward':
            x += int(step)
        elif direction == 'up':
            depth -= int(step)
        elif direction == 'down':
            depth += int(step)
    return x * depth


def test_part1(sample):
    assert main_part1(sample) == 150


def main_part2(commands: list) -> int:
    x, depth, aim = 0, 0, 0
    for cmd in commands:
        direction, step = cmd.split()
        step = int(step)
        if direction == 'forward':
            x += step
            depth += step * aim
        elif direction == 'up':
            aim -= step
        elif direction == 'down':
            aim += step
    return x * depth


def test_part2(sample):
    assert main_part2(sample) == 900


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
