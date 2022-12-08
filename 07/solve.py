import math
from dataclasses import dataclass

test = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".lstrip()


class Dir:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.size = None

    def __repr__(self):
        return f"{self}::{','.join(map(str, self.children))}"

    def __getitem__(self, key):
        to = self.children[key]
        assert isinstance(to, Dir)
        return to

    def __str__(self):
        return f'[D]{self.name}'

    def __len__(self):
        count = 0
        for child in self.children.values():
            count += len(child)
        return count


@dataclass
class File:
    size: int
    name: str

    def __len__(self):
        return self.size


def parse_tree(lines):
    root = Dir('/')
    cur = None

    i = 0
    while i < len(lines):
        line = lines[i]
        first_token = line.split()[:2]
        match first_token:
            case ['$', 'cd']:
                last_token = line.split()[-1]
                match last_token:
                    case '/':
                        cur = root
                    case '..':
                        cur = cur.parent
                    case _:
                        cur = cur[last_token]
                i += 1
            case ['$', 'ls']:
                j = i + 1
                while j < len(lines):
                    if lines[j].startswith("$ "):
                        break
                    size, name = lines[j].split()
                    if not lines[j].startswith('dir'):
                        cur.children[name] = File(int(size), name)
                    else:
                        cur.children[name] = Dir(name, parent=cur)
                    j += 1
                i = j
            case 'dir':
                print("Err.. Let's see first if I encounter this")
            case _:
                size, name = line.split()
                cur.children[name] = File(int(size), name)
                i += 1
    return root


def solve1(lines):
    root = parse_tree(lines)
    sizes_below_100k = []
    
    def visit_all_dir_nodes(node):
        if len(node) <= 100_000:
            sizes_below_100k.append(len(node))
        for child in node.children.values():
            if isinstance(child, Dir):
                if child.children:
                    visit_all_dir_nodes(child)
    visit_all_dir_nodes(root)

    return sum(sizes_below_100k)
    

def solve2(lines):
    total = 70000000
    need = 30000000
    
    root = parse_tree(lines)
    target = need - (total - len(root))
    
    all_dir_sizes = []
    def visit_all_dir_nodes(node):
        all_dir_sizes.append(len(node))
        for child in node.children.values():
            if isinstance(child, Dir):
                if child.children:
                    visit_all_dir_nodes(child)
    visit_all_dir_nodes(root)

    for sz in sorted(all_dir_sizes):
        if sz > target:
            return sz
    return None  # wait what

    

print("Test1", solve1(test.splitlines()))
print("Puzzle1", solve1(open("puzzle_input").readlines()))
print("Test2", solve2(test.splitlines()))
print("Puzzle2", solve2(open("puzzle_input").readlines()))
