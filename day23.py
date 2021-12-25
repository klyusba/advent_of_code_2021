from itertools import product


class Maze:
    def __init__(self, a, b, c, d):
        self.rooms = {
            'a': list(a),
            'b': list(b),
            'c': list(c),
            'd': list(d),
        }
        self.h = [None, ] * 11

        self.room_entries = {'a': 2, 'b': 4, 'c': 6, 'd': 8}
        self.room_idx = set(self.room_entries.values())
        self.step_cost = {'a': 1, 'b': 10, 'c': 100, 'd': 1000}

    def __str__(self):
        res = [''.join(agent or '.' for agent in self.h), ]
        for a, b, c, d in zip(*self.rooms.values()):
            res.append(f' #{a or "."}#{b or "."}#{c or "."}#{d or "."}#')
        return '\n'.join(res).upper()

    def __hash__(self):
        r = self.rooms
        return hash((*r['a'], *r['b'], *r['c'], *r['d'], *self.h))

    def move(self, pos_from, pos_to) -> int:
        room_name_start, pos_from = pos_from
        if room_name_start != 'h':
            agent = self.rooms[room_name_start][pos_from-1]
            self.rooms[room_name_start][pos_from - 1] = None
            h_start = self.room_entries[room_name_start]
        else:
            agent = self.h[pos_from]
            self.h[pos_from] = None
            h_start = pos_from
        assert agent is not None

        room_name_end, pos_to = pos_to
        if room_name_end != 'h':
            h_end = self.room_entries[room_name_end]
            self.rooms[room_name_end][pos_to - 1] = agent
        else:
            h_end = pos_to
            self.h[pos_to] = agent

        steps = 0
        if room_name_start != 'h':
            steps += pos_from
        steps += abs(h_end - h_start)
        if room_name_end != 'h':
            steps += pos_to
        return steps * self.step_cost[agent]

    def _reachable_pos(self, start, agent, rooms_only=False):
        room_reachable = False
        for i in reversed(range(start)):
            if self.h[i]: break
            if i in self.room_idx:
                if self.room_entries[agent] == i:
                    room_reachable = True
            elif not rooms_only:
                yield 'h', i

        for i in range(start+1, len(self.h)):
            if self.h[i]: break
            if i in self.room_idx:
                if self.room_entries[agent] == i:
                    room_reachable = True
            elif not rooms_only:
                yield 'h', i

        if not room_reachable:
            return
        # choose free bottom position in the room

        # if room empty - choose bottom square
        room = self.rooms[agent]
        if not any(room):
            yield agent, len(room)
            return

        # find free spot
        i = 0
        for i, a in enumerate(room):
            if a: break
        if i > 0 and all(a == agent for a in room[i:]):
            yield agent, i

    def get_moves(self):
        for room_name, entry in self.room_entries.items():
            room = self.rooms[room_name]
            for i, agent in enumerate(room, start=1):
                if agent:
                    if agent != room_name or any(a != room_name for a in room[i:]):
                        pos_from = room_name, i
                        yield from ((pos_from, pos_to) for pos_to in self._reachable_pos(entry, agent))
                    break

        for i, agent in enumerate(self.h):
            if agent:
                pos_from = 'h', i
                yield from ((pos_from, pos_to) for pos_to in self._reachable_pos(i, agent, rooms_only=True))

    @property
    def solved(self):
        return all(
            all(name == v for v in room)
            for name, room in self.rooms.items()
        )


def main(maze: Maze) -> int:
    moves = []
    path = []  # list[from, to, cost]
    min_cost = 100_000_000
    curr_cost = 0

    while True:
        if len(path) == len(moves):
            open_moves = maze.get_moves()
        else:
            open_moves = moves.pop()

        try:
            pos_from, pos_to = next(open_moves)
            cost = maze.move(pos_from, pos_to)
            curr_cost += cost
            moves.append(open_moves)
            if curr_cost >= min_cost:
                # no more steps in that way
                maze.move(pos_to, pos_from)
                curr_cost -= cost
            else:
                path.append((pos_from, pos_to, cost))
        except StopIteration:
            if curr_cost < min_cost and maze.solved:
                min_cost = curr_cost
                print(min_cost, path)

            # revert last move
            if not path: return min_cost
            pos_from, pos_to, cost = path.pop()
            maze.move(pos_to, pos_from)
            curr_cost -= cost


def test_cost():
    print('')
    maze = Maze('ba', 'cd', 'bc', 'da')
    print(maze)
    print('')
    assert maze.move(('c', 1), ('h', 3)) == 40
    print(maze)
    print('')
    assert maze.move(('b', 1), ('c', 1)) == 400
    print(maze)
    print('')
    assert maze.move(('b', 2), ('h', 5)) == 3000
    assert maze.move(('h', 3), ('b', 2)) == 30
    print(maze)
    print('')
    assert maze.move(('a', 1), ('b', 1)) == 40
    print(maze)
    print('')
    assert maze.move(('d', 1), ('h', 7)) == 2000
    assert maze.move(('d', 2), ('h', 9)) == 3
    print(maze)
    print('')
    assert maze.move(('h', 7), ('d', 2)) == 3000
    assert maze.move(('h', 5), ('d', 1)) == 4000
    print(maze)
    print('')
    assert maze.move(('h', 9), ('a', 1)) == 8
    print(maze)
    print('')
    assert maze.solved


def test_get_moves():
    maze = Maze('ba', 'cd', 'bc', 'da')
    assert set(maze.get_moves()) == set(((room, 1), ('h', i)) for room, i in product('abcd', [0, 1, 3, 5, 7, 9, 10]))


def test_get_moves_solved():
    maze = Maze('aa', 'bb', 'cc', 'dd')
    assert set(maze.get_moves()) == set()


def test_main():
    maze = Maze('aa', 'bb', 'cd', 'cd')
    assert main(maze) == 6100


def test_main_part1():
    # 62 sec
    maze = Maze('ba', 'cd', 'bc', 'da')
    assert main(maze) == 12521


def test_main_part2():
    # 500+ secs
    maze = Maze('bdda', 'ccbd', 'bbac', 'daca')
    assert main(maze) == 44169


if __name__ == "__main__":
    # part1
    input_data = Maze('bc', 'ba', 'da', 'dc')
    main(input_data)  # 10607

    # part2
    input_data = Maze('bddc', 'bcba', 'dbaa', 'dacc')
    main(input_data)  # 59071
