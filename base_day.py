import sys
from enum import Enum
from collections import defaultdict, namedtuple

Size = namedtuple("Size", ["width", "height"])
Point = namedtuple("Point", ["x", "y"])


class InputStyle(Enum):
    LINES = 1
    RAW = 2
    CHAR_GRID = 3


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class BaseDay:
    def __init__(
        self, day: int, hide_output: bool, input_style: InputStyle = InputStyle.LINES
    ):
        self.day = day
        self.hide_output = hide_output
        test = False
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            test = True
        if test:
            with open(f"inputs/test/input{day}.txt") as f:
                self.data = f.read()
        else:
            with open(f"inputs/actual/input{day}.txt") as f:
                self.data = f.read()

        if input_style != InputStyle.RAW:
            self.lines = [line.rstrip() for line in self.data.splitlines()]

        if input_style == InputStyle.CHAR_GRID:
            self.grid = defaultdict(str)

            self.grid_size = Size(len(self.lines[0]), len(self.lines))
            for y in range(len(self.lines)):
                for x in range(len(self.lines[y])):
                    self.grid[Point(x, y)] = self.lines[y][x]

    def __str__(self):
        return f"Day {self.day}"

    def __repr__(self):
        return f"Day {self.day}"

    def part1(self) -> str:
        raise NotImplementedError

    def part2(self) -> str:
        raise NotImplementedError

    def run(self) -> None:
        part1 = self.part1()
        part2 = self.part2()
        if not self.hide_output:
            print(f"Day {self.day} Part 1: {part1}")
            print(f"Day {self.day} Part 2: {part2}")
