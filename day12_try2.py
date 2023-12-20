from aocd import get_data, submit
import scipy
import re

year, day = 2023, 12
data = get_data(year=year, day=day).splitlines()

data = ['???.### 1,1,3', # 1  arrangements (this works!)
'.??..??...?##. 1,1,3', # 4 arrangements (this works!)
'?#?#?#?#?#?#?#? 1,3,1,6', # 1 arrangements
'????.#...#... 4,1,1',  #1 arrangements (this works!)
'????.######..#####. 1,6,5', # 4 arrangements (this works!)
'?###???????? 3,2,1', # 10 arrangements
"..???.??.? 1,1,1" # 9 arrangements (this works!)
]

def springCountsSpace(spring_counts):
    return sum(spring_counts) + len(spring_counts)

def springGroupIsFeasible(group, spring_counts):
    length_needed = sum(spring_counts) + len(spring_counts) - 1
    if length_needed > len(group):
        return False
    else:
        return True

def getFeasibleSpringGroups(group, current_spring_counts):
    # Dummy data in comments for this example "..???.??.? 1,1,1"
    # getFeasibleSpring Groups returns an array of arrays of feasible spring counts and corresponding next_spring_counts
    # For instance [[1,1],[1]] and [[1],[1,1]] on loop 1
    # Deze functie nog fixen, dan zou het moeten werken (na hoop debuggen waarschijnlijk...)
    
    # Begin bij [] als feasible_spring counts en schuif de andere door
    num_spring_counts = len(current_spring_counts)
    feasible_spring_counts = []
    new_spring_counts = []
    for i in range(num_spring_counts + 1):
        test_spring_counts = current_spring_counts[0:i]
        next_spring_counts = current_spring_counts[i:]
        if springGroupIsFeasible(group, test_spring_counts):
            feasible_spring_counts.append(test_spring_counts)
            new_spring_counts.append(next_spring_counts)
    return feasible_spring_counts, new_spring_counts

def getNumPermutations(group, spring_counts):
    question_len = len(group)
    num_spring_counts = len(spring_counts)
    # Je kan de punten tussen hashtags wegdenken in de groepen
    # De lengte van de virtuele string is dan len(vraagtekens) - (len(spring_groups) -1)
    # Het aantal combinaties is dan: de binominaal int(scipy.special.comb(lengte_string, len(spring_groups)))
    spring_group_extra_numbers = sum(spring_counts) - num_spring_counts
    binominal_size = question_len - (spring_group_extra_numbers) -  (num_spring_counts -1)
    num_permutations = int(scipy.special.comb(binominal_size, num_spring_counts))
    return num_permutations

def solveGroupWithHashtags(group, spring_counts, current_score, next_group_input_branches):
    print("solving group with hashtags", group, spring_counts)
    new_groups, new_spring_counts, new_scores = [], [], []
    
    # Input the score of this branch and the new set of spring counts format [[group_remaining, score, spring_counts_remaining]]
    group_loop_branches = [[group, current_score, spring_counts]]
    for branch_data in group_loop_branches:
        group_remaining = branch_data[0]
        loop_score = branch_data[1]
        spring_counts_remaining = branch_data[2]      
        # In de replace hashtag functie gaat nog e.e.a. mis!
        new_groups, new_scores, new_spring_counts = replaceLeftHashtag(group_remaining, spring_counts_remaining)
        print(new_groups, new_scores, new_spring_counts)
        for feasible_group, feasible_score, feasible_sprint_count in zip(new_groups, new_scores, new_spring_counts):
            # if not springGroupIsFeasible(feasible_group, feasible_sprint_count):
            #     return [],[],[]
            loop_score *= feasible_score
            if len(feasible_sprint_count) == 0 and (feasible_group.find("#") == -1):
                branch_scores.append(loop_score)
            elif (feasible_group.find("#") == -1):
                next_group_input_branches.append([loop_score, new_spring_counts])
            else:
                group_loop_branches.append([feasible_group, loop_score, feasible_sprint_count])  
    
    group_loop_branches = next_group_input_branches

    return new_groups, new_spring_counts, new_scores


def replaceLeftHashtag(group, spring_counts):
    hashtag_position = group.find("#")
    new_groups, new_spring_counts, new_scores = [], [], []

    # Hier gaat nog e.e.a. mis. Bijv. left en right space needed klopt niet, want de spring counts kunnen doorschuiven. 
    # Hoe dan wel? Eigenlijk net als in zonder hashtags, pak alle nieuwe spring counts en kijk dan welke feasible zijn.
    for spring_idx, spring_count in enumerate(spring_counts):
        left_spring_counts = spring_counts[:spring_idx]
        right_spring_counts = spring_counts[(spring_idx+1):]
        left_space_needed = springCountsSpace(left_spring_counts)
        right_space_needed = springCountsSpace(right_spring_counts)
        print(left_space_needed, right_space_needed)
        for i in range(spring_count):
            # We schuiven de spring van links naar rechts
            # Hier nog rekening houden met lengte van de spring!
            left_position = hashtag_position - spring_count + 1 + i
            right_position = hashtag_position + 1 + i
            right_space_remaining = len(group) - right_position
            left_space_remaining = left_position
            if (left_position < 0) or (right_position > len(group)):
                # Deze verschuiving van de spring kan niet. De spring valt nu er buiten. Bijvoorbeeld ??#?? [4] helemaal links en richtse kan niet.Stop!
                continue
            elif left_space_needed > left_space_remaining or right_space_needed > right_space_remaining:
                #Nu is er niet genoeg ruimte voor de andere springs, dus dit kan ook niet. Stop!
                continue
            else:
                left_part = group[:(left_position)]
                right_part = group[(right_position):]
                new_scores.append(getNumPermutations(left_part, left_spring_counts))
                if len(right_spring_counts) == 0 and (right_part.find("#") == -1 ):
                    new_groups.append(right_part)
                    new_spring_counts.append([])
                if len(right_spring_counts) > 0:
                    new_groups.append(right_part)
                    new_spring_counts.append(right_spring_counts)
                
    return new_groups, new_scores, new_spring_counts

def solveGroupNoHastags(group, current_spring_counts, current_score, next_group_input_branches):
    print('solving group no hashtags', group)
    # getFeasibleSpring Groups returns an array of arrays of feasible spring counts and corresponding next_spring_counts
    # For instance [[1,1],[1]] and [[1],[1,1]] and [[], [1,1,1]] on loop 1
    feasible_spring_counts_list, next_spring_counts_list = getFeasibleSpringGroups(group, current_spring_counts)
    for feasible_spring_counts, next_spring_counts in zip(feasible_spring_counts_list, next_spring_counts_list):
        print('feasible', feasible_spring_counts, next_spring_counts)
        score = current_score * getNumPermutations(group, feasible_spring_counts)
        # Get the input for the next branch 
        if len(next_spring_counts) == 0:
            branch_scores.append(score)
        else:
            print("hi")
            next_group_input_branches.append([score, next_spring_counts])
            print(next_group_input_branches)
    return next_group_input_branches

total_scores = []
for line in data:
    row, spring_counts = line.split(" ")
    spring_counts = [int(i) for i in spring_counts.split(",")]
    groups = list(filter(None, row.split('.')))

    print("Groups", groups)
    # Input the score of this branch and the new set of spring counts format [[score, spring_counts]]
    # Dummy data in comments for this example "..???.??.? 1,1,1"
    group_input_branches = [[1, spring_counts]]
    branch_scores = []
    for group_idx, group in enumerate(groups):
        # Get the feasible spring counts for the current group and the corresponding next group spring counts
        next_group_input_branches = []
        for branch_data in group_input_branches:
            current_score = branch_data[0]             ## For this example in loop 1 value is 1                  
            current_spring_counts = branch_data[1]     ## For instance [1,1,1] in group 1 
            print(group)
            # If there is a hashtag in this group, solve the group and return next group input branches
            if group.find("#") > -1:
                solveGroupWithHashtags(group, current_spring_counts, current_score, next_group_input_branches)
            else:
                solveGroupNoHastags(group, current_spring_counts, current_score, next_group_input_branches)
            
        group_input_branches = next_group_input_branches
        # This will be [ [1,[1]],[3,[1,1]] ] for the first loop
        # On the second loop we will get [ [2,[]], [1,[1]], [6,[1]] ]
        # After the last branch we get [2, [], [1,[]], [6,[]] ]
        # Once all next_group_inputs are empty we stop
    # print(branch_scores)
    total_scores.append(sum(branch_scores))

print(total_scores)

answerA = sum(total_scores)
print("Answer A is", answerA)


a,b,c = replaceLeftHashtag("#", [1,1])
print(a,b,c)
# submit(answerA, part="a", day=day, year=year)

### Part B ###

# Write your code here
# answerB = 

# submit(answerB, part="b", day=day, year=year)


# Hoe werkt algoritme?
# Zoek meest linker hashtag---> '?#?#?#?#?#?#?#?
# 1,3,5,7,9,11,13
# Replace met 

# Hoe werkt algoritme?
# Zoek meest linker hashtag---> '?????#?????#?????'  # 2,2
# Replace hashtag voor elk getal in counts
# ???? ???#????? [0,2]
# ???  ????#????? [0,2]
# ???? ???#????? [2,0]    --> 3
# ???   ????#????? [2,0]  --> 1.   
# Bereken van linker deel de score

# Replace met linker ding.

