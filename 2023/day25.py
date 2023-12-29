from aocd import get_data, submit
import copy

year, day = 2023, 25
data = get_data(year=year, day=day).splitlines()

wire_dict, all_wires, total_wires = {}, [], 0
for row in data:
    left, right = row.split(": ")
    all_wires.extend([left] + right.split(" "))
    total_wires += len(right.split(" "))

all_wires = list(set(all_wires))
for wire in all_wires: wire_dict[wire]= []
for row in data:
    left, right = row.split(": ")
    right_items = right.split(" ")
    wire_dict[left].extend(right_items)
    for right_item in right_items:
        wire_dict[right_item].append(left)

def removeWiresFromDict(remove_wire_dict, wire_list):
    cut_wire_dict = copy.deepcopy(remove_wire_dict)
    for wire in wire_list:
        cut_wire_dict[wire[0]].remove(wire[1]), cut_wire_dict[wire[1]].remove(wire[0])
    return cut_wire_dict

def getConnectedNodesN(start_node, search_wire_dict, N_layers):
    current_connected_nodes, all_connected_nodes, N = [start_node], [start_node], 0
    while len(current_connected_nodes) > 0 and N < N_layers:
        N += 1
        next_connected_nodes = []
        for connected_node in current_connected_nodes:
            new_connected_nodes = search_wire_dict[connected_node]
            for node in new_connected_nodes:
                if node not in all_connected_nodes:
                    all_connected_nodes.append(node), next_connected_nodes.append(node)
        current_connected_nodes = next_connected_nodes
    return all_connected_nodes

def getSimilarNodes(left_nodes, right_nodes):
    similar_count = 0
    for left_node in left_nodes:
        if left_node in right_nodes:
            similar_count += 1
    return similar_count

def getAllConnectedNodes(start_node, search_wire_dict):
    current_connected_nodes, all_connected_nodes = [start_node], [start_node]
    while len(current_connected_nodes) > 0:
        next_connected_nodes = []
        for connected_node in current_connected_nodes:
            new_connected_nodes = search_wire_dict[connected_node]
            for node in new_connected_nodes:
                if node not in all_connected_nodes:
                    all_connected_nodes.append(node), next_connected_nodes.append(node)
        current_connected_nodes = next_connected_nodes
    return all_connected_nodes

# search_N, simliar_node_threshold = 2, 3 # Use this for the dummy data
search_N, simliar_node_threshold = 4, 3 # Use this for the real data
seen_combinations, similar_nodes, three_wires_to_cut = [], [], []
for wire, connected_wires in wire_dict.items():
    combinations = [[wire, conn_wire] for conn_wire in connected_wires]
    for combination in combinations:
        reverse_combination = [combination[1], combination[0]]
        if combination not in seen_combinations and reverse_combination not in seen_combinations:
            seen_combinations.append(combination)
            cut_wire_dict = removeWiresFromDict(wire_dict, [combination])
            left_nodes = getConnectedNodesN(combination[0], cut_wire_dict, search_N)
            right_nodes = getConnectedNodesN(combination[1], cut_wire_dict, search_N)
            similar_nodes.append(getSimilarNodes(left_nodes, right_nodes))

for combi, similar_count in zip(seen_combinations, similar_nodes):
    if similar_count < simliar_node_threshold:
        three_wires_to_cut.append(combi)

cut_wire_dict = removeWiresFromDict(wire_dict, three_wires_to_cut)
wires_left, wires_right = getAllConnectedNodes(three_wires_to_cut[0][0], cut_wire_dict), getAllConnectedNodes(three_wires_to_cut[0][1], cut_wire_dict)
answerA = len(wires_left) * len(wires_right)
print("Answer A is", answerA)
submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)