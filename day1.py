from pytest import fixture


@fixture
def sample():
    return [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def read(filename: str) -> list:
    with open(filename, 'r') as f:
        return [int(line) for line in f]


def main_part1(measurements: list) -> int:
    # Count the number of times a depth measurement increases from the previous measurement.
    # (There is no measurement before the first measurement.)
    return sum(
        value > prev
        for prev, value in zip(measurements, measurements[1:])
    )


def test_part1(sample):
    assert main_part1(sample) == 7


def main_part2(measurements: list) -> int:
    # Instead, consider sums of a three-measurement sliding window.
    moving_sum = [
        v1 + v2 + v3
        for v1, v2, v3 in zip(measurements, measurements[1:], measurements[2:])
    ]
    return sum(
        value > prev
        for prev, value in zip(moving_sum, moving_sum[1:])
    )


def test_part2(sample):
    assert main_part2(sample) == 5


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
