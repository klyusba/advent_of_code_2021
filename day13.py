from pytest import fixture
from textwrap import dedent
import numpy as np


@fixture
def sample():
    return dedent("""\
        6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0
        
        fold along y=7
        fold along x=5
    """)


def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse(dots_folds: str):
    dots, folds = dots_folds.split('\n\n')
    dots = [
        tuple(map(int, reversed(line.split(','))))
        for line in dots.splitlines()
    ]

    def parse_fold(line):
        axis, coordinate = line[11:].split('=')
        return axis, int(coordinate)

    folds = [parse_fold(line) for line in folds.splitlines()]
    return dots, folds


def fold_up(paper, idx):
    top = paper[:idx, :]
    bottom = paper[idx+1:, :]
    return top + bottom[::-1, :]


def fold_left(paper, idx):
    left = paper[:, :idx]
    right = paper[:, idx + 1:]
    return left + right[:, ::-1]


def main_part1(dots_folds: str) -> int:
    dots, folds = parse(dots_folds)
    x_max = max(x for x, y in dots)
    y_max = max(y for x, y in dots)
    paper = np.zeros((x_max+1, y_max+1), dtype=bool)
    for x, y in dots:
        paper[x, y] = 1

    if folds[0][0] == 'y':
        paper = fold_up(paper, folds[0][1])
    else:
        paper = fold_left(paper, folds[0][1])
    return np.count_nonzero(paper)


def test_part1(sample):
    assert main_part1(sample) == 17


def main_part2(dots_folds: str) -> int:
    dots, folds = parse(dots_folds)
    x_max = max(x for x, y in dots)
    y_max = max(y for x, y in dots)
    paper = np.zeros((x_max + 1, y_max + 1), dtype=bool)
    for x, y in dots:
        paper[x, y] = 1

    for axis, idx in folds:
        if axis == 'y':
            paper = fold_up(paper, idx)
        else:
            paper = fold_left(paper, idx)

    print('')
    for line in paper:
        line = ''.join('#' if v else ' ' for v in line)
        print(line)
    return np.count_nonzero(paper)


def test_part2(sample):
    assert main_part2(sample)


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
