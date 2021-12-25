from pytest import fixture
from typing import List


@fixture
def sample():
    return [3, 4, 3, 1, 2]


def read(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        return list(map(int, f.readline().split(',')))


def lanternfish_sim(ages, days=80, days_to_double=6, days_for_new=8):
    unique_ages = [0] * (days_for_new + 1)
    for v in ages:
        unique_ages[v] += 1

    for _ in range(days):
        new = unique_ages.pop(0)
        unique_ages[days_to_double] += new
        unique_ages.append(new)
    return sum(unique_ages)


def main_part1(ages: List[int]) -> int:
    return lanternfish_sim(ages, 80)


def test_part1(sample):
    assert main_part1(sample) == 5934


def main_part2(ages: List[int]) -> int:
    return lanternfish_sim(ages, 256)


def test_part2(sample):
    assert main_part2(sample) == 26984457539


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
