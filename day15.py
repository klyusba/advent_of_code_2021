from typing import List
from pytest import fixture
from textwrap import dedent
import numpy as np


@fixture
def sample():
    return dedent("""\
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
    """).splitlines()


def read(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return f.read().splitlines()


def get_adjacent(idx, visited):
    x, y = idx
    if x != 0 and not visited[x-1, y]:
        yield x-1, y
    if x != visited.shape[0]-1 and not visited[x+1, y]:
        yield x+1, y
    if y != 0 and not visited[x, y-1]:
        yield x, y-1
    if y != visited.shape[1]-1 and not visited[x, y+1]:
        yield x, y+1


def dijkstra(weights: np.ndarray) -> np.ndarray:
    inf = max(weights.shape) ** 2 * 9
    costs = np.ones_like(weights, dtype=int) * inf
    costs[0, 0] = 0
    visited = np.zeros_like(weights, dtype=bool)
    costs_visited = costs.copy()
    i = 0
    while not visited[-1, -1]:  # we need only costs for right-bottom corner
        # TODO optimize: track nonvisited nodes with non-inf value
        curr_node = np.unravel_index(np.argmin(costs_visited, axis=None), costs.shape)
        visited[curr_node] = True
        costs_visited[curr_node] = inf
        for node in get_adjacent(curr_node, visited):
            if costs[node] > costs[curr_node] + weights[node]:
                costs[node] = costs[curr_node] + weights[node]
                costs_visited[node] = costs[node]

        i += 1
        if i % 1000 == 0:
            print(np.sum(visited) / (weights.shape[0] * weights.shape[1]))
    return costs


def main_part1(lines: List[str]) -> int:
    # You start in the top left position, your destination is the bottom right position, and you cannot move diagonally.
    levels = np.asarray([list(map(int, line)) for line in lines], dtype=int)
    costs = dijkstra(levels)
    return costs[-1, -1]


def test_part1(sample):
    assert main_part1(sample) == 40


def populate(weights: np.ndarray, k) -> np.ndarray:
    n, m = weights.shape
    levels_all = np.zeros((k*n, k*m), dtype=int)
    for i in range(k):
        part = weights + i
        part = part % 10 + part // 10
        levels_all[n * i: n * (i + 1), 0: m] = part
        for j in range(1, k):
            part = part + 1
            part = part % 10 + part // 10
            levels_all[n * i: n * (i + 1), m * j: m * (j + 1)] = part
    return levels_all


def main_part2(lines: List[str]) -> int:
    levels = np.asarray([list(map(int, line)) for line in lines], dtype=int)
    # construct bigger map:
    levels = populate(levels, k=5)
    costs = dijkstra(levels)
    return costs[-1, -1]


def test_populate():
    levels = np.asarray([[8, ]], dtype=int)
    levels = populate(levels, k=5)
    res = np.asarray([
        [8, 9, 1, 2, 3],
        [9, 1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
    ])
    assert np.all(levels == res)


def test_part2(sample):
    assert main_part2(sample) == 315


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
