from aocd import get_data, submit

year, day = 2023, 7

data = get_data(year=year, day=day).splitlines()
# data = data[0:200]
# data = [
# "32T3K 765",
# "T55J5 684",
# "KK677 28",
# "KTJJT 220",
# "QQQJA 483",
# ]

# Strengths from weak to strong
# card_values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A" ]
card_values = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A" ]

###### Part A ###### 

def getHighestCard(cards):
    highest_card_value = 0
    for idx, card_value in enumerate(card_values):
        if card_value in cards:
            highest_card_value = idx
    
    return highest_card_value

def getEqualCardValues(cards_dict):
    cardValues = []
    for card_name in cards_dict:
        cardValues.append(getHighestCard(card_name))
    cardValues = sorted(cardValues, reverse=True)
    cardSum = 0
    for idx, cardValue in enumerate(cardValues):
        cardSum += cardValue / (pow(100,idx))
    return cardSum

def getHandStrengthIfEqual(hand):
    value = ""
    for card in hand:
        value += str(11 + card_values.index(card))
    return int(value) / 10000000000



def getHandStrength(hand):
    counts = {i: hand.count(i) for i in set(hand)}
    max_count_card = max(counts, key=counts.get)
    max_count_value = counts[max_count_card]
    unique_cards = len(counts)
    hand_type = ""
    if unique_cards == 1:
        hand_type="Five"
        #If five of a kind value is 10,000,000 + highest card value 
        # hand_strength = 10000000 + getHighestCard(hand)
        hand_strength = 7 + getHandStrengthIfEqual(hand)

    elif unique_cards == 2:
        #Four of a kind or full house
        if max_count_value == 4:
            hand_type="Four"
            # If four of a kind value is 1,000,000 + highest card value + lowest card value / 10
            # hand_strength = 1000000 + getHighestCard(max_count_card)
            hand_strength = 6 + getHandStrengthIfEqual(hand)
            # del counts[max_count_card]
            # hand_strength += getEqualCardValues(counts) / 100
        else:
            hand_type="Full"
            # If full house value is 100,000 + highest card value + lowest card value / 10
            # hand_strength = 100000 + getHighestCard(max_count_card)
            hand_strength = 5 + getHandStrengthIfEqual(hand)
            # del counts[max_count_card]
            # hand_strength += getEqualCardValues(counts) / 100
    
    elif unique_cards == 3:
        #three of a kind or two pair 
        if max_count_value == 3:
            hand_type="Three"
            # If three of a kind, value is 10,000 + highest card value + middle card value /10+ lowest card value /100
            # hand_strength = 10000 + getHighestCard(max_count_card)
            hand_strength = 4 + getHandStrengthIfEqual(hand)
            # del counts[max_count_card]
            # hand_strength += getEqualCardValues(counts) / 100
            # Find max value and add to hand strength
        else:
            # If two pair, value is 1,000 + highest card value + second pair value / 10 + lowest card value /100
            # hand_strength = 1000
            hand_type="Two"
            hand_strength = 3 + getHandStrengthIfEqual(hand)
            # for count in counts:
            #     if counts[count] == 1:
            #         hand_strength += getHighestCard(count)/(100*100)
            #         delete_count = count
            # del counts[delete_count]
            # hand_strength += getEqualCardValues(counts)
   
    elif unique_cards == 4:
        hand_type="Pair"
        # If one pair, value is 100 + highest card value + second highest card value / 10 + third / 100 + fourth /1000
        hand_strength = 2 + getHandStrengthIfEqual(hand)
        # hand_strength = 100 + getHighestCard(max_count_card)
        # del counts[max_count_card]
        # hand_strength += getEqualCardValues(counts) /100

    elif unique_cards == 5:
        hand_type="One"
        # If high card, value is highest card value + second card value / 10 + third / 100 etc...
        hand_strength = 1 + getHandStrengthIfEqual(hand)
        # hand_strength = getEqualCardValues(hand)
    return hand_strength, hand_type

hand_strenghts = []
bids = []
hands = []
hand_types = []
for line in data:
    hand, bid = line.split(" ")
    hands.append(hand)
    bids.append(int(bid))
    hand_strength, hand_type = getHandStrength(hand)
    hand_strenghts.append(hand_strength)
    hand_types.append(hand_type)

# for hand_strength in hand_strenghts:
    
sorted_bids = [x for (y,x)in sorted(zip(hand_strenghts,bids))]
sorted_hand_strengths = [y for (y,x)in sorted(zip(hand_strenghts,bids))]
sorted_hands = [x for (y,x)in sorted(zip(hand_strenghts,hands))]
sorted_hand_types = [x for (y,x)in sorted(zip(hand_strenghts,hand_types))]

total_winnings = 0
for idx, (hand_strength, bid) in enumerate(zip(sorted_hand_strengths, sorted_bids)):
    # print(hand_strength, bid, idx + 1)
    total_winnings += (idx + 1) * bid

answerA = total_winnings
# submit(answerA, part="a", day=day, year=year)



### Part B ###

def checkIfJoker(card_dict):
    jokerCheck = False
    for card in card_dict:
        if card == "J":
            jokerCheck = True
    
    return jokerCheck

def getHandStrengthPartB(hand):
    counts = {i: hand.count(i) for i in set(hand)}
    max_count_card = max(counts, key=counts.get)
    max_count_value = counts[max_count_card]
    unique_cards = len(counts)
    hand_type = ""
    if unique_cards == 1:
        hand_type="Five"
        #If five of a kind value is 10,000,000 + highest card value 
        # hand_strength = 10000000 + getHighestCard(hand)
        hand_strength = 7 + getHandStrengthIfEqual(hand)

    elif unique_cards == 2:
        #Four of a kind or full house
        if max_count_value == 4:
            hand_type="Four"
            if checkIfJoker(counts):
                # Als er een J is five of a kind anders 4
                hand_strength = 7 + getHandStrengthIfEqual(hand)
            else:
                hand_strength = 6 + getHandStrengthIfEqual(hand)
        else:
            hand_type="Full"
            if checkIfJoker(counts):
                # Bij full house als er een J is dan Five of a kind anders full house
                hand_strength = 7 + getHandStrengthIfEqual(hand)
            else:
                hand_strength = 5 + getHandStrengthIfEqual(hand)           
   
    elif unique_cards == 3:
        #three of a kind or two pair 
        if max_count_value == 3:
            hand_type="Three"
            # Three of a kind, als er een J is 4 of a kind. Anders 3    
            if checkIfJoker(counts):
                hand_strength = 6 + getHandStrengthIfEqual(hand)
            else:
                hand_strength = 4 + getHandStrengthIfEqual(hand)    

        else:
            # Two pair. Als geen J dan two pair.  Als een van de 2 waarden Js heeft dan 4 of a kind, anders full house
            hand_type="Two"
            if checkIfJoker(counts):
                if counts['J'] == 2:
                    hand_strength = 6 + getHandStrengthIfEqual(hand)
                else:
                    hand_strength = 5 + getHandStrengthIfEqual(hand)
            else:
                hand_strength = 3 + getHandStrengthIfEqual(hand)
       
   
    elif unique_cards == 4:
        hand_type="Pair"
        # Als er een J is dan 3 of a kind, anders pair
        if checkIfJoker(counts):
            hand_strength = 4 + getHandStrengthIfEqual(hand)
        else: 
            hand_strength = 2 + getHandStrengthIfEqual(hand)

    elif unique_cards == 5:
        hand_type="One"
        # Als er een J is dan pair, anders 1 of a kind
        if checkIfJoker(counts):
            hand_strength = 2 + getHandStrengthIfEqual(hand)    
        else:
            hand_strength = 1 + getHandStrengthIfEqual(hand)

    return hand_strength, hand_type


hand_strenghts = []
bids = []
hands = []
hand_types = []
for line in data:
    hand, bid = line.split(" ")
    hands.append(hand)
    bids.append(int(bid))
    hand_strength, hand_type = getHandStrengthPartB(hand)
    hand_strenghts.append(hand_strength)
    hand_types.append(hand_type)

# for hand_strength in hand_strenghts:
    
sorted_bids = [x for (y,x)in sorted(zip(hand_strenghts,bids))]
sorted_hand_strengths = [y for (y,x)in sorted(zip(hand_strenghts,bids))]
sorted_hands = [x for (y,x)in sorted(zip(hand_strenghts,hands))]
sorted_hand_types = [x for (y,x)in sorted(zip(hand_strenghts,hand_types))]

total_winnings = 0
for idx, (hand_strength, bid) in enumerate(zip(sorted_hand_strengths, sorted_bids)):
    # print(hand_strength, bid, idx + 1)
    total_winnings += (idx + 1) * bid

answerB = total_winnings
print(answerB)
submit(answerB, part="b", day=day, year=year)