import time
from day1 import Day1
from day2 import Day2
from day3 import Day3
from day4 import Day4
from day5 import Day5


iterations = 1
average = 0.0

for i in range(iterations):
    start_time = time.perf_counter_ns()

    Day1(hide_output=(i > 0)).run()
    Day2(hide_output=(i > 0)).run()
    Day3(hide_output=(i > 0)).run()
    Day4(hide_output=(i > 0)).run()
    Day5(hide_output=(i > 0)).run()
    end_time = time.perf_counter_ns()
    average += end_time - start_time

average = average / iterations

print(f"Ran in: {average/1000000}ms")
