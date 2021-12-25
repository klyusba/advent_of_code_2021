from pytest import fixture
from typing import List, Tuple
import numpy as np


@fixture
def sample():
    return """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".splitlines()


def read(filename: str) -> list:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def parse(vents: List[str]) -> Tuple[List, int, int]:
    x_max, y_max = 0, 0
    res = []
    for line in vents:
        p_from, p_to = line.split(' -> ')
        x_from, y_from = map(int, p_from.split(','))
        x_to, y_to = map(int, p_to.split(','))

        if x_from < x_to or x_from == x_to and y_from < y_to:
            res.append((
                (x_from, y_from), (x_to, y_to)
            ))
        else:
            res.append((
                (x_to, y_to), (x_from, y_from)
            ))
        x_max = max(x_max, x_from, x_to)
        y_max = max(y_max, y_from, y_to)

    return res, x_max, y_max


def main_part1(vents: list) -> int:
    lines, x_max, y_max = parse(vents)
    field = np.zeros((x_max+1, y_max+1))
    for (x_from, y_from), (x_to, y_to) in lines:
        if x_from == x_to:
            field[x_from, y_from:y_to+1] += 1
        elif y_from == y_to:
            field[x_from:x_to+1, y_from] += 1
    return (field >= 2).sum()


def test_part1(sample):
    assert main_part1(sample) == 5


def main_part2(vents: list) -> int:
    lines, x_max, y_max = parse(vents)
    field = np.zeros((x_max + 1, y_max + 1))
    for (x_from, y_from), (x_to, y_to) in lines:
        if x_from == x_to:
            field[x_from, y_from:y_to + 1] += 1
        elif y_from == y_to:
            field[x_from:x_to + 1, y_from] += 1
        elif y_from < y_to:
            for i in range(y_to - y_from + 1):
                field[x_from + i, y_from + i] += 1
        elif y_from > y_to:
            for i in range(y_from - y_to + 1):
                field[x_from + i, y_from - i] += 1
    return (field >= 2).sum()


def test_part2(sample):
    assert main_part2(sample) == 12


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
