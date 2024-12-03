import sys


class BaseDay:
    def __init__(self, day: int, hide_output: bool):
        self.day = day
        self.hide_output = hide_output
        test = False
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            test = True
        if test:
            with open(f"inputs/test/input{day}.txt") as f:
                self.lines = [line.rstrip() for line in f]
        else:
            with open(f"inputs/actual/input{day}.txt") as f:
                self.lines = [line.rstrip() for line in f]

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
