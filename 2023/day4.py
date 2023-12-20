from aocd import get_data, submit

year, day = 2023, 4

cards = get_data(year=year, day=day).splitlines()

# cards = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
# "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
# "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
# "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
# "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
# "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]

### Part A ###

totalPoints = 0
matching_number_count = []
for card in cards:
    winning_numbers, my_numbers = card.split("|")
    winning_numbers = [x for x in winning_numbers.split(":")[1].split(" ") if x]
    my_numbers = [x for x in my_numbers.split(" ") if x]

    winning_number_count = 0
    for number in winning_numbers:
        winning_number_count += my_numbers.count(number)
    
    matching_number_count.append(winning_number_count)
    
    if winning_number_count > 0:
        totalPoints += pow(2 , winning_number_count - 1)

answerA = totalPoints
# submit(answerA, part="a", day=day, year=year)

### Part B ###

print(matching_number_count)
# Check winning number counts on each card

card_instances = [ 1 for x in range(len(cards))]
for card_id, num_matches in enumerate(matching_number_count):
    for i in range(num_matches):
        card_instances[card_id + i + 1] += card_instances[card_id]


answerB = sum(card_instances)
submit(answerB, part="b", day=day, year=year)