from aocd import get_data, submit

year, day = 2023, 24
data = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""".split("\n")
data = get_data(year=year, day=day).splitlines()

hailstones = []
for row in data:
    position, velocity = row.split(" @ ")
    hailstones.append([[int(p) for p in position.split(", ")], [int(v) for v in velocity.split(", ")]])

def intersect(hailstone_1, hailstone_2):
    velocity_diff = (hailstone_1[1][1]/hailstone_1[1][0] - hailstone_2[1][1]/hailstone_2[1][0])
    if velocity_diff == 0:
        return True, [0,0]
    else:    
        x_intersect = (hailstone_2[0][1] - hailstone_1[0][1] + hailstone_1[0][0] * hailstone_1[1][1] / hailstone_1[1][0] - hailstone_2[0][0] * hailstone_2[1][1] / hailstone_2[1][0]) / velocity_diff
        y_intersect = (x_intersect - hailstone_1[0][0])* hailstone_1[1][1] / hailstone_1[1][0] + hailstone_1[0][1]
        return False, [x_intersect, y_intersect]

def intersectPositionInRange(intersect_position):
    # min_position, max_position = 7, 27
    min_position, max_position = 200000000000000, 400000000000000
    return (intersect_position[0] > min_position and intersect_position[0] < max_position and intersect_position[1] > min_position and intersect_position[1] < max_position)

def intersectInFuture(hailstone_1, hailstone_2, intersect_position):
    hailstone_1_future = ((intersect_position[0] - hailstone_1[0][0]) / hailstone_1[1][0]) > 0
    hailstone_2_future = ((intersect_position[0] - hailstone_2[0][0]) / hailstone_2[1][0]) > 0
    return hailstone_1_future and hailstone_2_future

intersecting_hailstones = 0
for hailstone_id, hailstone in enumerate(hailstones):
    for hailstone_2 in hailstones[(hailstone_id +1):]:
        parallel, intersect_position = intersect(hailstone, hailstone_2)
        if not parallel and intersectPositionInRange(intersect_position) and intersectInFuture(hailstone, hailstone_2, intersect_position):
            intersecting_hailstones += 1

answerA = intersecting_hailstones
print("Answer A", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)