from pytest import fixture
from textwrap import dedent
import numpy as np

EAST_HERD = 1
SOUTH_HERD = 2


@fixture
def sample():
    return dedent("""\
        v...>>.vv>
        .vv>>.vv..
        >>.>v>...v
        >>v>>.>.v.
        v>v.vv.v..
        >.>>..v...
        .vv..>.>v.
        v.v..>>v.v
        ....v..v.>
    """)


def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse(cucumbers: str) -> np.ndarray:
    v = {'.': 0, '>': EAST_HERD, 'v': SOUTH_HERD}
    return np.asarray([
        list(map(lambda x: v[x], line))
        for line in cucumbers.splitlines()
    ], dtype=int)


def to_str(cucumbers: np.ndarray) -> str:
    v = {0: '.', EAST_HERD: '>', SOUTH_HERD: 'v'}
    return '\n'.join(
        ''.join(v[i] for i in row)
        for row in cucumbers
    )


def move(cucumbers) -> int:
    n, m = cucumbers.shape
    res = 0

    # first move the east-facing herd
    can_move = cucumbers == EAST_HERD
    can_move[:, :-1] &= cucumbers[:, 1:] == 0
    can_move[:, -1] &= cucumbers[:, 0] == 0
    i, j = np.where(can_move)
    if len(i):
        cucumbers[i, j] = 0
        cucumbers[i, (j+1) % m] = EAST_HERD
        res += len(i)

    # then move the south-facing herd
    can_move = cucumbers == SOUTH_HERD
    can_move[:-1, :] &= cucumbers[1:, :] == 0
    can_move[-1, :] &= cucumbers[0, :] == 0
    i, j = np.where(can_move)
    if len(i):
        cucumbers[i, j] = 0
        cucumbers[(i+1) % n, j] = SOUTH_HERD
        res += len(i)
    return res


def main_part1(cucumbers: str) -> int:
    # What is the first step on which no sea cucumbers move?
    cucumbers = parse(cucumbers)
    step = 1
    while move(cucumbers):
        step += 1
    return step


def test_move():
    c = parse(dedent("""\
        ..........
        .>v....v..
        .......>..
        ..........
    """))
    assert move(c) == 3

    res = parse(dedent("""\
        ..........
        .>........
        ..v....v>.
        ..........
    """))
    assert np.all(c == res)


def test_move2(sample):
    c = parse(sample)
    move(c)
    res = parse(dedent("""\
        ....>.>v.>
        v.v>.>v.v.
        >v>>..>v..
        >>v>v>.>.v
        .>v.v...v.
        v>>.>vvv..
        ..v...>>..
        vv...>>vv.
        >.v.v..v.v
    """))
    assert np.all(c == res)

    move(c)
    res = parse(dedent("""\
        >.v.v>>..v
        v.v.>>vv..
        >v>.>.>.v.
        >>v>v.>v>.
        .>..v....v
        .>v>>.v.v.
        v....v>v>.
        .vv..>>v..
        v>.....vv.
    """))
    assert np.all(c == res)


def test_main_part1(sample):
    assert main_part1(sample) == 58


def test_main():
    input_data = read('input')
    assert main_part1(input_data) == 534


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
