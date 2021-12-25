from pytest import fixture
from typing import List
import numpy as np
from scipy.signal import convolve2d


@fixture
def sample():
    return """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".splitlines()


def read(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def main_part1(lines: List[str]) -> int:
    levels = np.asarray([list(map(int, line)) for line in lines])
    total_flashes = 0
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0

    for _ in range(100):
        levels += 1

        flashes = np.zeros_like(levels)
        flashes_sum = 0
        while True:
            flashes = convolve2d((levels + flashes) > 9, kernel, mode='same')
            if flashes_sum == np.sum(flashes):
                break
            flashes_sum = np.sum(flashes)

        levels += flashes
        total_flashes += np.count_nonzero(levels > 9)
        levels[levels > 9] = 0

    return total_flashes


def test_part1(sample):
    assert main_part1(sample) == 1656


def main_part2(lines: List[str]) -> int:
    levels = np.asarray([list(map(int, line)) for line in lines])
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0

    for step in range(1000):
        levels += 1

        flashes = np.zeros_like(levels)
        flashes_sum = 0
        while True:
            flashes = convolve2d((levels + flashes) > 9, kernel, mode='same')
            if flashes_sum == np.sum(flashes):
                break
            flashes_sum = np.sum(flashes)

        levels += flashes
        levels[levels > 9] = 0
        if np.count_nonzero(levels) == 0:
            return step + 1

    return 0


def test_part2(sample):
    assert main_part2(sample) == 195


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
