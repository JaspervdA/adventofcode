from aocd import get_data, submit

year, day = 2023, 13
data = get_data(year=year, day=day)
# data = get_data(year=year, day=day).splitlines()

def transposePuzzle(puzzle_rows):
    puzzle_cols = []
    num_cols = len(puzzle_rows[0])
    for x in range(num_cols):
        puzzle_col = ""
        for puzzle_row in puzzle_rows:
            puzzle_col += puzzle_row[x]
        puzzle_cols.append(puzzle_col)

    return puzzle_cols

def checkIfMirror(mirror_row, puzzle_rows):
    #Mirror row is below  mirror
    num_rows_to_check = min(mirror_row, len(puzzle_rows) - mirror_row)
    # Extract rows and check if they match
    top_rows = puzzle_rows[mirror_row - num_rows_to_check:mirror_row]
    bottom_rows = puzzle_rows[mirror_row :mirror_row + num_rows_to_check]
  
    bottom_rows.reverse()

    return top_rows == bottom_rows

def checkPreviousRow(previous_row, row):
    return previous_row == row

puzzles = data.split("\n\n")
score = 0
for puzzle in puzzles:
    puzzle_rows = puzzle.split("\n")
    puzzle_cols = transposePuzzle(puzzle_rows)
    previous_row = []
    previous_col = []
    for row_idx, row in enumerate(puzzle_rows):
        if checkPreviousRow(previous_row, row):
            if checkIfMirror(row_idx, puzzle_rows):
                score += row_idx * 100
            
        previous_row = row
    
    for col_idx, col in enumerate(puzzle_cols):
        if checkPreviousRow(previous_col, col):
            if checkIfMirror(col_idx, puzzle_cols):
                score += col_idx
            
        previous_col = col

answerA = score
print("Answer A", score)
# submit(answerA, part="a", day=day, year=year)


### Part B ###

def checkIfRowsHaveSmudge(row_1, row_2):
    # Check if rows have smudge
    differences = 0
    for r1, r2 in zip(row_1,row_2):
        if r1 != r2:
            differences += 1
    return differences == 1

def checkPreviousRowWithSmudge(previous_row, row):
    # If there is mirroring without a smudge handle this case
    if previous_row == row:
        return True
    
    # If there is mirroring with a smudge, handle that case
    elif checkIfRowsHaveSmudge(previous_row, row):
        return True
    else:
        # No mirroring
        return False

def checkIfMirrorWithSmudge(mirror_row, puzzle_rows):
    #Mirror row is below  mirror
    num_rows_to_check = min(mirror_row, len(puzzle_rows) - mirror_row)
    # Extract rows and check if they match
    top_rows = puzzle_rows[mirror_row - num_rows_to_check:mirror_row]
    bottom_rows = puzzle_rows[mirror_row :mirror_row + num_rows_to_check]
    bottom_rows.reverse()

    smudge_count = 0
    similar_count = 0
    for row_1, row_2 in zip(top_rows, bottom_rows):
        if checkIfRowsHaveSmudge(row_1, row_2):
            smudge_count += 1
        elif row_1 == row_2:
            similar_count += 1
        else:
            continue
    if smudge_count == 1 and (similar_count == num_rows_to_check -1):
        return True
    else:
        return False    

score_B = 0

for puzzle in puzzles:
    puzzle_rows = puzzle.split("\n")
    puzzle_cols = transposePuzzle(puzzle_rows)
    previous_row = []
    previous_col = []
    for row_idx, row in enumerate(puzzle_rows):
        check_previous_row = checkPreviousRowWithSmudge(previous_row, row)
        
        if check_previous_row:
            print("mirroring row", row_idx)
            if checkIfMirrorWithSmudge(row_idx, puzzle_rows):
                score_B += row_idx * 100    
                break
        previous_row = row
    
    for col_idx, col in enumerate(puzzle_cols):
        check_previous_col = checkPreviousRowWithSmudge(previous_col, col)
        if check_previous_col:
            if checkIfMirrorWithSmudge(col_idx, puzzle_cols):
                score_B += col_idx
                break
        previous_col = col

answerB = score_B
# 38389 is incorrect, too high!
# 27406 is incorrect, too low!
print("Answer B", score_B)
# submit(answerB, part="b", day=day, year=year)