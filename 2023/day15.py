from aocd import get_data, submit

year, day = 2023, 15
data = get_data(year=year, day=day).split(",")
# data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")

def getNextValue(current_value, char):
    current_value = 17 * (current_value + ord(char))
    return current_value % 256

def stringToNumber(string):
    current_value = 0
    for char in string:
        current_value = getNextValue(current_value, char)
    return current_value

numbers = []
for line in data:
    numbers.append(stringToNumber(line))

answerA = sum(numbers)
# print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

def splitLine(line):
    focal_length = None
    if line[-1] == "-":
        operation = "-"
        label = line[:-1]
    elif line[-2] == "=":
        operation = "="
        label, focal_length = line.split(operation)
    label_id = stringToNumber(label)
    return label, label_id, operation, focal_length

### Part B ###
possible_box_numbers = []
for line in data:
    label, label_id, operation, focal_length = splitLine(line)
    possible_box_numbers.append(label_id)

# Initiate the empty boxes
boxes = [[] for i in range(max(possible_box_numbers)+1)]

def checkIfLabelInBox(box, label):
    box_label_id = -1
    for idx, box_item in enumerate(box):
        if box_item[0] == label:
            box_label_id = idx
            break
    
    return box_label_id

for line in data:
    label, label_id, operation, focal_length = splitLine(line)
    if operation == "=":
        # If the label in this box exists replace by new label
        box_label_id = checkIfLabelInBox(boxes[label_id], label)
        if  box_label_id > -1:
            boxes[label_id][box_label_id] = [label, focal_length]
        else:
            # If the label in this box does not exist, add the lens to the end of the box
            boxes[label_id].append([label, focal_length])
    elif operation == "-":
        # If the label in this box exists, remove the lens
        box_label_id = checkIfLabelInBox(boxes[label_id], label)
        if box_label_id > -1:
            # Move other items in the box to the left!
            boxes[label_id].pop(box_label_id)
    else:
        print("Unknown operation, something is going wrong")

total_focusing_power = 0
for box_id, box in enumerate(boxes):
    for slot_id, slot in enumerate(box):
        total_focusing_power += (box_id +1) * (slot_id +1) * int(slot[1])



answerB = total_focusing_power
print("Answer B is", answerB)
submit(answerB, part="b", day=day, year=year)
        