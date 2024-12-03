import re

from base_day import BaseDay


class Day3(BaseDay):
    def __init__(self, hide_output: bool = False):
        super().__init__(3, hide_output)

    def part1(self) -> str:
        sum = 0
        for line in self.lines:
            mul_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
            matches = re.finditer(mul_regex, line, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                sum += int(match.group(1)) * int(match.group(2))

        return str(sum)

    def part2(self) -> str:
        mul_enabled = True

        # this way collapses everything to 1 line, and then removes everything betweent a don't() and a do(),
        # then processes just like part 1. This isn't faster than dumb old regex method but leaving for posterity.

        # clean_sum = 0
        #
        # replace_reg = r"don't\(\).*?(do\(\)|$)"
        # clean_line = re.sub(r"\n", "", self.data)
        # clean_line = re.sub(replace_reg, "", clean_line)
        #
        # mul_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
        # matches = re.finditer(mul_regex, clean_line, re.MULTILINE)
        # for matchNum, match in enumerate(matches, start=1):
        #     # print(f"Multiplying {int(match.group(1))} x {int(match.group(2))}")
        #     clean_sum += int(match.group(1)) * int(match.group(2))
        # return str(clean_sum)

        sum = 0
        for line in self.lines:

            regex = r"(mul)\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)"
            matches = re.finditer(regex, line, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                op = match.group(1)
                if match.group(1) == "mul" and mul_enabled:
                    # print(f"Multiplying {int(match.group(2))} x {int(match.group(3))}")
                    sum += int(match.group(2)) * int(match.group(3))
                elif match.group(4) == "do":
                    mul_enabled = True
                elif match.group(5) == "don't":
                    mul_enabled = False
        return str(sum)


if __name__ == "__main__":
    Day3().run()
