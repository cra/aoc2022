test = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def solve1(lines):
    elves = lines.strip().split('\n''\n')
    max_cals = 0
    for elf in elves:
        cals = sum(map(int, elf.split('\n')))
        max_cals = max(cals, max_cals)
    return max_cals


def solve2(lines):
    elves = lines.strip().split('\n''\n')
    cals = []
    for elf in elves:
        cals.append(sum(map(int, elf.split('\n'))))
    cals = sorted(cals, reverse=True)
    #print(cals)
    return sum(cals[:3])


print("Test1", solve1(test))
print("Puzzle1", solve1(open("puzzle_input").read()))
print("Test2", solve2(test))
print("Puzzle2", solve2(open("puzzle_input").read()))
