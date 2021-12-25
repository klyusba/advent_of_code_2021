from pytest import fixture
from textwrap import dedent
from collections import defaultdict


@fixture
def sample():
    return dedent("""\
        NNCB

        CH -> B
        HH -> N
        CB -> H
        NH -> C
        HB -> C
        HC -> B
        HN -> C
        NN -> C
        BH -> H
        NC -> B
        NB -> B
        BN -> B
        BB -> N
        BC -> B
        CC -> N
        CN -> C
    """)


def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse(template_rules: str):
    template, rules = template_rules.split('\n\n')
    rules = dict(line.split(' -> ') for line in rules.splitlines())
    return template, rules


def polymerize(template, rules, n):
    counts = defaultdict(int)
    for a, b in zip(template, template[1:]):
        counts[a + b] += 1

    for _ in range(n):
        step = defaultdict(int)
        for pair, cnt in counts.items():
            element = rules[pair]
            step[pair[0] + element] += cnt
            step[element + pair[1]] += cnt
        counts = step

    elements = defaultdict(int)
    for pair, cnt in counts.items():
        elements[pair[0]] += cnt
        elements[pair[1]] += cnt

    # every element was counted twice, except the first and the last
    for element in elements:
        if element == template[0] or element == template[-1]:
            elements[element] += 1
        elements[element] //= 2

    return elements


def main_part1(template_rules: str) -> int:
    # after 10 steps, quantity of the most common element and subtract the quantity of the least common element?
    template, rules = parse(template_rules)
    cnt = polymerize(template, rules, 10)
    cnt = sorted(cnt.values())
    return cnt[-1] - cnt[0]


def test_part1(sample):
    assert main_part1(sample) == 1588


def main_part2(template_rules: str) -> int:
    # after 40 steps
    template, rules = parse(template_rules)
    cnt = polymerize(template, rules, 40)
    cnt = sorted(cnt.values())
    return cnt[-1] - cnt[0]


def test_part2(sample):
    assert main_part2(sample) == 2188189693529


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
