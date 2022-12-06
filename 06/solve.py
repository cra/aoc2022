import functools
import more_itertools


test = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]
answers1 = [7, 5, 6, 10, 11]
answers2 = [19, 23, 23, 29, 26]
assert len(test) == len(answers1) == len(answers2)


def solve(line, w):
    for idx, window in enumerate(more_itertools.windowed(line, w), start=w):
        if len(window) == len(set(window)):
            return idx

solve1 = functools.partial(solve, w=4)
solve2 = functools.partial(solve, w=14)

for t, a in zip(test, answers1):
    print(f"Test1({t}) = {solve1(t)} (should be {a})")
print(f"Puzzle1(open('puzzle_input')) = {solve1(open('puzzle_input').readline().strip())}")

for t, a in zip(test, answers2):
    print(f"Test2({t}) = {solve2(t)} (should be {a})")
print(f"Puzzle2(open('puzzle_input')) = {solve2(open('puzzle_input').readline().strip())}")


