from pytest import fixture
from typing import List, Tuple


@fixture
def sample():
    return """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


class Board:
    def __init__(self, board: List[List[int]]):
        self._board = board

    @classmethod
    def from_str(cls, board: str):
        return cls([
            list(map(int, line.split()))
            for line in board.splitlines()
        ])

    def get_score(self):
        # sum of all unmarked numbers
        return sum(
            sum(v for v in line if v != -1) for line in self._board
        )

    def _check_bingo_row(self, row: int) -> bool:
        return all(v == -1 for v in self._board[row])

    def _check_bingo_column(self, column: int) -> bool:
        return all(line[column] == -1 for line in self._board)

    def mark(self, number):
        # mark and return True if winning
        for i, line in enumerate(self._board):
            try:
                idx = line.index(number)
                line[idx] = -1
                return self._check_bingo_row(i) or self._check_bingo_column(idx)
            except ValueError:
                pass
        return False


def parse(numbers_boards: str) -> Tuple[List[int], List[Board]]:
    numbers, *boards = numbers_boards.split('\n\n')
    numbers = list(map(int, numbers.split(',')))
    boards = list(map(Board.from_str, boards))
    return numbers, boards


def main_part1(numbers_boards: str) -> int:
    numbers, boards = parse(numbers_boards)
    for number in numbers:
        for board in boards:
            if board.mark(number):
                return board.get_score() * number

    return 0


def test_part1(sample):
    assert main_part1(sample) == 4512


def main_part2(numbers_boards: str) -> int:
    numbers, boards = parse(numbers_boards)
    for number in numbers:
        for board in boards[:]:
            if board.mark(number):
                if len(boards) == 1:
                    return board.get_score() * number
                else:
                    boards.remove(board)


def test_part2(sample):
    assert main_part2(sample) == 1924


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
