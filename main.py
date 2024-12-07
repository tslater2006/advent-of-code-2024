import time
from day1 import Day1
from day2 import Day2
from day3 import Day3
from day4 import Day4
from day5 import Day5
from day6 import Day6

iterations = 1
average = 0.0

for i in range(iterations):
    start_time = time.perf_counter_ns()

    # Print table header only for the first iteration
    if i == 0:
        print(
            "|-----------------------------------------------------------------------------------------|"
        )
        print(
            "| Day |    Part 1 Result   |  Part 1 Time (ms)  |    Part 2 Result   |  Part 2 Time (ms)  |"
        )
        print(
            "|-----------------------------------------------------------------------------------------|"
        )

    # Run each day's solution and capture results
    # Print each as we go
    all_days = [Day1, Day2, Day3, Day4, Day5, Day6]
    for day_num, DayClass in enumerate(all_days, start=1):
        part1_res, part2_res, part1_ms, part2_ms = DayClass(hide_output=(i > 0)).run()
        # Print the result in a tabular format right after obtaining it
        print(
            f"| {day_num:<3} | {str(part1_res):<18} | {part1_ms:<18.3f} | {str(part2_res):<18} | {part2_ms:<18.3f} |"
        )

    end_time = time.perf_counter_ns()
    average += end_time - start_time

average = average / iterations
print(
    "|-----------------------------------------------------------------------------------------|"
)
print(f"Total run time: {average / 1_000_000:.3f} ms")
