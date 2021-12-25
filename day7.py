from pytest import fixture
from typing import List
import numpy as np


@fixture
def sample():
    return [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def read(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        return list(map(int, f.readline().split(',')))


def main_part1(positions: List[int]) -> int:
    p = np.asarray(positions)
    m = np.max(p) + 1
    costs = np.zeros(m)
    for i in range(m):
        costs[i] = np.abs(p - i).sum()
    return np.min(costs)


def test_part1(sample):
    assert main_part1(sample) == 37


def main_part2(positions: List[int]) -> int:
    p = np.asarray(positions)
    m = np.max(p) + 1
    costs = np.zeros(m)
    for i in range(m):
        steps = np.abs(p - i)
        costs[i] = np.sum(steps * (steps + 1) / 2)
    return np.min(costs)


def test_part2(sample):
    assert main_part2(sample) == 168


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
