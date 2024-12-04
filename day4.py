from typing import List, Optional, Tuple

from base_day import BaseDay, InputStyle, Point


class Day4(BaseDay):
    def __init__(self, hide_output: bool = False):
        super().__init__(4, hide_output, input_style=InputStyle.CHAR_GRID)

    def search_along_direction(
        self, start_point: Point, remaining_letters: str, direction: (int, int)
    ) -> Optional[Tuple[Point, Point]]:
        x = start_point.x
        y = start_point.y

        for i in range(len(remaining_letters)):
            x += direction[0]
            y += direction[1]
            char = self.grid[(x, y)]
            if char == "":
                return None

            if char != remaining_letters[i]:
                return None

        # print(f"Found word: ({start_point}, {(x, y)}")
        return start_point, Point(x, y)

    def print_grid(self):
        for y in range(self.grid_size.height):
            for x in range(self.grid_size.width):
                print(self.grid[(x, y)], end="")
            print()

    def find_word_locations(
        self, word: str, search_directions: List[Tuple[int, int]]
    ) -> List[Tuple[Point, Point]]:

        locations = []
        start_letter = word[0]

        for y in range(self.grid_size.height):
            for x in range(self.grid_size.width):
                if self.grid[(x, y)] != start_letter:
                    continue
                for direction in search_directions:
                    location = self.search_along_direction(
                        Point(x, y), word[1:], direction
                    )
                    if location:
                        locations.append(location)
                    pass

        return locations

    def part1(self) -> str:
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]
        locations = self.find_word_locations("XMAS", directions)

        return str(len(locations))

    def part2(self) -> str:

        left_arm_directions = [(1, 1), (-1, -1)]
        right_arm_directions = [(1, -1), (-1, 1)]

        left_arms = self.find_word_locations("MAS", left_arm_directions)
        right_arms = self.find_word_locations("MAS", right_arm_directions)

        centers = []
        x_mas_found = 0
        for arm in left_arms:
            highest_point = arm[0] if arm[0].y < arm[1].y else arm[1]
            centers.append(Point(highest_point.x + 1, highest_point.y + 1))

        for arm in right_arms:
            highest_point = arm[0] if arm[0].y < arm[1].y else arm[1]
            center_point = Point(highest_point.x - 1, highest_point.y + 1)

            if center_point in centers:
                x_mas_found += 1

        return str(x_mas_found)


if __name__ == "__main__":
    Day4().run()
