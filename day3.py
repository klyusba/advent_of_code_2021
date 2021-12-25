from pytest import fixture


@fixture
def sample():
    return [
        '00100',
        '11110',
        '10110',
        '10111',
        '10101',
        '01111',
        '00111',
        '11100',
        '10000',
        '11001',
        '00010',
        '01010',
    ]


def read(filename: str) -> list:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def main_part1(numbers: list) -> int:
    # Each bit in the gamma rate can be determined by finding
    # the most common bit in the corresponding position of all numbers;
    # The epsilon rate is calculated in a similar way; rather than use the most common bit,
    # the least common bit from each position is used.

    cnt = [0, ] * len(numbers[0])
    for bits in numbers:
        for i, bit in enumerate(bits):
            cnt[i] += bit == '1'

    gamma = ''.join(
        '1' if 2 * v > len(numbers) else '0'
        for v in cnt
    )
    epsilon = ''.join(
        '1' if 2 * v < len(numbers) else '0'
        for v in cnt
    )
    return int(gamma, 2) * int(epsilon, 2)


def test_part1(sample):
    assert main_part1(sample) == 198


def main_part2(numbers: list) -> int:
    # oxygen generator rating
    filtered = numbers
    prefix = ''
    pos = 0
    while len(filtered) > 1:
        cnt = sum(v[pos] == '1' for v in filtered)
        if 2 * cnt >= len(filtered):
            prefix += '1'
        else:
            prefix += '0'
        filtered = [number for number in filtered if number.startswith(prefix)]
        pos += 1
    ogr = int(filtered[0], 2)

    # CO2 scrubber rating
    filtered = numbers
    prefix = ''
    pos = 0
    while len(filtered) > 1:
        cnt = sum(v[pos] == '1' for v in filtered)
        if 2 * cnt >= len(filtered):
            prefix += '0'
        else:
            prefix += '1'
        filtered = [number for number in filtered if number.startswith(prefix)]
        pos += 1
    csr = int(filtered[0], 2)

    return csr * ogr


def test_part2(sample):
    assert main_part2(sample) == 230


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
