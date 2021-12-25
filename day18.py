import numpy as np
from functools import reduce
from operator import add
from itertools import permutations


class SnailfishNumber:

    def __init__(self, levels: np.ndarray, values: np.ndarray):
        self._levels = levels
        self._values = values

    @classmethod
    def from_str(cls, n: str):
        pos = 0
        lvl = 0

        levels = np.zeros(len(n), dtype=int)
        values = np.zeros(len(n), dtype=int)
        for c in n:
            if c == '[':
                lvl += 1
            elif c == ']':
                lvl -= 1
            elif c == ',':
                pass
            else:
                values[pos] = int(c)
                levels[pos] = lvl
                pos += 1
        return cls(levels[:pos], values[:pos])

    def reduce(self):
        while self.explode() or self.split():
            ...

    def explode(self):
        idx = np.argmax(self._levels >= 5)
        if self._levels[idx] < 5:
            return False

        self._levels[idx: idx+2] -= 1
        if idx > 0:
            self._values[idx-1] += self._values[idx]
        if idx + 2 < len(self._values):
            self._values[idx + 2] += self._values[idx + 1]
        self._values[idx+1] = 0
        self._values = np.concatenate((self._values[:idx], self._values[idx + 1:]))
        self._levels = np.concatenate((self._levels[:idx], self._levels[idx + 1:]))
        return True

    def split(self):
        idx = np.argmax(self._values >= 10)
        if self._values[idx] < 10:
            return False
        v = self._values[idx]
        v = v // 2, v - v // 2
        lvl = self._levels[idx]

        self._values = np.concatenate((self._values[:idx], v, self._values[idx + 1:]))
        self._levels = np.concatenate((self._levels[:idx], (lvl+1, lvl+1), self._levels[idx + 1:]))
        return True

    def __add__(self, other):
        v = np.concatenate((self._values, other._values))
        lvl = np.concatenate((self._levels, other._levels))
        res = SnailfishNumber(lvl + 1, v)
        res.reduce()
        return res

    def __eq__(self, other):
        return np.all(self._values == other._values) and np.all(self._levels == other._levels)

    @property
    def magnitude(self):
        stack = [-1, ] * 5  # we have zeros in values
        for lvl, value in zip(self._levels, self._values):
            while stack[lvl] != -1:
                v1, stack[lvl] = stack[lvl], -1
                value = v1 * 3 + 2 * value
                lvl -= 1
            stack[lvl] = value
        return stack[0]


def test_explode1():
    n = SnailfishNumber.from_str("[[[[[9,8],1],2],3],4]")
    n.explode()
    assert n == SnailfishNumber.from_str("[[[[0,9],2],3],4]")


def test_explode2():
    n = SnailfishNumber.from_str("[7,[6,[5,[4,[3,2]]]]]")
    n.explode()
    assert n == SnailfishNumber.from_str("[7,[6,[5,[7,0]]]]")


def test_explode3():
    n = SnailfishNumber.from_str("[[6,[5,[4,[3,2]]]],1]")
    n.explode()
    assert n == SnailfishNumber.from_str("[[6,[5,[7,0]]],3]")


def test_explode4():
    n = SnailfishNumber.from_str("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    n.explode()
    assert n == SnailfishNumber.from_str("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")


def test_explode5():
    n = SnailfishNumber.from_str("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    n.explode()
    assert n == SnailfishNumber.from_str("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")


def test_split1():
    n = SnailfishNumber.from_str("[1,1]")
    n._values[0] = 11
    n.split()
    assert n == SnailfishNumber.from_str("[[5,6],1]")


def test_split2():
    n = SnailfishNumber.from_str("[1,1]")
    n._values[0] = 12
    n.split()
    assert n == SnailfishNumber.from_str("[[6,6],1]")


def test_add():
    n1 = SnailfishNumber.from_str("[[[[4,3],4],4],[7,[[8,4],9]]]")
    n2 = SnailfishNumber.from_str("[1,1]")
    n = n1 + n2
    assert n == SnailfishNumber.from_str("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")


def test_sum_list1():
    lst = map(SnailfishNumber.from_str, [
        "[1,1]",
        "[2,2]",
        "[3,3]",
        "[4,4]",
    ])
    assert reduce(add, lst) == SnailfishNumber.from_str("[[[[1,1],[2,2]],[3,3]],[4,4]]")


def test_sum_list2():
    lst = map(SnailfishNumber.from_str, [
        "[1,1]",
        "[2,2]",
        "[3,3]",
        "[4,4]",
        "[5,5]",
    ])
    assert reduce(add, lst) == SnailfishNumber.from_str("[[[[3,0],[5,3]],[4,4]],[5,5]]")


def test_sum_list3():
    lst = map(SnailfishNumber.from_str, [
        "[1,1]",
        "[2,2]",
        "[3,3]",
        "[4,4]",
        "[5,5]",
        "[6,6]",
    ])
    assert reduce(add, lst) == SnailfishNumber.from_str("[[[[5,0],[7,4]],[5,5]],[6,6]]")


def test_sum_list4():
    lst = map(SnailfishNumber.from_str, [
        "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
        "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
        "[7,[5,[[3,8],[1,4]]]]",
        "[[2,[2,2]],[8,[8,1]]]",
        "[2,9]",
        "[1,[[[9,3],9],[[9,0],[0,7]]]]",
        "[[[5,[7,4]],7],1]",
        "[[[[4,2],2],6],[8,7]]",
    ])
    assert reduce(add, lst) == SnailfishNumber.from_str("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")


def test_sum_list5():
    lst = map(SnailfishNumber.from_str, [
        "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
        "[[[5,[2,8]],4],[5,[[9,9],0]]]",
        "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
        "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
        "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
        "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
        "[[[[5,4],[7,7]],8],[[8,3],8]]",
        "[[9,3],[[9,9],[6,[4,9]]]]",
        "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
        "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
    ])
    res = reduce(add, lst)
    assert res == SnailfishNumber.from_str("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
    assert res.magnitude == 4140


def test_magnitude1():
    assert SnailfishNumber.from_str("[9,1]").magnitude == 29


def test_magnitude2():
    assert SnailfishNumber.from_str("[1,9]").magnitude == 21


def test_magnitude3():
    assert SnailfishNumber.from_str("[[9,1],[1,9]]").magnitude == 129


def test_magnitude4():
    assert SnailfishNumber.from_str("[[1,2],[[3,4],5]]").magnitude == 143


def test_magnitude5():
    assert SnailfishNumber.from_str("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude == 1384


def test_magnitude6():
    assert SnailfishNumber.from_str("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude == 445


def test_magnitude7():
    assert SnailfishNumber.from_str("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude == 791


def test_magnitude8():
    assert SnailfishNumber.from_str("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude == 1137


def test_magnitude9():
    assert SnailfishNumber.from_str("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude == 3488


def read(filename: str) -> list:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def main_part1(nums) -> int:
    lst = map(SnailfishNumber.from_str, nums)
    res = reduce(add, lst)
    return res.magnitude


def main_part2(nums) -> int:
    lst = map(SnailfishNumber.from_str, nums)
    return max(
        (n1 + n2).magnitude
        for n1, n2 in permutations(lst, 2)
    )


def test_main_part2():
    lst = map(SnailfishNumber.from_str, [
        "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
        "[[[5,[2,8]],4],[5,[[9,9],0]]]",
        "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
        "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
        "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
        "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
        "[[[[5,4],[7,7]],8],[[8,3],8]]",
        "[[9,3],[[9,9],[6,[4,9]]]]",
        "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
        "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
    ])
    res = max(
        (n1 + n2).magnitude
        for n1, n2 in permutations(lst, 2)
    )
    assert res == 3993


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
