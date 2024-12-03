from typing import List

from base_day import BaseDay


class Day2(BaseDay):
    def __init__(self, hide_output: bool = False):
        super().__init__(2, hide_output)
        self.reports = [list(map(int, line.split())) for line in self.lines]

    @staticmethod
    def report_valid(report: List[int], dampen: bool = False):
        # Determine the asc/desc order based off the first 2 elements. these can never be wrong
        descending = (report[0] - report[1]) > 0
        valid = True
        for i in range(0, len(report) - 1):

            # for each pair of numbers, we will subtract and ensure both the asc/desc is the same and that they
            # differ by no more than 3
            diff = report[i] - report[i + 1]
            valid_gap = 0 < abs(diff) <= 3
            valid_sign = descending and diff > 0 or (not descending and diff < 0)

            if not valid_gap or not valid_sign:
                valid = False

                # Part 2 allows us to ignore one invalid element, and if the string is valid that way, to count it
                if dampen:

                    # try removing the left element of the pair, if valid return True immediately
                    report_without_left = report[:i] + report[i + 1 :]
                    left_valid = Day2.report_valid(report_without_left, False)
                    if left_valid:
                        return True

                    # if we are here, left element didn't fix it, lets try removing the right element and return if true
                    report_without_right = report[: i + 1] + report[i + 2 :]
                    right_valid = Day2.report_valid(report_without_right, False)
                    if right_valid:
                        return True

        # the logic above only tests removing the left or right element of a detected "error", thus it would never try
        # removing the first element, lets do so explicitly here in case what was wrong was our assumed direction (asc/desc)
        if dampen and not valid:
            remove_first = Day2.report_valid(report[1:], False)
            valid = remove_first

        return valid

    def part1(self) -> str:
        total_safe = sum(1 for x in self.reports if self.report_valid(x))
        return str(total_safe)

    def part2(self) -> str:
        total_safe = sum(1 for x in self.reports if self.report_valid(x, dampen=True))
        return str(total_safe)


if __name__ == "__main__":
    Day2().run()
