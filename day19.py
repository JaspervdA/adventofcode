from aocd import get_data, submit

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
        
        # This handles the case if a workflow was already visited
        if new_workflow in seen_workflows:
            go_to_next_worflow, part_accepted = False, False
        #  This handles the case if there is an R or A after the rule, i.e. a>1716:R
        if new_workflow == "A":
            go_to_next_worflow, part_accepted = False, True
        elif new_workflow == "R":
            go_to_next_worflow, part_accepted = False, False

        current_workflow = new_workflow
    if part_accepted:
        accepted_part_sums.append(sum(rating))

total_sum = sum(accepted_part_sums)
answerA = total_sum
print("Answer A is", answerA)
submit(answerA, part="a", day=day, year=year)

### Part B ###


# String all conditions together, for instance we could get s<1351, a<2006, x<1416:A

# To string together, loop over the combined workflows. Start at in
# Subsitute the result part after : 
# loop over the new combined workflows

# Get the min and max condition, min is where there is a > operator, max is where there is a < operator

# Then we get the number of feasible combinations:
# (x_max - x_min - 1 ) * (m_max - m_min - 1 ) * (a_max - a_min -1 ) * (s_max - s_min - 1 )

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)