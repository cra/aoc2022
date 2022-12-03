test = """
A Y
B X
C Z
"""

def solve1(lines):
    value = {"A": 1, "B": 2, "C": 3}
    translate = {"X": "A", "Y": "B", "Z": "C"}
    wins = {"A": "C", "B": "A", "C": "B"}
    score = 0
    for fight in lines:
        elf, me = fight.split()
        me = translate[me]
        price = value[me]
        if me == elf:
            score += 3 + price
            continue
        if wins[me] == elf:
            score += 6 + price
            continue
        if wins[elf] == me:
            score += 0 + price
            continue
    return score


def solve2(lines):
    value = {"A": 1, "B": 2, "C": 3}
    translate = {
        "A X": "C", "A Y": "A", "A Z": "B",
        "B X": "A", "B Y": "B", "B Z": "C",
        "C X": "B", "C Y": "C", "C Z": "A",
    }
    wins = {"X": 0, "Y": 3, "Z": 6}
    score = 0
    for fight in lines:
        fight = fight.strip()
        elf, target = fight.split()
        me = translate[fight]
        score += wins[target] + value[me]
    return score

print("Test1", solve1(test.strip().splitlines()))
print("Puzzle1", solve1(open('puzzle_input').readlines()))
print("Test2", solve2(test.strip().splitlines()))
print("Puzzle1", solve2(open('puzzle_input').readlines()))
