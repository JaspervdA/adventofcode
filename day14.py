from aocd import get_data, submit
import copy 

year, day = 2023, 14
data = get_data(year=year, day=day).splitlines()

# data = ["O....#....",
# "O.OO#....#",
# ".....##...",
# "OO.#O....O",
# ".O.....O#.",
# "O.#..O.#.#",
# "..O..#O..O",
# '.......O..',
# '#....###..',
# '#OO..#....']

def transposePuzzle(puzzle_rows):
    puzzle_cols = []
    num_cols = len(puzzle_rows[0])
    for x in range(num_cols):
        puzzle_col = ""
        for puzzle_row in puzzle_rows:
            puzzle_col += puzzle_row[x]
        puzzle_cols.append(puzzle_col)
    return puzzle_cols

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

hashtag_positions = []
zero_positions = []
for row in transposePuzzle(data):
    hashtag_positions.append(find(row, "#"))
    zero_positions.append(find(row, "O"))

puzzle_height = len(data)

def calculateTotalLoad(hashtag_positions_input, zero_positions_input):
    hashtag_positions = copy.deepcopy(hashtag_positions_input)
    zero_positions = copy.deepcopy(zero_positions_input)
    total_score = 0
    for cube_positions, rock_positions in zip(hashtag_positions, zero_positions):
        # Add a final blocker cube for the loop to work on the last rocks
        cube_positions.append(puzzle_height)
        last_cube_position = 0
        for cube_ix, cube_position in enumerate(cube_positions):
            next_cube_position = cube_position
            new_rock_positions = rock_positions

            for idx, zero_position in enumerate(rock_positions[:]):
                # We reached the next nube-shaped rock
                if zero_position > next_cube_position:
                    last_cube_position = cube_position
                    rock_positions = new_rock_positions
                    break
                else:
                    extra_score = 1 if cube_ix > 0 else 0

                    total_score += puzzle_height - (last_cube_position + idx + extra_score)
                    new_rock_positions.pop(0)
                    # This zero is in between the hasthags
                    
                    # Set the zero behind the cube-shaped rock
    return total_score

# answerA = calculateTotalLoad(hashtag_positions, zero_positions)
# print("Answer A", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

def rolledRockPositionsNorth(cube_positions, rock_positions):
    rolled_rock_positions = []
    for cube_positions_row, rock_positions_row in zip(cube_positions, rock_positions):
        cube_positions_row.append(puzzle_height)
        last_cube_position = 0
        rolled_positions_row = []
        for cube_ix, cube_position in enumerate(cube_positions_row):
            next_cube_position = cube_position
            new_rock_positions = rock_positions_row
            for idx, zero_position in enumerate(new_rock_positions[:]):
                # We reached the next nube-shaped rock
                if zero_position > next_cube_position:
                    last_cube_position = cube_position
                    rock_positions_row = new_rock_positions
                    break
                else:
                    extra_position = 1 if cube_ix > 0 else 0
                    rolled_positions_row.append(last_cube_position + idx + extra_position)
                    new_rock_positions.pop(0)
                    # This zero is in between the hasthags
        rolled_rock_positions.append(rolled_positions_row)
    # Remove the extra hashtag we added to loop
    for cube_positions_row in cube_positions:
        cube_positions_row.pop()
    # print("WAAROM IS DEZE LEEG?", rock_positions)
    return rolled_rock_positions

def flipPositions(positions):
    size = len(positions)
    flipped_positions = [[] for i in range(size)]
    for row_idx, position_row in enumerate(positions):
        for position in position_row:
            flipped_positions[size - 1 - position].append(row_idx)
    return flipped_positions

def flipPuzzleRight(cube_positions, rock_positions):
    return flipPositions(cube_positions), flipPositions(rock_positions)

# Get the new cube positions using the code from part A
def doCycle(cube_positions, rock_positions):
    rolled_rock_positions = rolledRockPositionsNorth(cube_positions, rock_positions)
    
    # Now flip the puzzle to the right to make sure a west roll is a north roll
    flipped_cube_positions, flipped_rock_positions = flipPuzzleRight(cube_positions, rolled_rock_positions)
    rolled_rock_positions = rolledRockPositionsNorth(flipped_cube_positions, flipped_rock_positions)
    #Now flip the puzzle to the right to make sure a south roll is a north roll
    flipped_cube_positions, flipped_rock_positions = flipPuzzleRight(flipped_cube_positions, rolled_rock_positions)
    rolled_rock_positions = rolledRockPositionsNorth(flipped_cube_positions, flipped_rock_positions)
    # Now flip the puzzle to the right to make sure a east roll is a north roll
    flipped_cube_positions, flipped_rock_positions = flipPuzzleRight(flipped_cube_positions, rolled_rock_positions)
    rolled_rock_positions = rolledRockPositionsNorth(flipped_cube_positions, flipped_rock_positions)
    # Now flip the puzzle back!
    flipped_cube_positions, flipped_rock_positions = flipPuzzleRight(flipped_cube_positions, rolled_rock_positions)

    return flipped_rock_positions

def calculateTotalLoadNoRoll(zero_positions_input):
    score = 0
    length = len(zero_positions_input)
    for row in zero_positions_input:
        for item in row:
            score += length - item

    return score

last_cycled_rocks = zero_positions
loads = []
for i in range(1000):
    cycled_rocks = doCycle(hashtag_positions, last_cycled_rocks)
    loads.append(calculateTotalLoadNoRoll(cycled_rocks))
    last_cycled_rocks = cycled_rocks

print(loads)

similar_positions = []
indices_last_number = [i for i, x in enumerate(loads) if x == loads[-1]]

loop_size = indices_last_number[-1] - indices_last_number[-2]

item_number = 1000000 % loop_size

print('hi')
loads[-1 -loop_size]
answerB = loads[ -2 - loop_size + item_number]
print("answer B is", answerB)

submit(answerB, part="b", day=day, year=year)