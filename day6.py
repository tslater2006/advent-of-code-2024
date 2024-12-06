from collections import defaultdict
from typing import Dict, List, Set

from base_day import BaseDay, Direction, InputStyle, Point


class Day6(BaseDay):
    def __init__(self, hide_output: bool = False):
        super().__init__(6, hide_output, input_style=InputStyle.CHAR_GRID)
        self.column_map: Dict[int, List[int]] = defaultdict(lambda: [])
        self.row_map: Dict[int, List[int]] = defaultdict(lambda: [])
        self.starting_point: Point = None

        # 0 == UP, 1 == RIGHT, 2 == DOWN, 3 == LEFT
        # rotate right == (val + 1) % 4
        self.starting_direction: int = 0
        for point in self.grid:
            char = self.grid[point]
            if char == ".":
                continue

            loc_x = point[0]
            loc_y = point[1]

            if char == "#":
                self.column_map[loc_x].append(loc_y)
                self.row_map[loc_y].append(loc_x)
            if char in ["^", ">", "<", "v"]:
                self.starting_point = point
                match char:
                    case "^":
                        self.starting_direction = 0
                    case ">":
                        self.starting_direction = 1
                    case "v":
                        self.starting_direction = 2
                    case "<":
                        self.starting_direction = 3

    def print_grid_with_visits(self, visited_points: Set[Point]):
        for y in range(self.grid_size.height):
            row = self.row_map[y]
            for x in range(self.grid_size.width):
                if x in row:
                    print("#", end="")
                    continue
                if Point(x, y) in visited_points:
                    print("X", end="")
                    continue
                else:
                    print(".", end="")
                    continue
            print()

    def part1(self) -> str:
        visited_points: Set[Point] = set()
        visited_points.add(self.starting_point)
        guard_point = self.starting_point
        guard_direction = self.starting_direction

        while True:
            changing_x = (guard_direction == 1) or (guard_direction == 3)
            needs_less_than = (guard_direction == 0) or (guard_direction == 3)
            if guard_direction == 0 or guard_direction == 2:
                # dealing with a column
                list_of_blocks = self.column_map[guard_point.x]
            else:
                list_of_blocks = self.row_map[guard_point.y]

            if changing_x:
                if needs_less_than:
                    blocks_in_front = [x for x in list_of_blocks if x < guard_point.x]
                else:
                    blocks_in_front = [x for x in list_of_blocks if x > guard_point.x]
            else:
                if needs_less_than:
                    blocks_in_front = [y for y in list_of_blocks if y < guard_point.y]
                else:
                    blocks_in_front = [y for y in list_of_blocks if y > guard_point.y]

            if len(blocks_in_front) == 0:
                # Add the points on the map until guard leaves
                if changing_x:
                    if needs_less_than:
                        for x in range(guard_point.x, -1, -1):
                            visited_points.add(Point(x, guard_point.y))
                    else:
                        for x in range(guard_point.x, self.grid_size.width):
                            visited_points.add(Point(x, guard_point.y))
                else:
                    if needs_less_than:
                        for y in range(guard_point.y, -1, -1):
                            visited_points.add(Point(guard_point.x, y))
                    else:
                        for y in range(guard_point.y, self.grid_size.height):
                            visited_points.add(Point(guard_point.x, y))
                # print("leaving!")
                # self.print_grid_with_visits(visited_points)
                break
            else:
                change_step = -1 if needs_less_than else 1
                stopping_offset = 1 if needs_less_than else -1
                block_index = -1 if needs_less_than else 0
                if changing_x:
                    new_x = blocks_in_front[block_index] + stopping_offset
                    while guard_point.x != new_x:
                        guard_point = Point(guard_point.x + change_step, guard_point.y)
                        visited_points.add(guard_point)
                else:
                    new_y = blocks_in_front[block_index] + stopping_offset
                    while guard_point.y != new_y:
                        guard_point = Point(guard_point.x, guard_point.y + change_step)
                        visited_points.add(Point(guard_point.x, guard_point.y))

                guard_direction = (guard_direction + 1) % 4

        return str(len(visited_points))

    def part2(self) -> str:
        return "Not implemented"


if __name__ == "__main__":
    Day6().run()
