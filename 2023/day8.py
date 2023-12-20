from aocd import get_data, submit

year, day = 2023, 8

data = get_data(year=year, day=day).splitlines()

# data = ["LR",
# "",
# "11A = (11B, XXX)",
# "11B = (XXX, 11Z)",
# "11Z = (11B, XXX)",
# "22A = (22B, XXX)",
# "22B = (22C, 22C)",
# "22C = (22Z, 22Z)",
# "22Z = (22B, 22B)",
# "XXX = (XXX, XXX)"
# ]

# Format the data to a dict
leftright_list = data[0]
data_dict = {}
for line in data[2:]:
    key, values = line.split(" = ")
    left, right = values.split(", ")
    data_dict[key] =  [left[1:], right[:-1]]

current_element = "AAA"
# current_element = "11A"

def runSequence(leftright_list, current_element):
    for step_count, letter in enumerate(leftright_list):
        if letter == "L":
            current_element = data_dict[current_element][0]
        elif letter == "R":
            current_element = data_dict[current_element][1]
        else:
            print('Something is going wrong...')
        
        if current_element == "ZZZ":
            return current_element, step_count + 1

    return current_element, step_count + 1

step_count = 0
for i in range(100):
    new_element, additional_steps = runSequence(leftright_list, current_element)
    step_count += additional_steps
    current_element = new_element
    if new_element == "ZZZ":
        break

answerA = step_count
# print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Get starting nodes
starting_keys = []
for key in data_dict:
    if key[-1] == "A":
        starting_keys.append(key)

def checkCurrentKey(current_key):
    check = True
    if current_key[-1] != "Z":
        check = False
    return check

def getNewElement(letter, current_element):
    if letter == "L":
        new_element = data_dict[current_element][0]
    elif letter == "R":
        new_element = data_dict[current_element][1]
    else:
        print('Something is going wrong...')
    return new_element

def runSequence(leftright_list, current_key):
    for step_count, letter in enumerate(leftright_list):
        current_key = getNewElement(letter, current_key)
        if checkCurrentKey(current_key):
            return current_key, step_count + 1
        
    return current_key, step_count + 1


loop_size = 10000
steps_needed = []
for current_key in starting_keys:
    total_steps = 0
    for i in range (loop_size):
        current_key, additional_steps = runSequence(leftright_list, current_key)
        total_steps += additional_steps
        print('total steps', total_steps)
        if checkCurrentKey(current_key):
            steps_needed.append(total_steps)    
            break

print(steps_needed)
#  Deze heb ik niet, in Wolfram gegooid
# answerB = lcm(steps_needed)
answerB = 8811050362409
print("Answer B is", answerB)

submit(answerB, part="b", day=day, year=year)