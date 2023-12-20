from aocd import get_data, submit
import itertools
import numpy as np

year, day = 2023, 3

data = get_data(year=year, day=day).splitlines()
### Part A ###
chars = ["$","-","@","%","=","/","#","*","&","+"]

num_columns = len(data[0])
num_rows = len(data)
engine_matrix = [[None for i in range(num_columns)] for j in range(num_rows)]

engine_schematic = data

# First create the 2D-matrix with numbers, properly parsed
for row_idx, row in enumerate(engine_schematic):
    numeric_counter = 0
    last_item_is_numeric = False
    row_split = ["".join(x) for _, x in itertools.groupby(row, key=str.isdigit)]

    col_count = 0
    for big_item in row_split:
        if big_item.isnumeric():
            for c in range(len(big_item)):
                engine_matrix[row_idx][col_count + c] = big_item
            col_count += len(big_item)
        else:
            for item_idx, item in enumerate(big_item):
                if item == ".":
                    # For part A
                    # engine_matrix[row_idx][col_count] = False
                    # For part B
                    engine_matrix[row_idx][col_count] = item
                    col_count += 1
                else:
                    # For part A
                    # engine_matrix[row_idx][col_count] = True
                    # For part B
                    engine_matrix[row_idx][col_count] = item
                    col_count += 1

engine_matrix = np.array(engine_matrix)

def find_adjacent_items(row_idx, col_idx):
    min_row_id = max(0, row_idx - 1)
    max_row_id = min(num_rows, row_idx + 2)
    min_col_id = max(0, col_idx - 1)
    max_col_id = min(num_columns, col_idx + 2)
    adjacent_items = engine_matrix[min_row_id:max_row_id, min_col_id:max_col_id]
    return adjacent_items

def is_character_in_matrix(matrix):
    characterCheck = False
    for row in matrix:
        for item in row:
            if item == 'True':
                characterCheck = True

    return characterCheck

# Now check if there are matching characters next to a number

engine_sum = 0
for row_idx, row in enumerate(engine_matrix):
    last_sum_item = None
    for col_idx, item in enumerate(row):
        if item.isnumeric():
            adjacent_items = find_adjacent_items(row_idx,col_idx)
            if is_character_in_matrix(adjacent_items):
                current_sum_item = int(item)
                if current_sum_item != last_sum_item:
                    engine_sum += current_sum_item
                    last_sum_item = current_sum_item

answerA = engine_sum
# submit(answerA, part="a", day=day, year=year)

### Part B ###

def get_numbers_in_matrix(matrix):
    numbers = []
    for row in matrix:
        for item in row:
            if item.isnumeric():
                numbers.append(int(item))
                numbers= list(dict.fromkeys(numbers))
    return numbers
    
gear_ratio_sum = 0
for row_idx, row in enumerate(engine_matrix):
    last_sum_item = None
    for col_idx, item in enumerate(row):
        # print(item)
        if item == "*":
            #Check if there are characters adjacent
            adjacent_items = find_adjacent_items(row_idx,col_idx)
            numbers = get_numbers_in_matrix(adjacent_items)
            if len(numbers) == 2:
                gear_ratio_sum += numbers[0] * numbers [1]

answerB = gear_ratio_sum
print(answerB)
submit(answerB, part="b", day=day, year=year)