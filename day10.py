from pytest import fixture
from typing import List


@fixture
def sample():
    return """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".splitlines()


pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}


def read(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def main_part1(lines: List[str]) -> int:
    costs = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    score = 0
    for line in lines:
        stack = []
        for c in line:
            if c in pairs:
                stack.append(c)
            elif c != pairs[stack.pop()]:
                score += costs[c]
                break
    return score


def test_part1(sample):
    assert main_part1(sample) == 26397


def main_part2(lines: List[str]) -> int:
    costs = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4,
    }

    scores = []
    for line in lines:
        score = 0
        stack = []
        for c in line:
            if c in pairs:
                stack.append(c)
            elif c != pairs[stack.pop()]:
                break
        else:
            for c in reversed(stack):
                score = 5 * score + costs[c]
            scores.append(score)

    scores.sort()
    return scores[len(scores) // 2]


def test_part2(sample):
    assert main_part2(sample) == 288957


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
