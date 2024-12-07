from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

from base_day import BaseDay, Direction, InputStyle, Point


def move(p: Point, d: int, r: bool = False) -> Point:
    if r:
        match d:
            case 0:
                d = 2
            case 1:
                d = 3
            case 2:
                d = 0
            case 3:
                d = 1

    match d:
        case 0:
            return Point(p.x, p.y - 1)
        case 2:
            return Point(p.x, p.y + 1)
        case 1:
            return Point(p.x + 1, p.y)
        case 3:
            return Point(p.x - 1, p.y)


def move_back(p: Point, d: int) -> Point:
    return move(p, d, True)


class Day6(BaseDay):

    # This method does the normal walk from Part 1 but it also caches start/end points of straight lines traveled
    # this cache is used later for Part 2 so building it here is "free"
    # as we step along we keep track of the "current line"
    # once we hit a barrier, we create entries in the cache map for each point on the line:
    #    cache.add( (point,direction), end_point)
    # this allows us to look up the end point for any spot on the line later
    def normal_walk(self) -> Set[Point]:
        guard_point = self.starting_point
        guard_direction = self.starting_direction
        current_line = [guard_point]
        visited_points: Set[Point] = set()
        visited_points.add(guard_point)
        while True:
            new_point = move(guard_point, guard_direction)
            char = self.grid[new_point]
            if char == "#":
                for p in current_line:
                    line_end = move_back(new_point, guard_direction)
                    self.cache[(Point(p.x, p.y), guard_direction)] = line_end
                visited_points.update(current_line)
                guard_direction = (guard_direction + 1) % 4
                current_line = []
            elif char != "":
                guard_point = new_point
                self.regular_path.add(guard_point)
                current_line.append(guard_point)
            else:
                visited_points.update(current_line)
                break
        return visited_points

    def __init__(self, hide_output: bool = False):
        super().__init__(6, hide_output, input_style=InputStyle.CHAR_GRID)
        self.starting_point: Point = None
        self.starting_direction: int = 0
        self.cache: Dict[Tuple[Point, int], Optional[Point]] = {}
        self.regular_path: Set[Point] = set()
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
        self.visited_points: Set[Point] = set()

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

    # This method runs the walk but with an extra barrier placed at the passed in Point
    # This is accomplished by the following steps:
    #   - Check if there is a cache entry for the current (Point,direction) tuple
    #   - If there is an entry, we'll assume this is our end point
    #   - Before we use it though, we'll check to see if the extra barrier is between
    #     the guard and the cached end point. If so, we'll use the point *before* the extra barrier
    #     as the proper end point
    #   - If there is no entry in the cache for our current location (we are off the original path)
    #     We fall back to walking one space at a time until we hit a barrier (normal or extra)
    #   - Once we've hit a barrier we will track the (Point, direction) tuple of our new location
    #     to mark that we've been here and then turn the guard 90 degrees.
    #   ** This was the big AHA moment. we don't have to track every visited location, only the ends of the lines
    #      and the direction we were traveling. It is not critical to stop traversing the moment we hit a previous
    #      spot. This is because the question isn't asking "how many step until we loop", it just asks if we do!
    #      Big thanks to DFreiberg for this realization.

    def check_for_loop(self, extra_barrier: Point) -> bool:
        guard_point = self.starting_point
        direction = self.starting_direction
        turn_points: Set[Tuple[Point, int]] = set()
        while True:
            cache_key = (guard_point, direction)

            # Check cache
            if cache_key in self.cache:
                cached = self.cache[cache_key]

                # handle if extra barrier is between us and cached end point
                if direction in [0, 2] and cached.x == extra_barrier.x:
                    if direction == 0:  # moving up
                        if guard_point.y > extra_barrier.y >= cached.y:
                            cached = move_back(extra_barrier, direction)
                    elif direction == 2:  # moving down
                        if guard_point.y < extra_barrier.y <= cached.y:
                            cached = move_back(extra_barrier, direction)

                elif direction in [1, 3] and cached.y == extra_barrier.y:
                    if direction == 1:  # moving right
                        if guard_point.x < extra_barrier.x <= cached.x:
                            cached = move_back(extra_barrier, direction)
                    elif direction == 3:  # moving left
                        if guard_point.x > extra_barrier.x >= cached.x:
                            cached = move_back(extra_barrier, direction)

                # move to the end point
                guard_point = cached

                # Check to see if we've been to this end point before from the same direction
                turn_key = (guard_point, direction)
                if turn_key in turn_points:
                    return True
                else:
                    turn_points.add(turn_key)

                # rotate the guard
                direction = (direction + 1) % 4

            else:
                # no cache entry, fall back to walking mode.

                # peek at the character in front of us
                next_point = move(guard_point, direction)
                next_char = self.grid[next_point]

                # if it is a barrier, do the loop check and rotate the guard
                if next_char == "#" or next_point == extra_barrier:
                    turn_key = (guard_point, direction)
                    if turn_key in turn_points:
                        return True
                    else:
                        turn_points.add(turn_key)
                    direction = (direction + 1) % 4
                # otherwise advance the guard to next point
                elif next_char != "":
                    guard_point = next_point
                else:
                    # we fell off the map, no loop
                    return False

    def part1(self) -> str:
        self.visited_points = self.normal_walk()
        unique_point_count = len(self.visited_points)
        return str(unique_point_count)

    def part2(self) -> str:
        found_blocks: Set[Point] = set()
        for p in self.regular_path:
            if p not in found_blocks and p != self.starting_point:
                looped = self.check_for_loop(extra_barrier=p)
                if looped:
                    found_blocks.add(p)
        return str(len(found_blocks))


if __name__ == "__main__":
    part1_result, part2_result, part1_time_ms, part2_time_ms = Day6().run()
    print("Part 1", part1_result)
    print("Part 2", part2_result)
