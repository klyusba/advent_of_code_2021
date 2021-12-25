from pytest import fixture
from textwrap import dedent


@fixture
def sample():
    return read('day22.example')


class Cuboid:
    def __init__(self, x_from, x_to, y_from, y_to, z_from, z_to, sign=1):
        self.x_from = x_from
        self.x_to = x_to
        self.y_from = y_from
        self.y_to = y_to
        self.z_from = z_from
        self.z_to = z_to
        self.sign = sign

    @classmethod
    def from_str(cls, s):
        cmd, s = s.split()
        ranges = []
        for range_def in s.split(','):
            range_def = range_def[2:]
            ranges.extend(map(int, range_def.split('..')))

        return cls(*ranges, sign=1 if cmd == 'on' else -1)

    @property
    def volume(self):
        return (self.x_to - self.x_from + 1) * (self.y_to - self.y_from + 1) * (self.z_to - self.z_from + 1) * self.sign

    def __and__(self, other):
        x_from, x_to = max(self.x_from, other.x_from), min(self.x_to, other.x_to)
        if x_from > x_to:
            return None

        y_from, y_to = max(self.y_from, other.y_from), min(self.y_to, other.y_to)
        if y_from > y_to:
            return None

        z_from, z_to = max(self.z_from, other.z_from), min(self.z_to, other.z_to)
        if z_from > z_to:
            return None

        return Cuboid(x_from, x_to, y_from, y_to, z_from, z_to, -other.sign)

    def __contains__(self, other):
        return self.x_from <= other.x_from \
            and self.x_to >= other.x_to \
            and self.y_from <= other.y_from \
            and self.y_to >= other.y_to \
            and self.z_from <= other.z_from \
            and self.z_to >= other.z_to

    def __str__(self):
        return f'{"on" if self.sign == 1 else "off"} {self.x_from}..{self.x_to},{self.y_from}..{self.y_to},{self.z_from}..{self.z_to}'


class Grid:
    def __init__(self):
        self._cuboids = []

    def __iter__(self):
        return iter(self._cuboids)

    def add(self, cuboid: Cuboid):
        new = []
        for c in self._cuboids:
            if c not in cuboid:
                new.append(c)
                intersection = cuboid & c  # cuboid on top of c
                if intersection is not None:
                    new.append(intersection)
        if cuboid.sign == 1:
            new.append(cuboid)
        self._cuboids = new

    @property
    def volume(self):
        return sum(c.volume for c in self._cuboids)


def read(filename: str) -> list:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def parse(coordinates, box=None):
    grid = Grid()
    for line in coordinates:
        c = Cuboid.from_str(line)
        if box is None or c in box:
            grid.add(c)
    return grid


def main_part1(coordinates: list) -> int:
    box = Cuboid(-50, 50, -50, 50, -50, 50)
    region = parse(coordinates, box)
    return region.volume


def test_parse1():
    data = dedent("""\
        on x=10..12,y=10..12,z=10..12
        on x=11..13,y=11..13,z=11..13
        off x=9..11,y=9..11,z=9..11
        on x=10..10,y=10..10,z=10..10
    """).splitlines()

    grid = parse(data[:1])
    assert grid.volume == 27
    grid = parse(data[:2])
    assert grid.volume == 27 + 19
    grid = parse(data[:3])
    assert grid.volume == 27 + 19 - 8
    grid = parse(data)
    assert grid.volume == 39


def test_main_part1(sample):
    assert main_part1(sample) == 590784


def main_part2(coordinates: list) -> int:
    region = parse(coordinates)
    return region.volume


def test_main_part2(sample):
    assert main_part2(sample) == 2758514936282235


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
