from collections import defaultdict
from typing import Dict, List
from functools import cmp_to_key
from base_day import BaseDay


class Day5(BaseDay):
    def __init__(self, hide_output: bool = False):
        super().__init__(5, hide_output)

        self.ordering_rules: Dict[int, List[int]] = defaultdict(lambda: [])
        self.updates: List[List[int]] = []
        self.invalid_updates: List[List[int]] = []

        rules = True
        for line in self.lines:
            if line.strip() == "":
                rules = False
                continue
            if rules:
                before, after = map(int, line.split("|"))
                self.ordering_rules[before].append(after)
            else:
                self.updates.append(list(map(int, line.split(","))))

        # print(dict(self.ordering_rules))
        # print(self.updates)

    def part1(self) -> str:
        answer = 0
        for index, update in enumerate(self.updates):
            valid = True
            seen = []
            for page in update:
                applicable = [x for x in self.ordering_rules[page] if x in update]
                # print("Applicable: ", applicable)
                # print("Seen: ", seen)

                if any(item in applicable for item in seen):
                    valid = False
                    break
                seen.append(page)

            if valid:
                middle_index = int((len(update) - 1) / 2)
                answer += update[middle_index]
            else:
                self.invalid_updates.append(update)

        return str(answer)

    def compare(self, item1, item2):
        if item2 in self.ordering_rules[item1]:
            return -1
        else:
            return 1

    def part2(self) -> str:
        answer = 0
        for update in self.invalid_updates:
            middle_index = int((len(update) - 1) / 2)
            sorted_update = sorted(update, key=cmp_to_key(self.compare))

            answer += sorted_update[middle_index]
        return str(answer)


if __name__ == "__main__":
    Day5().run()
