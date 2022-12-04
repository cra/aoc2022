import functools
import operator
import string

import more_itertools

test = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def solve1(lines):
    weights = {letter: score for score, letter in enumerate(string.ascii_letters, start=1)}
    score = 0
    for content in lines:
        mid = len(content) // 2
        lhs, rhs = content[:mid], content[mid:]
        common = set(rhs) & set(lhs)
        score += weights[common.pop()]
    return score


def solve2(lines):
    weights = {letter: score for score, letter in enumerate(string.ascii_letters, start=1)}
    # score = sum(weights[reduce(and_, map(set, group)).pop()] for group in chunked(lines, 3))
    score = 0
    for group in more_itertools.chunked(lines, 3):
        uniq = functools.reduce(operator.and_, map(set, group)).pop()
        score += weights[uniq]
    return score


print("Test1", solve1(test.strip().splitlines()))
print("Puzzle1", solve1(open("puzzle_input").readlines()))
print("Test2", solve2(test.strip().splitlines()))
print("Puzzle2", solve2([line.strip() for line in open("puzzle_input").readlines()]))
