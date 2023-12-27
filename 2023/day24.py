from aocd import get_data, submit
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

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
        z_intersect = (x_intersect - hailstone_1[0][0])* hailstone_1[1][2] / hailstone_1[1][0] + hailstone_1[0][2]
        return False, [x_intersect, y_intersect, z_intersect]

def intersectPositionInRange(intersect_position, range_x, range_y, range_z):
    intersect_x = intersect_position[0] > range_x[0] and intersect_position[0] < range_x[1]
    intersect_y = intersect_position[1] > range_y[0] and intersect_position[1] < range_y[1]
    intersect_z = intersect_position[2] > range_z[0] and intersect_position[2] < range_z[1]
    return ( intersect_x and intersect_y and intersect_z)

def intersectInFuture(hailstone_1, hailstone_2, intersect_position):
    hailstone_1_future = ((intersect_position[0] - hailstone_1[0][0]) / hailstone_1[1][0]) > 0
    hailstone_2_future = ((intersect_position[0] - hailstone_2[0][0]) / hailstone_2[1][0]) > 0
    return hailstone_1_future and hailstone_2_future

intersecting_hailstones = 0
for hailstone_id, hailstone in enumerate(hailstones):
    for hailstone_2 in hailstones[(hailstone_id +1):]:
        parallel, intersect_position = intersect(hailstone, hailstone_2)
        # For dummy data use min_position, max_position = 7, 27  
        range_x, range_y, range_z = [200000000000000, 400000000000000], [200000000000000, 400000000000000], [200000000000000, 400000000000000]
        if not parallel and intersectPositionInRange(intersect_position, range_x, range_y, range_z) and intersectInFuture(hailstone, hailstone_2, intersect_position):
            intersecting_hailstones += 1

answerA = intersecting_hailstones
print("Answer A", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###
def fitLine(x_points, y_points, z_points):
    # n, x_bar, y_bar, z_bar = len(x_points), sum(x_points)/len(x_points), sum(y_points)/len(y_points), sum(z_points)/len(z_points)
    x_bar, y_bar, z_bar = sum(x_points)/len(x_points), sum(y_points)/len(y_points), sum(z_points)/len(z_points)
    coords = np.array((x_points, y_points, z_points)).T

    pca = PCA(n_components=1)
    pca.fit(coords)
    direction_vector = pca.components_

    # Create plot
    origin = np.mean(coords, axis=0)
    euclidian_distance = np.linalg.norm(coords - origin, axis=1)
    extent = np.max(euclidian_distance)
    print("extent", extent)
    print(origin - extent * direction_vector)
    print(origin + extent * direction_vector)
    start_points = origin - extent * direction_vector
    end_points = origin + extent * direction_vector

    line = np.vstack((origin - direction_vector * extent,
                    origin + direction_vector * extent))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.scatter(coords[:, 0], coords[:, 1], coords[:,2])
    ax.plot(line[:, 0], line[:, 1], line[:, 2], 'r')
    plt.savefig('day_24.png')

    # numer = sum([xi*yi for xi,yi in zip(x_points, y_points)]) - n * x_bar * y_bar
    # denum = sum([xi**2 for xi in x_points]) - n * x_bar**2
    # b = numer / denum
    # a = y_bar - b * x_bar
    return direction_vector, start_points.tolist(), end_points.tolist()

# a, b = fitLine(hailstones)
x_points, y_points, z_points = [h[0][0] for h in hailstones], [h[0][1] for h in hailstones], [h[0][2] for h in hailstones]

direction_vector, start_points, end_points = fitLine(x_points, y_points, z_points)
print(direction_vector)
print(start_points, end_points)

def setSearchRange(rock):
    if rock[1][0] > 0:
        range_x = [ rock[0][0], 400000000000000000 ]
    else:
        range_x = [ 0, rock[0][0]]

    if rock[1][1] > 0:
        range_y = [ rock[0][1], 400000000000000000 ]
    else:
        range_y = [ 0, rock[0][1]]

    if rock[1][2] > 0:
        range_z = [ rock[0][2], 400000000000000000 ]
    else:
        range_z = [ 0, rock[0][2]]
    return range_x, range_y, range_z


def checkIfAllHailstonesCollide(hailstones, rock):
    intersecting_hailstones = 0
    for hailstone in hailstones:
        parallel, intersect_position = intersect(hailstone, rock)
        range_x, range_y, range_z = setSearchRange(rock)
        if not parallel and intersectPositionInRange(intersect_position, range_x, range_y, range_z) and intersectInFuture(hailstone, rock, intersect_position):
            intersecting_hailstones += 1
    return intersecting_hailstones == len(hailstones)

def getHailstoneClosestToStart(hailstones):
    # The diction of the rock is [+, +, +]
    # So we want to get the rock with x_min, y_min, z_min
    max_score = -hailstones[0][0][0] - hailstones[0][0][1] - hailstones[0][0][2]
    hailstone_closest, hailstone_second_closest = None, None
    for hailstone in hailstones:
        score = hailstone[0][0] - hailstone[0][1] - hailstone[0][2]
        if score > max_score:
            max_score = score
            hailstone_second_closest = hailstone_closest
            hailstone_closest = hailstone
            
    return hailstone_closest, hailstone_second_closest


def next_hailstone_positions(hailstone, num_positions):
    next_positions = []
    for t in range(num_positions):
        next_x = hailstone[0][0] + (t+1) * hailstone[1][0]
        next_y = hailstone[0][1] + (t+1) * hailstone[1][1]
        next_z = hailstone[0][2] + (t+1) * hailstone[1][2]
        next_positions.append([next_x, next_y, next_z])
    return next_positions


# Iterate from hailstone closest to start and see what we get
hailstone_closest, hailstone_second_closest = getHailstoneClosestToStart(hailstones)
num_positions = 200
closest_hailstone_positions, second_closest_hailstone_positions = next_hailstone_positions(hailstone_closest, num_positions), next_hailstone_positions(hailstone_second_closest, num_positions)
print("Closest hailstone", hailstone_closest)
print("Second-closest hailstone", hailstone_second_closest)

# Fit a line between the closest and second closest hailstone positions
def findRock(closest_hailstone_positions, second_closest_hailstone_positions):
    for t_c, c in enumerate(closest_hailstone_positions):
        for t_s, s in enumerate(second_closest_hailstone_positions):
            if t_c < t_s:
                velocity = [(s[0] - c[0]) / (t_s - t_c), (s[1] - c[1])/ (t_s - t_c), (s[2] - c[2]) / (t_s - t_c)]
                position = [c[0] - (t_c + 1) * velocity[0], c[1] - (t_c + 1) * velocity[1], c[2] - (t_c + 1) * velocity[2]]
                rock = [position, velocity]
                check = checkIfAllHailstonesCollide(hailstones, rock)
                if check:
                    return rock
            elif t_s < t_c:
                velocity = [(c[0] - s[0]) / (t_c - t_s), (c[1] - s[1]) / (t_c - t_s), (c[2] - s[2]) / (t_c - t_s)]
                position = [s[0] - (t_s + 1) * velocity[0], s[1] - (t_s + 1) * velocity[1], s[2] - (t_s + 1) * velocity[2]]
                rock = [position, velocity]
                check = checkIfAllHailstonesCollide(hailstones, rock)
                if check:
                        return rock
    return None

rock = findRock(closest_hailstone_positions, second_closest_hailstone_positions)
print("We found this rock", rock)
# rock = [[24, 13, 10], [-3, 1, 2]]

# check = checkIfAllHailstonesCollide(hailstones, rock)
# print("All hailstones collide is:", check)
# plt.plot(x_points, y_fit)

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)