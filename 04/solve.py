import itertools

test = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def solve1(lines):
    count = sum(
        any((a <= c and b >= d, c <= a and d >= b))
        for a, b, c, d in (map(int, l.split('-') + r.split('-')) for l, r in (line.split(",") for line in lines))
    )
    return count


def solve2(lines):
    count = sum(
        any((a <= c and c <= b, a >= c and b <= d, c <= a <= d))
        for a, b, c, d in (map(int, l.split('-') + r.split('-')) for l, r in (line.split(",") for line in lines))
    )
    return count


print("Test1", solve1(test.strip().splitlines()))
print("Puzzle1", solve1(open("puzzle_input").readlines()))
print("Test2", solve2(test.strip().splitlines()))
print("Puzzle2", solve2([line.strip() for line in open("puzzle_input").readlines()]))
