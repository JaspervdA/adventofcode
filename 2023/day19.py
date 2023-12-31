from aocd import get_data, submit
import copy 
import math

year, day = 2023, 19

data = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".split("\n")
data = get_data(year=year, day=day).splitlines()

workflows, ratings, at_ratings = {}, [], False
for row in data:
    if len(row) == 0:
        at_ratings = True
        continue
    if at_ratings:
        rating_unformatted = row[1:-1].split(",")
        rating_formatted = [int(r[2:]) for r in rating_unformatted]
        ratings.append(rating_formatted)
        
    else:
        name, workflow_not_parsed = row.split("{")
        workflows[name] =  workflow_not_parsed[:-1].split(",")

def checkRatingRule(rule, rating):
    if rule.find(":") == -1:
        # No rule to check, return next item
        return False, rule
    
    rule_logic, rule_result = rule.split(":")
    
    if rule_logic[0] == "x":
        rating_item = 0
    elif rule_logic[0] == "m":
        rating_item = 1
    elif rule_logic[0] == "a":
        rating_item = 2
    elif rule_logic[0] == "s":
        rating_item = 3
    else:
        print("Unkown rule", rule)

    if rule_logic[1] == ">":
        # If the role logic is matched go to the next workflow
        if rating[rating_item] > int(rule_logic[2:]):
            check_next_rule_in_workflow, next_workflow  = False, rule_result
        # Otherwise check the next rules
        else:
            check_next_rule_in_workflow, next_workflow  = True, None
    elif rule_logic[1] == "<":
        # If the role logic is matched go to the next workflow
        if rating[rating_item] < int(rule_logic[2:]):
            check_next_rule_in_workflow, next_workflow  = False, rule_result
        # Otherwise check the next rules
        else:
            check_next_rule_in_workflow, next_workflow  = True, None
    
    return check_next_rule_in_workflow, next_workflow

# rfg{s<537:gd,x>2440:R,A}
def doWorkflow(workflow, rating):
    for rule in workflows[workflow]:
        check_next_rule_in_workflow = True
        if rule[0] == "A":
            return None, False, True
        elif rule[0] =="R":
            return None, False, False
        else:
            next_rule = rule
            check_next_rule_in_workflow, next_workflow = checkRatingRule(next_rule, rating)
            if check_next_rule_in_workflow:
                continue
            else:
                return next_workflow, True, False

    return next_workflow, False, False

accepted_part_sums = []
for rating in ratings:
    current_workflow, go_to_next_worflow, part_accepted, seen_workflows = "in", True, False, []
    while go_to_next_worflow:
        seen_workflows.append(current_workflow)
        new_workflow, go_to_next_worflow, part_accepted = doWorkflow(current_workflow, rating)
        if new_workflow in seen_workflows:
            go_to_next_worflow, part_accepted = False, False
        if new_workflow == "A":
            go_to_next_worflow, part_accepted = False, True
        elif new_workflow == "R":
            go_to_next_worflow, part_accepted = False, False

        current_workflow = new_workflow
    if part_accepted:
        accepted_part_sums.append(sum(rating))

total_sum = sum(accepted_part_sums)
answerA = total_sum
# print("Answer A is", answerA)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

def getNextWorkflows(workflow):
    conditionals, next_workflows = [], []
    for item in workflow:
        if item.find(":") > -1:
            conditional, next_workflow = item.split(":")
        else:
            conditional, next_workflow = '', item
        next_workflows.append(next_workflow)
        conditionals.append(conditional)
    return conditionals, next_workflows

def getNotConditional(conditional):
    if conditional.find(">") > -1:
        letter, threshold = conditional.split(">")
        not_conditional = f"{letter}<{int(threshold)+1}"
    elif conditional.find("<") > -1:
        letter, threshold = conditional.split("<")
        not_conditional = f"{letter}>{int(threshold)-1}"
    return not_conditional

def lettersInString(conditional_string):
    evaluate_string, letters = copy.deepcopy(conditional_string), []
    if (evaluate_string.find("x") > -1): letters.append("x")
    if (evaluate_string.find("m") > -1): letters.append("m")
    if (evaluate_string.find("s") > -1): letters.append("s")
    if (evaluate_string.replace("and", " ").find("a") > -1): letters.append("a")
    return letters

def applyConditionals(workflow_conditional, new_conditionals, new_workflows):
    not_conditional, next_workflow_conditionals, next_accept_conditionals, next_reject_conditionals = "", [], [], []
    
    for new_conditional, new_workflow in zip(new_conditionals, new_workflows):
        current_conditional = workflow_conditional['conditional']
        if len(new_conditional) > 0:
            next_conditional = current_conditional + " and " + new_conditional if len(current_conditional) > 0 else new_conditional
            next_plus_not_conditional = next_conditional + " and " + not_conditional if len(not_conditional) > 0 else next_conditional
            if new_workflow == "A":
                next_accept_conditionals.append(next_plus_not_conditional)    
            elif new_workflow == "R":
                next_reject_conditionals.append(next_plus_not_conditional)
            else:
                #This is the case if we go to a new workflow but with an extra conditional
                next_workflow_conditionals.append({'workflow': new_workflow, 'conditional': next_plus_not_conditional})
            next_not_conditional = getNotConditional(new_conditional)
            not_conditional = not_conditional + " and " + next_not_conditional if len(not_conditional) > 0 else next_not_conditional
        else:
            current_plus_and_conditional = current_conditional + " and " if len(current_conditional) > 0 else current_conditional
            current_plus_not_conditional = current_plus_and_conditional + not_conditional if len(not_conditional) > 0 else current_conditional
            if new_workflow =="A":
                next_accept_conditionals.append(current_plus_not_conditional)    
            elif new_workflow == "R":
                next_reject_conditionals.append(current_plus_not_conditional)
            else:
                #This is the case if we go to a new workflow but without an extra conditional
                next_workflow_conditionals.append({'workflow': new_workflow, 'conditional': current_plus_not_conditional})

    return next_workflow_conditionals, next_accept_conditionals, next_reject_conditionals

# String all the conditionals together
start_workflow_conditional = {"workflow": "in", "conditional": ""}
current_workflow_conditionals, accept_conditionals, reject_conditionals = [start_workflow_conditional], [], []
while len(current_workflow_conditionals) > 0:
    new_workflow_conditionals = []
    for workflow_conditional in current_workflow_conditionals:
        next_conditionals, next_workflows = getNextWorkflows(workflows[workflow_conditional['workflow']])
        next_workflow_conditionals, next_accept_conditionals, next_reject_conditionals = applyConditionals(workflow_conditional, next_conditionals, next_workflows)
        new_workflow_conditionals.extend(next_workflow_conditionals), accept_conditionals.extend(next_accept_conditionals), reject_conditionals.extend(next_reject_conditionals)
    current_workflow_conditionals = new_workflow_conditionals

# Get the number of combinations for these conditionals
all_num_combinations = []
for accepted_conditional in accept_conditionals:
    conditionals = accepted_conditional.split(' and ')
    letters_in_string = lettersInString(accepted_conditional)
    num_combinations, letter_conditionals = 1, []
    for letter in letters_in_string:
        letter_conditional, count = "", 0
        for conditional in conditionals:
            if conditional[0] == letter:
                letter_conditional = letter_conditional + " and " + conditional if count > 0 else conditional
                count += 1
        letter_conditionals.append(letter_conditional)

    letter_accepted_scores = [4000, 4000, 4000, 4000]
    for letter_idx, (letter, letter_conditional) in enumerate(zip(letters_in_string, letter_conditionals)):
        letter_accepted_score = 0
        for i in range(1,4001):
            exec(f"{letter} = {i}")
            if eval(letter_conditional):
                letter_accepted_score +=1
        letter_accepted_scores[letter_idx] = letter_accepted_score
    all_num_combinations.append(math.prod(letter_accepted_scores))

# Write your code here
answerB = sum(all_num_combinations)
print("Answer B is", answerB)
submit(answerB, part="b", day=day, year=year)