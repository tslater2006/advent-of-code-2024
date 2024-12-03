from base_day import BaseDay
from collections import defaultdict


class Day1(BaseDay):
    def __init__(self, hide_output: bool = False):
        super().__init__(1, hide_output)
        left = []
        right = []

        for line in self.lines:
            a, b = map(int, line.split("   "))
            left.append(a)
            right.append(b)

        self.left = left
        self.right = right

    def part1(self) -> str:

        self.left.sort()
        self.right.sort()
        total_distance = 0
        for i in range(0, len(self.left)):
            total_distance += abs(self.left[i] - self.right[i])

        return str(total_distance)

    def part2(self) -> str:
        seen_map = defaultdict(lambda: 0)
        for i in self.right:
            seen_map[i] += 1

        similarity_score = 0
        for i in self.left:
            similarity_score += i * seen_map[i]

        return str(similarity_score)


if __name__ == "__main__":
    Day1().run()
