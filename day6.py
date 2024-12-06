from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

from base_day import BaseDay, Direction, InputStyle, Point


class Day6(BaseDay):
    def __init__(self, hide_output: bool = False):
        super().__init__(6, hide_output, input_style=InputStyle.CHAR_GRID)
        self.starting_point: Point = None
        self.starting_direction: int = 0
        self.movement_offsets: List[Tuple[int, int]] = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
        ]
        for point in self.grid:
            char = self.grid[point]
            if char == "." or char == "#":
                continue

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

    def print_grid(
        self,
        visited_points: Optional[Set[Point]] = None,
        blockage_point: Optional[Point] = None,
    ):
        for y in range(self.grid_size.height):
            for x in range(self.grid_size.width):
                if Point(x, y) in visited_points:
                    if Point(x, y) == blockage_point:
                        print("O", end="")
                    else:
                        print("X", end="")
                    continue
                else:
                    if Point(x, y) == blockage_point:
                        print("O", end="")
                    else:
                        print(self.grid[Point(x, y)], end="")
                    continue
            print()

    def walk_map(
        self, extra_block: Optional[Point] = None, detect_loops: bool = False
    ) -> Tuple[int, bool]:
        visited_points: Set[Point] = set()
        visited_direction_points: Set[Tuple[Point, int]] = set()

        visited_points.add(self.starting_point)
        guard_point = self.starting_point
        guard_direction = self.starting_direction

        while True:
            offset = self.movement_offsets[guard_direction]
            new_point = Point(guard_point.x + offset[0], guard_point.y + offset[1])
            char = self.grid[new_point]
            if char == "#" or new_point == extra_block:
                guard_direction = (guard_direction + 1) % 4
            elif char != "":
                guard_point = new_point
                visited_points.add(new_point)
                # self.print_grid(visited_points, extra_block)
                # print()
                if detect_loops:

                    if (new_point, guard_direction) in visited_direction_points:
                        # print("Good block: ", extra_block)
                        # self.print_grid(visited_points, extra_block)
                        return len(visited_points), True

                    visited_direction_points.add((new_point, guard_direction))
            else:
                return len(visited_points), False

    def part1(self) -> str:
        spots, looped = self.walk_map()
        return str(spots)

    def part2(self) -> str:
        guard_point = self.starting_point
        guard_direction = self.starting_direction
        found_blocks: Set[Point] = set()
        while True:
            offset = self.movement_offsets[guard_direction]
            new_point = Point(guard_point.x + offset[0], guard_point.y + offset[1])
            char = self.grid[new_point]
            if char == "#":
                guard_direction = (guard_direction + 1) % 4
            elif char != "":
                if new_point not in found_blocks:
                    _, looped = self.walk_map(extra_block=new_point, detect_loops=True)
                    if looped:
                        found_blocks.add(new_point)
                guard_point = new_point
            else:
                break

        return str(len(found_blocks))


if __name__ == "__main__":
    Day6().run()
