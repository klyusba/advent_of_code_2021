from pytest import fixture
from typing import List, Dict


@fixture
def sample():
    return """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".splitlines()


def read(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def main_part1(observations: List[str]) -> int:
    res = 0
    for entry in observations:
        patterns, digits = map(str.split, entry.split(' | '))
        res += sum(
            1
            for digit in digits
            if len(digit) in {2, 3, 4, 7}
        )
    return res


def test_part1(sample):
    assert main_part1(sample) == 26


def decode(patters: List[frozenset]) -> Dict[frozenset, str]:
    one = next(p for p in patters if len(p) == 2)
    patters.remove(one)

    seven = next(p for p in patters if len(p) == 3)
    patters.remove(seven)

    four = next(p for p in patters if len(p) == 4)
    patters.remove(four)

    eight = next(p for p in patters if len(p) == 7)
    patters.remove(eight)

    six = next(p for p in patters if len(p - one) == 5)
    patters.remove(six)

    three = next(p for p in patters if len(p - one) == 3)
    patters.remove(three)

    nine = next(p for p in patters if three | four == p)
    patters.remove(nine)

    zero = next(p for p in patters if len(eight - p) == 1)
    patters.remove(zero)

    five = next(p for p in patters if len(six - p) == 1)
    patters.remove(five)

    two = patters[0]

    return {
        one: '1',
        two: '2',
        three: '3',
        four: '4',
        five: '5',
        six: '6',
        seven: '7',
        eight: '8',
        nine: '9',
        zero: '0',
    }


def main_part2(observations: List[str]) -> int:
    res = 0
    for entry in observations:
        patterns, digits = map(str.split, entry.split(' | '))
        patterns = [frozenset(p) for p in patterns]
        digits = [frozenset(d) for d in digits]

        matching = decode(patterns)
        number = ''.join(matching[d] for d in digits)
        res += int(number)
    return res


def test_part2(sample):
    assert main_part2(sample) == 61229


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
