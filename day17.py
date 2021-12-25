from pytest import fixture
from itertools import product
import numpy as np


@fixture
def sample():
    return "target area: x=20..30, y=-10..-5"


@fixture
def puzzle_input():
    return "target area: x=265..287, y=-103..-58"


def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.readline()


def parse(area: str):
    area = area[13:]

    def _parse(s):
        _, s = s.split('=')
        return tuple(map(int, s.split('..')))
    return tuple(map(_parse, area.split(',')))


def main_part1(area: str) -> int:
    # What is the highest y position it reaches on this trajectory?
    # motion law:
    #     x(0), y(0) = 0, 0
    #     x <- x + vx
    #     y <- y + vy
    #     vx <- vx - sign(vx)
    #     vy <- vy - 1
    # y(i) = i * (2 * vy0 - i + 1) / 2
    # x_max = v0 * (v0 + 1) / 2
    (x_from, x_to), (y_from, y_to) = parse(area)
    v = -y_from - 1
    return v * (v + 1) / 2


def test_part1(sample):
    assert main_part1(sample) == 45


def sim(vx, vy, x_from, x_to, y_from, y_to):
    # TODO calc enough steps instead of hard coded amount 1000
    vx = np.maximum(vx - np.arange(1000), 0)
    vy = vy - np.arange(1000)
    x = np.cumsum(vx)
    y = np.cumsum(vy)
    return np.any((x >= x_from) & (x <= x_to) & (y >= y_from) & (y <= y_to))


def main_part2(area: str) -> int:
    # How many distinct initial velocity values cause the probe to be within the target area after any step?
    (x_from, x_to), (y_from, y_to) = parse(area)
    vx_min = int((2 * x_from) ** 0.5) - 1
    vx_max = x_to
    vy_min = y_from
    vy_max = -y_from

    cnt = 0
    for vx, vy in product(range(vx_min, vx_max+1), range(vy_min, vy_max+1)):
        cnt += sim(vx, vy, x_from, x_to, y_from, y_to)
    return cnt


def test_part2(sample):
    assert main_part2(sample) == 112


def test_part2_true(puzzle_input):
    assert main_part2(puzzle_input) == 1770


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
