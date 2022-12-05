import re
import rich
from collections import defaultdict


test = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def solve1(init, commands, verbose=False):
    stacks = {tag: [] for tag in init.splitlines()[-1].split()}
    init_load = init.splitlines()[:-1]
    for row in init_load:
        if not row:
            continue
        for k, i in enumerate(range(1, len(stacks) * 3 + len(stacks), 4), start=1):
            if i < len(row):
                if (payload := row[i]) != " ":
                    stacks[str(k)].append(payload)
    stacks = {tag: stack[::-1] for tag, stack in stacks.items()}
    if verbose: rich.print(stacks)
    for i, command in enumerate(commands.splitlines(), start=1):
        num, src, target = re.search("move (\d+) from (\d+) to (\d+)", command).groups()
        num = int(num)
        for _ in range(int(num)):
            stacks[target].append(stacks[src].pop())
        if verbose:
            print(i, command, f'{src}-[{num}]->{target}')
            rich.print(stacks)
            print('-' * 80)
    return ''.join(s[-1] for s in stacks.values())


def solve2(init, commands, verbose=False):
    stacks = {tag: [] for tag in init.splitlines()[-1].split()}
    init_load = init.splitlines()[:-1]
    for row in init_load:
        if not row:
            continue
        for k, i in enumerate(range(1, len(stacks) * 3 + len(stacks), 4), start=1):
            if i < len(row):
                if (payload := row[i]) != " ":
                    stacks[str(k)].append(payload)
    stacks = {tag: stack[::-1] for tag, stack in stacks.items()}
    crane_ebanat = []
    if verbose: rich.print(stacks)
    for i, command in enumerate(commands.splitlines(), start=1):
        num, src, target = re.search("move (\d+) from (\d+) to (\d+)", command).groups()
        num = int(num)
        for _ in range(int(num)):
            crane_ebanat.append(stacks[src].pop()) 
        for _ in range(int(num)):
            stacks[target].append(crane_ebanat.pop())
        if verbose:
            print(i, command, f'{src}-[{num}]->{target}')
            rich.print(stacks)
            print('-' * 80)
    return ''.join(s[-1] for s in stacks.values())


print("test1", solve1(*test.split("\n\n")))
print("puzzle1", solve1(*open('puzzle_input').read().split("\n\n")))
print("test2", solve2(*test.split("\n\n")))
print("puzzle2", solve2(*open('puzzle_input').read().split("\n\n")))
