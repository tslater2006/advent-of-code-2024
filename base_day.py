class BaseDay:
    def __init__(self, day: int, test: bool):
        self.day = day
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
