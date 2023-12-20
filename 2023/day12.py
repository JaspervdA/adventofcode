from aocd import get_data, submit
import re
import scipy.special
import math

year, day = 2023, 12
data = get_data(year=year, day=day).splitlines()

data = ['???.### 1,1,3',
'.??..??...?##. 1,1,3',
'?#?#?#?#?#?#?#? 1,3,1,6',
'????.#...#... 4,1,1', 
'????.######..#####. 1,6,5',
'?###???????? 3,2,1',
"..???.??.? 1,1,1"
]

#Part B data
data = ['???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3', #1 arrangement
'.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##. 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3', # 16384 arrangements
'?#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#? 1,3,1,6,1,3,1,6,1,3,1,6,1,3,1,6,1,3,1,6', # 1 arrangements (this works!)
'????.#...#...?????.#...#...?????.#...#...?????.#...#...?????.#...#...???? 4,1,1,4,1,1,4,1,1,4,1,1,4,1,1',  # 16 arrangements (this works!)
'????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####. 1,6,5,1,6,5,1,6,5,1,6,5,1,6,5',  #2500 arrangements
'?###??????????###??????????###??????????###??????????###???????? 3,2,1,3,2,1,3,2,1,3,2,1,3,2,1', # 506250 arrangements
]

def removeDots(spring_conditions):
    if len(spring_conditions) == 0:
        return spring_conditions

    remove_trailing_dots = True
    while remove_trailing_dots:
        remove_trailing_dots = False
        if spring_conditions[0] ==".":
            spring_conditions = spring_conditions[1:]
            remove_trailing_dots = True
        if len(spring_conditions) == 0:
            break
        if spring_conditions[-1] ==".":
            spring_conditions = spring_conditions[:-1]
            remove_trailing_dots = True
    spring_conditions = re.sub(r'\.+', '.', spring_conditions)
    return spring_conditions


# Hoe te algemeniseren?
# Vind de posities van de eerste #

def removeLeadingHashtags(spring_conditions, spring_groups):
    removing = False
    if len(spring_conditions) == 0:
        return spring_conditions, spring_groups, removing
    
    if len(spring_groups) == 0:
        return spring_conditions, spring_groups, removing
    first_spring_group = spring_groups[0]
    
    if spring_conditions[0] == "#":
        # Als de eerste char een hasthag is dan is dit altijd de eerste hashtag en kunnen we die verwijderen, bijv. ###??? wordt ??
        spring_conditions = spring_conditions[first_spring_group + 1 :]
        removing = True
        spring_groups.pop(0)
        return spring_conditions, spring_groups, removing
    
    if len(spring_conditions) == 1:
        removing = False
        return spring_conditions, spring_groups, removing

    if spring_conditions[1] == '#':
        if first_spring_group == 1: 
            # Als het een enkele hashtag op plek 1 is eerste 3 getallen weghalen
            spring_conditions = spring_conditions[first_spring_group + 2 :]
            removing = True
            spring_groups.pop(0)
            return spring_conditions, spring_groups, removing
        #  Bit hacky elif to make sure we do not get stucky literally copy code from the else statement later on
        elif len(spring_conditions) < first_spring_group + 2:
            potential_spring = spring_conditions[1 : 1 + first_spring_group]
            last_hashtag = potential_spring.rfind('#')
            hashtag_length = last_hashtag + 1
            if hashtag_length == first_spring_group:
                # Als de lengte van char 1 tot laatste # zelfde is als spring_group dan hele weghalen Bijv. ?#?#??? met first spring group 3 wordt ??
                spring_conditions = spring_conditions[first_spring_group + 2 :]
                removing = True
                spring_groups.pop(0)
                return spring_conditions, spring_groups, removing
            else:
                # Zo niet gaan we de hashtags inkorten bijv. ?##?? met first spring group 3. Dan willen we naar ??? met first spring group 1
                spring_groups[0] -= (hashtag_length)
                removing = True
                spring_conditions = spring_conditions[:1] + spring_conditions[hashtag_length + 1 :]
                return spring_conditions, spring_groups, removing
        elif spring_conditions[first_spring_group + 1] == "#":
            # This is the "blocker" scenario where the #s must start at first ?. For instance ?#??#??# with length 6 we know the first 6 chars are what we want and 7h is a . so remove first 5 characters!
            spring_conditions = spring_conditions[first_spring_group + 1 :]
            removing = True
            spring_groups.pop(0)
            return spring_conditions, spring_groups, removing
        
        else:
            potential_spring = spring_conditions[1 : 1 + first_spring_group]
            last_hashtag = potential_spring.rfind('#')
            hashtag_length = last_hashtag + 1
            if hashtag_length == first_spring_group:
                # Als de lengte van char 1 tot laatste # zelfde is als spring_group dan hele weghalen Bijv. ?#?#??? met first spring group 3 wordt ??
                spring_conditions = spring_conditions[first_spring_group + 2 :]
                removing = True
                spring_groups.pop(0)
                return spring_conditions, spring_groups, removing
            else:
                # Zo niet gaan we de hashtags inkorten bijv. ?##?? met first spring group 3. Dan willen we naar ??? met first spring group 1
                spring_groups[0] -= (hashtag_length)
                removing = True
                spring_conditions = spring_conditions[:1] + spring_conditions[hashtag_length + 1 :]
                return spring_conditions, spring_groups, removing
            
    return spring_conditions, spring_groups, removing


def removeTrailingHashtags(spring_conditions, spring_groups):
    removing = False
    if len(spring_conditions) == 0:
        return spring_conditions, spring_groups, removing

    if len(spring_groups) == 0:
        removing = False
        return spring_conditions, spring_groups, removing
    
    last_spring_group = spring_groups[-1]
    
    if spring_conditions[-1] == "#":
        # Als de eerste char een hasthag is dan is dit altijd de laatste hashtag en kunnen we die verwijderen
        spring_conditions = spring_conditions[:-last_spring_group -1]        
        removing = True
        spring_groups.pop()
        return spring_conditions, spring_groups, removing
    
    if len(spring_conditions) == 1:
        removing = False
        return spring_conditions, spring_groups, removing
    
    if spring_conditions[-2] == "#":
        if last_spring_group == 1:
            # Als het een enkele hashtag op een na laatste positie is laastse 3 getallen weghalen
            spring_conditions = spring_conditions[: -2 - last_spring_group]
            removing = True
            spring_groups.pop() 
            return spring_conditions, spring_groups, removing
        #  Bit hacky elif to make sure we do not get stucky literally copy code from the else statement later on
        elif len(spring_conditions) < last_spring_group + 2:
            potential_spring = spring_conditions[-1 - last_spring_group: -1]
            first_hashtag = potential_spring.find('#')
            hashtag_length = last_spring_group - first_hashtag
            if hashtag_length == last_spring_group:
                # Als de lengte van char 1 tot laatste # zelfde is als spring_group dan hele weghalen Bijv. ???#?#? met last spring group 3 wordt ??
                spring_conditions = spring_conditions[: -2 - last_spring_group]
                removing = True
                spring_groups.pop()
                return spring_conditions, spring_groups, removing            
            else:
                # Zo niet gaan we de hashtags inkorten bijv. ??##? met last spring group 3. Dan willen we naar ??? met last spring group 1
                spring_groups[-1] -= (hashtag_length)
                removing = True
                spring_conditions = spring_conditions[:-hashtag_length - 1] + spring_conditions[-1]
                return spring_conditions, spring_groups, removing  
        elif spring_conditions[-2 - last_spring_group ] == "#":
            # This is the "blocker" scenario where the #s must start at first ?. For instance #??#??#? with length 6 we know the last 6 chars are what we want and 7h is a . so remove last 7 characters!
            spring_conditions = spring_conditions[:-last_spring_group -1]
            removing = True
            spring_groups.pop()
            return spring_conditions, spring_groups, removing
        else:
            potential_spring = spring_conditions[-1 - last_spring_group: -1]
            first_hashtag = potential_spring.find('#')
            hashtag_length = last_spring_group - first_hashtag
            if hashtag_length == last_spring_group:
                # Als de lengte van char 1 tot laatste # zelfde is als spring_group dan hele weghalen Bijv. ???#?#? met last spring group 3 wordt ??
                spring_conditions = spring_conditions[: -2 - last_spring_group]
                removing = True
                spring_groups.pop()
                return spring_conditions, spring_groups, removing            
            else:
                # Zo niet gaan we de hashtags inkorten bijv. ??##? met last spring group 3. Dan willen we naar ??? met last spring group 1
                spring_groups[-1] -= (hashtag_length)
                removing = True
                spring_conditions = spring_conditions[:-hashtag_length - 1] + spring_conditions[-1]
                return spring_conditions, spring_groups, removing     

    return spring_conditions, spring_groups, removing


def springGroupLength(spring_counts):
    length = []
    cumsum = 0
    for idx, s in enumerate(spring_counts):
        cumsum += s + idx
        length.append(cumsum)

    return length

def getFeasibleSpringGroups(spring_groups, question_len):
    feasible_spring_groups_id = 0 
    for spring_idx, spring_length in enumerate(springGroupLength(spring_groups)):
        # Bij deze opties moeten we nog van links naar rechts gaan kijken en spring counts weggooien
        if spring_length > question_len:
            #Not feasible, stop the loop.
            break
        else:
            feasible_spring_groups_id = spring_idx + 1
        
    return spring_groups[0:feasible_spring_groups_id]

total_permutations = 0
permutations = []
i = 0
for row in data[0:1]:
    i += 1
    spring_conditions, spring_groups = row.split(" ")
    spring_groups = spring_groups.split(",")
    spring_groups = [int(i) for i in spring_groups]
    removing = True
    print("Row number", i)
    print(spring_conditions)
    print(spring_groups)

    while removing:
        spring_conditions = removeDots(spring_conditions)
        spring_conditions, spring_groups, removing_leading = removeLeadingHashtags(spring_conditions, spring_groups)
        spring_conditions, spring_groups, removing_trailing = removeTrailingHashtags(spring_conditions, spring_groups)
        removing = removing_leading or removing_trailing

    # De string is nu helemaal goed opgeschoond, nu moeten we nog het aantal "vrijheidsgraden" berekenen!
    print(spring_conditions)
    print(spring_groups)
    question_groups = spring_conditions.split(".")
    group_permutations = []

    # ???.??.?

    for group in question_groups:
        question_len = len(group)
        if question_len == 0:
            num_permutations = 1
        else:
            # Get feasible spring groups moet verbeterd worden. We gooien nu geen spring counts weg!
            feasible_spring_groups = getFeasibleSpringGroups(spring_groups, question_len)
            # Je kan de punten tussen hashtags wegdenken in de groepen
            # De lengte van de virtuele string is dan len(vraagtekens) - (len(spring_groups) -1)
            spring_group_extra_numbers = sum(feasible_spring_groups) - len(feasible_spring_groups)
            binominal_size = question_len - (spring_group_extra_numbers) -  (len(feasible_spring_groups) -1)
            # print(binominal_size, len(spring_groups))
            # Het aantal combinaties is dan: de binominaal int(scipy.special.comb(lengte_string, len(spring_groups)))
            num_permutations = int(scipy.special.comb(binominal_size, len(feasible_spring_groups)))
            group_permutations.append(num_permutations)
    
    total_group_permutations = math.prod(group_permutations)
    permutations.append(total_group_permutations)
    total_permutations += total_group_permutations
        

print(permutations)
print(total_permutations)


#answerA = total_permutations
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)