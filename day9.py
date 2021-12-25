from pytest import fixture
from typing import List
import numpy as np


@fixture
def sample():
    return """\
2199943210
3987894921
9856789892
8767896789
9899965678
""".splitlines()


def read(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def main_part1(heightmap: List[str]) -> int:
    heightmap = np.asarray([list(map(int, line)) for line in heightmap])
    mask = np.ones_like(heightmap, dtype=bool)
    mask[1:, :] &= heightmap[1:, :] < heightmap[:-1, :]
    mask[:-1, :] &= heightmap[:-1, :] < heightmap[1:, :]
    mask[:, 1:] &= heightmap[:, 1:] < heightmap[:, :-1]
    mask[:, :-1] &= heightmap[:, :-1] < heightmap[:, 1:]

    return (heightmap[mask] + 1).sum()


def test_part1(sample):
    assert main_part1(sample) == 15


def main_part2(heightmap: List[str]) -> int:
    heightmap = np.asarray([list(map(int, line)) for line in heightmap])
    mask = np.ones_like(heightmap, dtype=bool)
    mask[1:, :] &= heightmap[1:, :] < heightmap[:-1, :]
    mask[:-1, :] &= heightmap[:-1, :] < heightmap[1:, :]
    mask[:, 1:] &= heightmap[:, 1:] < heightmap[:, :-1]
    mask[:, :-1] &= heightmap[:, :-1] < heightmap[:, 1:]

    basinmap = np.zeros_like(heightmap)
    basinmap[mask] = np.arange(1, np.count_nonzero(mask) + 1)

    mask = heightmap != 9
    while np.any(basinmap[mask] == 0):
        basinmap[1:, :] |= mask[1:, :] * basinmap[:-1, :]
        basinmap[:-1, :] |= mask[:-1, :] * basinmap[1:, :]
        basinmap[:, 1:] |= mask[:, 1:] * basinmap[:, :-1]
        basinmap[:, :-1] |= mask[:, :-1] * basinmap[:, 1:]

    unique, cnt = np.unique(basinmap, return_counts=True)
    cnt = np.sort(cnt[1:])
    return np.prod(cnt[-3:])


def test_part2(sample):
    assert main_part2(sample) == 1134


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
