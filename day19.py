import numpy as np
from textwrap import dedent
from itertools import product, chain, combinations, starmap

# By establishing 12 common beacons, you can precisely determine where
# the scanners are relative to each other, allowing you to reconstruct
# the beacon map one scanner at a time.
THRESHOLD = 12
# Each scanner is capable of detecting all beacons in a large cube centered
# on the scanner; beacons that are at most 1000 units away from the scanner
# in each of the three axes (x, y, and z) have their precise position determined
# relative to the scanner.
MAX_RANGE = 1000

# rotation = axis change


class MatchesNotEnough(Exception):
    pass


def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse(scanner_views: str) -> list:
    res = []
    for scanner in scanner_views.split('\n\n'):
        scanner = [
            list(map(int, line.split(',')))
            for line in scanner.splitlines()[1:]  # skip header
        ]
        res.append(np.asarray(scanner))
    return res


def align_views(base: np.ndarray, other: np.ndarray, threshold=THRESHOLD) -> (np.ndarray, np.ndarray):
    # rotate and translate other into coordinate system of base

    shifts = []
    for axis in range(3):
        axis_shifts = []
        x = base[:, axis]
        for i, dir in product(range(3), [1, -1]):
            v = dir * other[:, i]
            un, cnt = np.unique(x[:, np.newaxis] - v, return_counts=True)
            for shift in un[cnt >= threshold]:
                axis_shifts.append((i, dir, shift))
        shifts.append(axis_shifts)

    def hash(x):
        return x[:, 0] + x[:, 1] * 10_000 + x[:, 2] * 100_000_000

    x = hash(base)
    for (idx1, dir1, shift1), (idx2, dir2, shift2), (idx3, dir3, shift3) in product(*shifts):
        if idx1 == idx2 or idx1 == idx3 or idx2 == idx3:
            continue
        shift = np.asarray([shift1, shift2, shift3])
        new_view = other[:, [idx1, idx2, idx3]] * [dir1, dir2, dir3] + shift
        v = hash(new_view)
        v = x[:, np.newaxis] - v
        if (v == 0).sum() >= threshold:
            return new_view, shift
    else:
        raise MatchesNotEnough()


def main(scanner_views: str) -> (int, int):
    scanner_views = parse(scanner_views)
    aligned = [scanner_views.pop(0), ]
    scanners = [np.zeros(3), ]
    idx = 0
    while scanner_views:
        not_matched = []
        aligned_view = aligned[idx]
        for view in scanner_views:
            try:
                new_view, shift = align_views(aligned_view, view)
                aligned.append(new_view)
                scanners.append(shift)
            except MatchesNotEnough:
                not_matched.append(view)
        scanner_views = not_matched
        idx += 1

    # part1 - count unique beacons
    unique = set()
    for beacon in chain.from_iterable(aligned):
        unique.add(tuple(beacon))
    result_for_part1 = len(unique)

    # part2 - max l1 between scanners:
    def l1_norm(v1, v2):
        return np.sum(np.abs(v1 - v2))

    result_for_part2 = max(starmap(l1_norm, combinations(scanners, 2)))
    return result_for_part1, result_for_part2


def test_parse():
    data = dedent("""\
        --- scanner 0 ---
        0,2,0
        4,1,0
        3,3,0
        
        --- scanner 1 ---
        -1,-1,0
        -5,0,0
        -2,1,0
    """)
    res = parse(data)
    assert len(res) == 2
    assert res[0].shape == (3, 3)
    assert res[1].shape == (3, 3)

    new_view = align_views(res[0], res[1], 3)
    assert np.all(np.sort(new_view, axis=None) == np.sort(res[0], axis=None))


def test_main():
    input_data = read('day19.example')
    assert main(input_data) == (79, 3621)


if __name__ == "__main__":
    input_data = read('input')
    print(main(input_data))
