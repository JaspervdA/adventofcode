from aocd import get_data, submit
from functools import reduce

year, day = 2023, 6

data = get_data(year=year, day=day).splitlines()
# data = ['Time:      7  15   30',
# 'Distance:  9  40  200']
# print(data)


a = data[0].split(" ")
b = data[1].split(" ")

times = []
time_b = ""
for x in a:
    if x.isnumeric():
        time_b += x
        times.append(int(x))

distances = []
distance_b = ""
for y in b:
    if y.isnumeric():
        distance_b += y
        distances.append(int(y))


def checkIfWinning(time, record_distance):
    true_count = 0 
    total_time = time
    for t in range(time):
        speed = t
        distance = (total_time - t ) * speed
        if distance > record_distance:
            true_count += 1
    return true_count

# win_counts = []
# for time, distance in zip(times, distances):
#     win_counts.append(checkIfWinning(time, distance))

# answerA = reduce(lambda x, y: x*y, win_counts)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

answerB = checkIfWinning(int(time_b), int(distance_b))
print(answerB)
submit(answerB, part="b", day=day, year=year)