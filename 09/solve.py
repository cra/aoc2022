from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set


test = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".lstrip()


def x(point) -> int:
    return int(point.real)


def y(point) -> int:
    return int(point.imag)


def variants(Ax, Ay, Bx, By):
    yield Ax == Bx and Ay == By
    # ... ...
    # .AB BA.
    # ... ...
    yield Ax in (Bx-1, Bx+1) and Ay == By
    # ... .B.
    # .A. .A.
    # .B. ...
    yield Ay in (By-1, By+1) and Ax == Bx
    # ... ..B ... B..
    # .A. .A. .A. .A.
    # ..B ... B.. ...
    yield Ay in (By-1, By+1) and Ax in (Bx-1, Bx+1)


def update(head, tail):
    if any(variants(x(head), y(head), x(tail), y(tail))):
        return tail  # they touch
    distance = abs(x(head) - x(tail)) + abs(y(head) - y(tail))
    assert distance <= 4  # safety check
    if y(head) == y(tail):
        tail += (-1, 1)[x(head) > x(tail)]
    elif x(head) == x(tail):
        tail += (-1j, 1j)[y(head) > y(tail)]
    elif distance == 3:
        # small diagonal shift
        # .H.    .H.
        # ... -> .T.
        # T..    ...
        v = (-1, 1)[y(head) > y(tail)]
        h = (-1, 1)[x(head) > x(tail)]
        tail += h + v*1j
    else:
        # longest stretch
        if x(head) == x(tail) + 2 and y(head) == y(tail) + 2:
            # ..H    ..H
            # ... -> .T.
            # T..    ...
            tail += 1 + 1j
        elif x(head) == x(tail) + 2 and y(head) == y(tail) - 2:
            # T..    ...
            # ... -> .T.
            # ..H    ..H
            tail += 1 - 1j
        elif x(head) == x(tail) - 2 and y(head) == y(tail) - 2:
            # ..T    ...
            # ... -> .T.
            # H..    H..
            tail += -1 - 1j
        elif x(head) == x(tail) - 2 and y(head) == y(tail) + 2:
            # H..    H..
            # ... -> .T.
            # ..T    ...
            tail += -1 - 1j

    assert any(variants(x(head), y(head), x(tail), y(tail)))

    return tail


def solve1(lines):
    head = 0 + 0j
    tail = 0 + 0j
    seen = {}
    delta = {'U': 1j, 'D': -1j, 'L': -1, 'R': 1}
    for instr in lines:
        d, c = instr.split()
        for _ in range(int(c)):
            head += delta[d]
            tail = update(head, tail)
            if tail not in seen:
                seen[tail] = True
            ## print(head, tail)
    return len(seen)

## OUCH

test2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".lstrip()


@dataclass
class Rope:
    x: int
    y: int
    parent: Optional[Rope] = None
    child: Optional[Rope] = None

    @property
    def real(self):
        return self.x

    @property
    def imag(self):
        return self.y

    @property
    def point(self) -> complex:
        return self.x + self.y*1j

    def __str__(self):
        return str(self.point)

    def __iadd__(self, other):
        assert isinstance(other, complex)
        self.x += other.real
        self.y += other.imag
        return self

    def __add__(self, other):
        assert isinstance(other, (complex, int))
        return Rope(self.x + other.real, self.y + other.imag)
    
    def __sub__(self, other):
        assert isinstance(other, (complex, int))
        return Rope(self.x - other.real, self.y - other.imag)

    @property
    def str_from_here(self):
        cur = self
        positions = []
        while cur.child is not None:
            positions.append(str(cur))
            cur = cur.child
        s = '->'.join(positions)
        return s

    @property
    def last_position(self):
        cur = self
        while cur.child is not None:
            cur = cur.child
        return cur.point


def solve2(lines):
    head = Rope(0, 0, None)
    cur = head
    for _ in range(10):
        child = Rope(0, 0, cur)
        cur.child = child
        cur = child
    
    seen = {}
    delta = {'U': 1j, 'D': -1j, 'L': -1+0j, 'R': 1+0j}
    for instr in lines:
        print("======", instr)
        d, c = instr.split()
        for _ in range(int(c)):
            head += delta[d]
            cur = head
            while cur.child is not None:
                tail = update(cur.point, cur.child.point)
                cur.child.x, cur.child.y = x(tail), y(tail)
                cur = cur.child
            print("->", cur.point)
            if cur.point not in seen:
                seen[cur.point] = True
            print(head.str_from_here)
            print("-->", head.last_position)
    return len(seen)


print("Test1", solve1(test.splitlines()))
print("Puzzle1", solve1(open("puzzle_input").readlines()))
print("Test2-1", solve2(test.splitlines()))
print("Test2-2", solve2(test2.splitlines()))