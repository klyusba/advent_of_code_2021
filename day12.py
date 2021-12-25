from typing import List
from pytest import fixture
from textwrap import dedent
from collections import defaultdict

START = 'start'
END = 'end'


@fixture
def sample1():
    return dedent("""\
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
    """).splitlines()


@fixture
def sample2():
    return dedent("""\
        dc-end
        HN-start
        start-kj
        dc-start
        dc-HN
        LN-dc
        HN-end
        kj-sa
        kj-HN
        kj-dc
    """).splitlines()


@fixture
def sample3():
    return dedent("""\
        fs-end
        he-DX
        fs-he
        start-DX
        pj-DX
        end-zg
        zg-sl
        zg-pj
        pj-he
        RW-he
        fs-DX
        pj-RW
        zg-RW
        start-pj
        he-WI
        zg-he
        pj-fs
        start-RW
    """).splitlines()


def read(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def is_small(cave: str) -> bool:
    return cave == cave.lower()


def main_part1(connections: List[str]) -> int:
    # How many paths through this cave system are there that visit small caves at most once?
    caves = defaultdict(set)
    for conn in connections:
        cave1, cave2 = conn.split('-')
        if (cave2 != START) and (cave1 != END):
            caves[cave1].add(cave2)
        if (cave2 != END) and (cave1 != START):
            caves[cave2].add(cave1)

    count = 0
    stack = [[START, ], ]
    path = ['', ]
    while stack:
        while stack and not stack[-1]:
            stack.pop()
            path.pop()
        if not stack:
            break
        cave = stack[-1].pop()
        if cave == END:
            count += 1
            continue
        if is_small(cave) and cave in path:
            continue
        path.append(cave)
        next_caves = caves[cave]
        stack.append(list(next_caves))
    return count


def test_part1_1(sample1):
    assert main_part1(sample1) == 10


def test_part1_2(sample2):
    assert main_part1(sample2) == 19


def test_part1_3(sample3):
    assert main_part1(sample3) == 226


def main_part2(connections: List[str]) -> int:
    # How many paths through this cave system are there that visit small caves at most once?
    caves = defaultdict(set)
    for conn in connections:
        cave1, cave2 = conn.split('-')
        if (cave2 != START) and (cave1 != END):
            caves[cave1].add(cave2)
        if (cave2 != END) and (cave1 != START):
            caves[cave2].add(cave1)

    count = 0
    stack = [[START, ], ]
    path = ['', ]
    single_small_cave = ''
    while stack:
        while stack and not stack[-1]:
            stack.pop()
            if path.pop() == single_small_cave:
                single_small_cave = ''
        if not stack:
            break
        cave = stack[-1].pop()
        if cave == END:
            count += 1
            continue
        if is_small(cave) and cave in path:
            if single_small_cave == '':
                single_small_cave = cave
            else:
                continue

        path.append(cave)
        next_caves = caves[cave]
        stack.append(list(next_caves))
    return count


def test_part2_1(sample1):
    assert main_part2(sample1) == 36


def test_part2_2(sample2):
    assert main_part2(sample2) == 103


def test_part2_3(sample3):
    assert main_part2(sample3) == 3509


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
