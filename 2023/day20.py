from aocd import get_data, submit
import copy
import math

year, day = 2023, 20
data = get_data(year=year, day=day).splitlines()

flipflops = {}
conjunctions = {}
for row in data:
    module_name, next_module = row.split(" -> ")
    if row[0] == "b":
        broadcaster_items = row.split(" -> ")[1].split(", ")
    elif row[0] == "%":
        flipflops[module_name[1:]] = [0] + next_module.split(", ")
    elif row[0] == "&":
        conjunctions[module_name[1:]] = [{}] + next_module.split(", ") 

for conjunction_name, conjunction in conjunctions.items():
    for module_name in conjunction[1:]:
        if module_name in conjunctions:
            conjunctions[module_name][0][conjunction_name] = 0

for flipflop_name, flipflop in flipflops.items():
    for module_name in flipflop[1:]:
        if module_name in conjunctions:
            conjunctions[module_name][0][flipflop_name] = 0

def doFlipflop(pulse, module):
    flipflop_state, flipflop_next_modules = flipflops[module][0], flipflops[module][1:]
    if pulse == 1:
        return []
    elif pulse == 0:
        flipflops[module][0] = (flipflop_state + 1) % 2
        return [[module, (flipflop_state + 1) % 2, next_module] for next_module in flipflop_next_modules]

def doConjunction(sending_module, pulse, receiving_module):
    conjunctions[receiving_module][0][sending_module] = pulse
    conjunction_all_high = True
    for input_value in conjunctions[receiving_module][0].values():
        if input_value == 0:
            conjunction_all_high = False
            break
    next_pulse = 0 if conjunction_all_high else 1
    conjunction_next_modules = conjunctions[receiving_module][1:]
    return [[receiving_module, next_pulse, next_module] for next_module in conjunction_next_modules]
    
# The current pulse modules are ["sending_module_name", pulse high/low, "next_module_name"] for instance ["broadcaster", 0, "a"]
def pushButton(iteration, low_pulse_count):
    # print(f"Pushing the button, iteration {iteration+1}")
    return [["broadcaster", 0, item] for item in broadcaster_items], low_pulse_count  + 1

def checkIfCycleCompleted():
    for initial_flipflop, flipflop in zip(initial_flipflop_state.values(), flipflops.values()):
        if initial_flipflop != flipflop:
            return False
    for initial_conjunction, conjunction in zip(initial_conjunction_state.values(), conjunctions.values()):
        if initial_conjunction != conjunction:
            return False
    return True

initial_conjunction_state = copy.deepcopy(conjunctions)
initial_flipflop_state = copy.deepcopy(flipflops)

total_button_pushes = 100000
low_pulse_counts, high_pulse_counts = 0, 0
all_rx_inputs_found = False
rx_inputs = ["nd", "pc", "vd", "tx"]
rx_inputs_found = [False, False, False, False]
rx_inputs_found_iteration = [None, None, None, None]
for i in range(total_button_pushes):
    if all_rx_inputs_found:
        break
    low_pulse_count, high_pulse_count = 0, 0
    current_pulse_modules, low_pulse_count = pushButton(i, low_pulse_count)
    while len(current_pulse_modules) > 0:
        next_pulse_modules = []
        for pulse_module in current_pulse_modules:
            sending_module_name = pulse_module[0]
            pulse = pulse_module[1]
            if pulse == 0:
                low_pulse_count += 1
            elif pulse ==1:
                high_pulse_count += 1
        
            receiving_module_name = pulse_module[2]
            for input_idx, (rx_input, found) in enumerate(zip(rx_inputs, rx_inputs_found)):
                if receiving_module_name == rx_input and pulse == 0 and not found:
                    rx_inputs_found_iteration[input_idx] = i + 1
                    rx_inputs_found[input_idx] = True
            if all(rx_inputs_found):
                all_rx_inputs_found = True
            if receiving_module_name in flipflops:
                next_pulse_modules.extend(doFlipflop(pulse, receiving_module_name))
            elif receiving_module_name in conjunctions:
                next_pulse_modules.extend(doConjunction(sending_module_name, pulse, receiving_module_name))
        current_pulse_modules = next_pulse_modules
    low_pulse_counts += low_pulse_count
    high_pulse_counts += high_pulse_count

    if checkIfCycleCompleted():
        cycle_length = i + 1
        # break

answerA = low_pulse_counts * high_pulse_counts
# submit(answerA, part="a", day=day, year=year)

### Part B ###

print(rx_inputs_found_iteration)
# Wolframapha, least common multiple for [4019, 3881, 3767, 3769]
answerB = 221453937522197

print("Answer B is", answerB)

submit(answerB, part="b", day=day, year=year)