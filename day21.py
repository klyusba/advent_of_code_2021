from itertools import cycle
from collections import defaultdict


def main_part1(start_pos: list) -> int:
    score = [0, ] * len(start_pos)
    dice = cycle(range(1, 101))
    pos = start_pos.copy()
    cnt = 0
    while max(score) < 1000:
        for i, p in enumerate(pos):
            step = next(dice) + next(dice) + next(dice)
            p = (p + step - 1) % 10 + 1

            pos[i] = p
            score[i] += p

            cnt += 3

            if score[i] >= 1000:
                break
    return cnt * min(score)


def test_play():
    assert main_part1([4, 8]) == 739785


d3_3 = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


def make_move(outcomes: dict) -> dict:
    res = defaultdict(int)
    for (score, pos), outcome in outcomes.items():
        for step, odds in d3_3.items():
            p = (pos + step - 1) % 10 + 1
            res[score + p, p] += outcome * odds
    return res


def reduce(outcomes: dict) -> int:
    wins = 0
    for score, pos in outcomes.copy().keys():
        if score >= 21:
            wins += outcomes.pop((score, pos))
    return wins


def total(outcomes: dict) -> int:
    return sum(outcomes.values())


def main_part2(start_pos: list) -> int:
    outcomes1 = {(0, start_pos[0]): 1}  # score, pos -> counts
    outcomes2 = {(0, start_pos[1]): 1}  # score, pos -> counts
    wins1, wins2 = 0, 0

    while outcomes1 and outcomes2:
        outcomes1 = make_move(outcomes1)
        wins1 += reduce(outcomes1) * total(outcomes2)

        outcomes2 = make_move(outcomes2)
        wins2 += reduce(outcomes2) * total(outcomes1)

    return max(wins1, wins2)


def test_play2():
    assert main_part2([4, 8]) == 444356092776315


if __name__ == "__main__":
    input_data = [2, 1]
    print(main_part1(input_data))
    print(main_part2(input_data))
