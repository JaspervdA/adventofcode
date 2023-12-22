from aocd import get_data, submit

year, day = 2023, 20
data = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".split("\n")
# data = get_data(year=year, day=day).splitlines()

flipflops = {}
conjunctions = {}
for row in data:
    module_name, next_module = row.split(" -> ")
    if row[0] == "b":
        broadcaster_items = row.split(" -> ")[1].split(", ")
    elif row[0] == "%":
        flipflops[module_name[1:]] = [0] + next_module.split(", ")
    elif row[0] == "&":
        conjunctions[module_name[1:]] =  next_module.split(", ")

print(flipflops)  # Flip flops are [on/off, next_module_1 , next_module_2, ..., next_module_N ]
print(conjunctions)

def doFlipflop(pulse):
    if pulse
    next_pulse = pulse %1
    # flipflops[pulse]
    return []

# def doConjunction():

current_pulse_modules = [[item, 0] for item in broadcaster_items]

# Wrap this for loop in a while statement
for pulse_module in current_pulse_module:
    pulse = pulse_module[0]
    module = pulse_module[1]
    next_pulse_modules = []
    if pulse[0] in flipflops:
        next_pulse_modules.append(doFlipflop(pulse, module))
    elif pulse[0] in conjunctions:
        next_pulse_modules.append(doConjunction(pulse, module))
current_pulse_modules = next_pulse_modules
print(next_pulses)


# Flip-flop on/off --> Low pulse flips on/off. If off, turn on and send high pulse
# Conjunction, remember
# Broadcaster send pules to all modules
# Button module

# Pulses are on and off and go t. So a list of []

# Start with the broadcaster

def broadcast(broadcaster):
    module=1
    return module

# Untill there are no more pulses left




# low_pulses_sent = X
# high_pulses_sent = Y

#answerA = low_pulses_sent * high_pulses_sent
# print("Answer A", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)