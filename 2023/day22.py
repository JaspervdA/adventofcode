from aocd import get_data, submit
import copy

year, day = 2023, 22
data = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".split("\n")
# data = """1,0,1~1,3,1
# 1,1,2~1,1,4
# 1,3,2~1,3,2
# 1,3,3~1,3,3
# 1,3,4~1,3,4
# 1,0,5~1,3,5""".split("\n")
# data = """1,0,1~1,3,1
# 1,1,2~1,1,4
# 1,3,2~1,3,3
# 1,3,4~1,3,4
# 1,0,5~1,3,5""".split("\n")
data = get_data(year=year, day=day).splitlines()

max_x, max_y, max_z, bricks, bricks_min_z = 0, 0, 0, [], []
for brick in data:
    brick_start, brick_end = brick.split("~")
    brick_start, brick_end = [int(b) for b in brick_start.split(",")], [int(b) for b in brick_end.split(",")]
    max_x, max_y, max_z = max(max_x, brick_start[0], brick_end[0]), max(max_y, brick_start[1], brick_end[1]), max(max_z, brick_start[2], brick_end[2])
    bricks_min_z.append(min(brick_end[2], brick_start[2]))
    bricks.append([brick_start, brick_end])
empty_grid, bricks_moved_down = [[[None for z in range(max_z + 2)] for y in range(max_y + 1)] for x in range(max_x + 1)], []
def findBrickBelow(brick, min_z):
    for z in reversed(range(min_z)):
        for x in range(brick[0][0], brick[1][0] +1):
            for y in range(brick[0][1], brick[1][1] +1):        
                if empty_grid[x][y][z] is not None:
                    return z + 1
    return 1

def moveBrickDown(brick, min_z, brick_idx):
    z_to_move_to = findBrickBelow(brick, min_z)
    z_diff, brick_moved_down = min_z - z_to_move_to, copy.deepcopy(brick)
    brick_moved_down[0][2] -= z_diff
    brick_moved_down[1][2] -= z_diff
    for x in range(brick[0][0], brick[1][0] +1):
        for y in range(brick[0][1], brick[1][1] +1):
            for z in range(z_to_move_to, z_to_move_to + 1 + brick[1][2] - brick[0][2]):
                empty_grid[x][y][z] = brick_idx
    return brick_moved_down

def getBricksBelow(brick):
    bricks_below = []
    for x in range(brick[0][0], brick[1][0] +1):
        for y in range(brick[0][1], brick[1][1] +1):
            z = brick[0][2]
            block_below = empty_grid[x][y][z-1]
            if block_below is not None and block_below not in bricks_below:
                bricks_below.append(block_below)
    return bricks_below

def getBricksAbove(brick):
    bricks_above = []
    for x in range(brick[0][0], brick[1][0] +1):
        for y in range(brick[0][1], brick[1][1] +1):
            z = brick[1][2]
            block_above = empty_grid[x][y][z+1]
            if block_above is not None and block_above not in bricks_above:
                bricks_above.append(block_above)
    return bricks_above

def getAllBricksAbove(brick, brick_idx):
    current_bricks_above_list, brick_above_count, bricks_above_higher_z = [brick], 0, []
    seen_brick_above_ids = [brick_idx]
    removed_bricks = [brick_idx]
    current_z = brick[1][2]
    while len(current_bricks_above_list) > 0 or len(bricks_above_higher_z) > 0:
        current_z +=1
        new_bricks_above_list, bricks_above_ids, new_bricks_above_higher_z, new_filtered_bricks_above_list = [], [], [], []
        # Get all bricks above the current brick
        for current_brick in current_bricks_above_list: 
            bricks_above_ids.extend(getBricksAbove(current_brick))

        for brick_above_id in list(set(bricks_above_ids)):
            if brick_above_id not in seen_brick_above_ids: 
                seen_brick_above_ids.append(brick_above_id)
                # For each brick that is above the current brick check if there are unseen bricks below, if yes the brick will not fall
                bricks_below_ids = getBricksBelow(bricks_moved_down[brick_above_id])    
                all_bricks_below_removed = True
                for brick_below in bricks_below_ids:
                    if brick_below not in removed_bricks:
                        all_bricks_below_removed = False

                if all_bricks_below_removed and bricks_moved_down[brick_above_id] not in new_bricks_above_list:
                    removed_bricks.append(brick_above_id)
                    new_bricks_above_list.append(bricks_moved_down[brick_above_id])
                    brick_above_count +=1 
        
        for brick in (new_bricks_above_list + bricks_above_higher_z):
            if brick[1][2] > current_z and brick not in new_bricks_above_higher_z:
                new_bricks_above_higher_z.append(brick)
            elif brick not in new_filtered_bricks_above_list:
                new_filtered_bricks_above_list.append(brick)
        current_bricks_above_list, bricks_above_higher_z = new_filtered_bricks_above_list, new_bricks_above_higher_z
    return brick_above_count

for brick_idx, (min_z, brick) in enumerate(sorted(zip(bricks_min_z, bricks))):
    bricks_moved_down.append(moveBrickDown(brick, min_z, brick_idx))

disintegrate_bricks = 0
brick_above_counts = []
for brick_idx, brick in enumerate(bricks_moved_down):
    bricks_above_ids = getBricksAbove(brick)
    brick_can_be_removed = True
    # For each brick above, check how many bricks support that bricks
    # If for all bricks above they are supported by more than 1 brick it can be disintegrated
    for brick_above_id in bricks_above_ids:
        bricks_below_ids = getBricksBelow(bricks_moved_down[brick_above_id])
        if len(bricks_below_ids) < 2:
            brick_can_be_removed = False
    if not brick_can_be_removed:
        brick_above_counts.append(getAllBricksAbove(brick, brick_idx))
    if brick_can_be_removed:
        disintegrate_bricks += 1

# print("bricks", bricks)
# print("bricks_moved_down", bricks_moved_down)

answerA = disintegrate_bricks
print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

answerB = sum(brick_above_counts)
print("Answer B is", answerB)
# submit(answerB, part="b", day=day, year=year)