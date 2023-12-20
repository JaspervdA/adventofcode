from aocd import get_data, submit

year, day = 2023, 9
data = get_data(year=year, day=day).splitlines()

# data = ["0 3 6 9 12 15",
# "1 3 6 10 15 21",
# "10 13 16 21 30 45"]

data_formatted = []
for line in data:
    data_formatted.append([int(number) for number in line.split(" ")])

def getDifferences(list_of_values):
    differences = []
    for index, current_value in enumerate(list_of_values):
        if index == 0:
            last_value = current_value
        else:
            differences.append(current_value - last_value)
            last_value = current_value
    return differences

def checkAllZeroes(sequence):
    return all(v == 0 for v in sequence)

# Part A
total_number_A = 0
for sequence in data_formatted:
    new_sequence = sequence
    next_number = 0
    while not checkAllZeroes(new_sequence):
        next_number += new_sequence[-1]
        new_sequence = getDifferences(new_sequence)
    total_number_A += next_number

answerA = total_number_A
print("answer A is ", answerA)
# submit(answerA, part="a", day=day, year=year)

# Part B
total_number_B = 0
for sequence in data_formatted:
    new_sequence = sequence
    new_sequence.reverse()
    previous_number = 0
    while not checkAllZeroes(new_sequence):
        previous_number += new_sequence[-1]
        new_sequence = getDifferences(new_sequence)

    total_number_B += previous_number

answerB = total_number_B
print("answer B is ", answerB)
submit(answerB, part="b", day=day, year=year)