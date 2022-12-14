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
            tail += -1 + 1j

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



def solve2(lines):    
    seen = {}
    delta = {'U': 1j, 'D': -1j, 'L': -1+0j, 'R': 1+0j}
    uzly = [0+0j]*10
    for instr in lines:
        print(instr)
        d, c = instr.split()
        for _ in range(int(c)):
            uzly[0] += delta[d]
            for i in range(1, 10):
                tail = update(head=uzly[i-1], tail=uzly[i])
                uzly[i] = tail
            if (cur := uzly[-1]) not in seen:
                seen[cur] = True
            print('->'.join(map(str, uzly)))
    return len(seen)


print("Test1", solve1(test.splitlines()))
print("Puzzle1", solve1(open("puzzle_input").readlines()))
print("Test2-1", solve2(test.splitlines()))
print("Test2-2", solve2(test2.splitlines()))
print("Puzzle2", solve2(open("puzzle_input").readlines()))