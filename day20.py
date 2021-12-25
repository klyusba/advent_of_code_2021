from pytest import fixture
import numpy as np
from scipy.signal import convolve2d


@fixture
def sample():
    return """\
        ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##\
        #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###\
        .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.\
        .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....\
        .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..\
        ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....\
        ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
        
        #..#.
        #....
        ##..#
        ..#..
        ..###
    """.replace(" ", "")


def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse(alg_image: str):
    alg, _, *image = alg_image.splitlines()
    alg = np.asarray([c == '#' for c in alg], dtype=bool)
    image = np.asarray([
        list(map(lambda x: x == '#', line))
        for line in image
    ], dtype=bool)

    assert len(alg) == 512
    assert image.shape[0] == image.shape[1]
    return alg, image


kernel = np.asarray([
    [ 1,   2,   4],
    [ 8,  16,  32],
    [64, 128, 256],
], dtype=int)


def enhance(image, alg, env):
    conv = convolve2d(image, kernel, fillvalue=env)
    enhanced = np.resize(alg[conv.flatten()], conv.shape)
    env = 1 * alg[[0, 511]][env]
    return enhanced, env


def main_part1(alg_image: str) -> int:
    alg, image = parse(alg_image)
    env = 0
    for _ in range(2):
        image, env = enhance(image, alg, env)
    return image.sum()


def test_part1(sample):
    assert main_part1(sample) == 35


def main_part2(alg_image: str) -> int:
    alg, image = parse(alg_image)
    env = 0
    for _ in range(50):
        image, env = enhance(image, alg, env)
    return image.sum()


def test_part2(sample):
    assert main_part2(sample) == 3351


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
