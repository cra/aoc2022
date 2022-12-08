import collections
import itertools
import operator
import functools
from dataclasses import dataclass

import rich

test = """
30373
25512
65332
33549
35390
""".lstrip()


@dataclass
class Tree:
    height: int
    visible: bool

    def __str__(self):
        color = ('yellow', 'blue')[self.visible]
        return f'[{color}]{self.height}[/{color}]'
    
    def __lt__(self, other):
        if isinstance(other, Tree):
            return self.height < other.height
        raise TypeError("Incompatible comparison type, can only compare trees")
    
    def __eq__(self, other):
        if isinstance(other, Tree):
            return self.height == other.height
        raise TypeError("Incompatible comparison type, can only compare trees")


def print_board(board, highlight=None):
    w, h = len(board[0]), len(board)
    for i, j in itertools.product(range(h), range(w)):
        if highlight is None:
            rich.print(str(board[i][j]), end='\n' if j == w-1 else '')

        if (i, j) == highlight:
            rich.print(f'[bright_white on black]{board[i][j].height}[/]', end='\n' if j == w-1 else '')
            continue
        print(board[i][j].height, end='\n' if j == w-1 else '')



def read_polyana(lines):
    board = collections.defaultdict(dict)
    for i, line in enumerate(lines):
        for j, tree in enumerate(line):
            board[i][j] = Tree(height=int(tree), visible=False)
    return board


def solve1(lines):
    board = read_polyana(lines)
    
    W, H = len(board[0]), len(board)
    w, h = W - 1, H - 1

    num_visible = -4 # dedup corners counter
    # all sides are visible by default
    # vertical left and right
    for i, j in zip(range(W), itertools.repeat(0)):
        board[i][j].visible = True
        board[i][w].visible = True
        num_visible += 2
    # horizontal top and bottom
    for i, j in zip(itertools.repeat(0), range(H)):
        board[i][j].visible = True
        board[h][j].visible = True
        num_visible += 2

    # walk inside
    for i, j in itertools.product(range(1, h), range(1, w)):
        current = board[i][j]
        up = [board[k][j] for k in range(i-1, -1, -1)]
        down = [board[k][j] for k in range(i+1, H)]
        left = [board[i][k] for k in range(j-1, -1, -1)]
        right = [board[i][k] for k in range(j+1, W)]
        current.visible = any(
            all(tree < current for tree in direction)
            for direction in [up, down, left, right]
        )
        num_visible += current.visible

    # print_board(board)
    return num_visible


def solve2(lines):
    board = read_polyana(lines)
    
    W, H = len(board[0]), len(board)

    score = 0
    best = None
    old_score = 0

    # walk the board
    for i, j in itertools.product(range(H), range(W)):
        current = board[i][j]
        u = [board[k][j] for k in range(i-1, -1, -1)]
        d = [board[k][j] for k in range(i+1, H)]
        l = [board[i][k] for k in range(j-1, -1, -1)]
        r = [board[i][k] for k in range(j+1, W)]

        cnt = dict(u=0, d=0, l=0, r=0)
        for eye, view in zip(cnt, (u, d, l, r)):
            for tree in view:
                if tree < current:
                    cnt[eye] += 1
                else:
                    cnt[eye] += 1
                    break
        old_score = score
        score = max(score, functools.reduce(operator.mul, cnt.values()))
        if score != old_score:
            best = (i, j)

    print(best)
    print_board(board, highlight=best)
    return score



print("Test1", solve1(test.splitlines()))
print("Puzzle1", solve1([line.strip() for line in open("puzzle_input").readlines()]))
print("Test2", solve2(test.splitlines()))
print("Puzzle2", solve2([line.strip() for line in open("puzzle_input").readlines()]))