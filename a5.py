# Assignment 5

#
# Full Name:Hiroshi Wong, Kanamu Kobayashi
#  SFU ID #:301625447
# SFU Email:hew5@sfu.ca
#

import random
from multiprocessing.managers import Value

#===========#

dice_face = {
    1: [" ----- ",
        "|     |",
        "|  ●  |",
        "|     |",
        " ----- "],
    2: [" ----- ",
        "| ●   |",
        "|     |",
        "|   ● |",
        " ----- "],
    3: [" ----- ",
        "| ●   |",
        "|  ●  |",
        "|   ● |",
        " ----- "],
    4: [" ----- ",
        "| ● ● |",
        "|     |",
        "| ● ● |",
        " ----- "],
    5: [" ----- ",
        "| ● ● |",
        "|  ●  |",
        "| ● ● |",
        " ----- "],
    6: [" ----- ",
        "| ● ● |",
        "| ● ● |",
        "| ● ● |",
        " ----- "]
}

points = {1: 100, 2: 2, 3: 3, 4: 4, 5: 5, 6: 60}
special_scores = {
    (4, 5, 6): 1000,
    (6, 6, 6): 900,
    (5, 5, 5): 800,
    (4, 4, 4): 700,
    (3, 3, 3): 600,
    (2, 2, 2): 500,
    (1, 1, 1): 400,
    (1, 2, 3): 300
}

scores = {"user":0, "bot1":0, "bot2":0, "bot3":0}
risk = {"user": 0, "bot1": 0, "bot2": 0, "bot3": 0}

# player stats to be remembered over entire game
players = {
    "user": {
        "name": "kana",
        "score": 0,
        "num_chip": 0
    },
    "bot1": {
        "name": "bot1",
        "score": 0,
        "num_chip": 0
    },
    "bot2": {
        "name": "bot2",
        "score": 0,
        "num_chip": 0
    },
    "bot3": {
        "name": "bot3",
        "score": 0,
        "num_chip": 0
    }
}

def random_turn_order():
    # this gives you all the keys in the dict BUT NOT THE VALUES
    temp_player_list = list(players.keys())
    
    # shuffle order of player list
    random.shuffle(temp_player_list)
    return temp_player_list 


def roll_dice(user):
    scores[user] = 0
    risk[user] = 0

    rolls = [random.randint(1, 6) for j in range(3)]

    for row in range(5):
        print("  ".join(dice_face[i][row] for i in rolls))

    sorted_rolls = tuple(sorted(rolls))
    if sorted_rolls in special_scores:
        scores[user] += special_scores[sorted_rolls]

        if sorted_rolls == (4, 5, 6):
            print("PoCo!")
            risk[user] += 4
        elif sorted_rolls == (1, 2, 3):
            print("LoCo!")
            risk[user] += 2
        else:
            print("Three-of-a-kind!")
            risk[user] += 3

    else:
        scores[user] += sum(points[die] for die in rolls)
        risk[user] += 1

    print(f'Rolled {rolls}')
    print(f'Total Points for {user}: {scores[user]}')#temporary, setting up winning and losing
#===========#
rolls_left = 0

def three_tries(tries, user):
    rolls_remaining = tries
    while rolls_remaining > 0:
        roll_dice(user)
        rolls_remaining -= 1

        if rolls_remaining == 0:
            print(f"State automatically saved after {tries - rolls_remaining} attempts")
            # use rolls_remaining instead of rolls_left
            # rolls_left = tries - rolls_remaining
            break

        print(f'attempts left: {rolls_remaining}')
        if user == name: # if user is human player
            retry = input('Would you like to try again?: (Yes/No)').strip().lower()

            if retry == "yes":
                print("Re-rolling...")

            elif retry == "no":
                print(f"State automatically saved after {tries - rolls_remaining} attempts")
                print("Ending Turn")
                
                # rolls_left = tries - rolls_remaining
                break

            else:
                print("Invalid input. Please type 'yes' or 'no'.")
        else: 
            if (scores[user]) >= 100:
                print(f"State automatically saved after {tries - rolls_remaining} attempts")
                print("Ending Turn")
                # rolls_left = tries - rolls_remaining
                break
            else:
                print("Re-rolling...")

    return tries - rolls_remaining
#===========#

def ai_turn(tries, bot_name):
    print(f"\n{bot_name}'s turn begins!")
    three_tries(tries, bot_name)
    


#===========#

ran_player1 = {1:"Ajani", 2:"Bruvac", 3:"Christ", 4:"Dean", 5:"Elspeth", 6:"Frank", 7:"Gisa", 8:"Herman", 9:"Isaac"}
ran_player2 = {1:"Jace", 2:"Karn", 3:"Lindy", 4:"Minsc", 5:"Nissa", 6:"Oscar", 7:"Peter", 8:"Queen", 9:"Rachel"}
ran_player3 = {1:"Sorin", 2:"Thalia", 3:"Urza", 4:"Virgil", 5:"Walter", 6:"Xavier", 7:"Yarok", 8:"Zuko"}

player = {0:"user", 1:"player1", 2:"player2", 3:"player3"}

# unused function, renamed to init_players
def init_players():
    players["bot1"]["name"] = random.choice(list(ran_player1.values()))
    players["bot2"]["name"] = random.choice(list(ran_player2.values()))
    players["bot3"]["name"] = random.choice(list(ran_player3.values()))

    # player[1] = random.choice(list(ran_player1.values()))
    # player[2] = random.choice(list(ran_player2.values()))
    # player[3] = random.choice(list(ran_player3.values()))
    # scores[1] = player[1]
    # scores[2] = player[2]
    # scores[3] = player[3]

#===========#
# function to be used in the game function

def report(rounds):
    round_text = (f"Round {rounds}")
    border_len = len(round_text) + 4

    print("+" + "-" * (border_len - 2) + "+")
    print(f'| {round_text} |')
    print("+" + "-" * (border_len - 2) + "+")

    print(f"""
    {player[0]}: {tokens["user"]}
    {player[1]}: {tokens["bot1"]}
    {player[2]}: {tokens["bot2"]}
    {player[3]}: {tokens["bot3"]}
    """)

#===========#

def winner(): #this needs more work
    #make an if function stating that any scores greater than the minimum score will be a winner making 3 winners
    
    # scores = {"user":100, "bot1":2000, "bot2":30000, "bot3":-5}
    min_user = ''
    min_score = 99999
    for k, v in scores.items():
        if v < min_score:
            min_score = v
            min_user = k
    print(f'min_user is {min_user} with score of {min_score}') #this will print out the lowest score player and its score
    
    
    # winner = max(scores)
    
    # print(f'the winner of this round is {winner}, and the loser of this round is {loser}')
    # print(f'Changing scores...')


#===========#

tokens = {"user":0, "bot1":0, "bot2":0, "bot3":0} #this might need to be changed to number of chips

def chips():
    while True:
        try:
            chip_num = int(input("How many chips would you like to start? The default amount is 10"))
            #b/c we cannot play if the num of chips is 0 i added a feature to not let that happen -K
            if (chip_num <= 0):
                chip_num = 10
                print(f"Sorry, because the number of chips selected was zero the number of chips will be {chip_num}.")
            break
        except ValueError:
            print(f'Please give a non-decimal number')
    #this assigns the number of chips to each player
    for player in players.keys():
        players[player]["num_chip"] = chip_num

    # tokens["user"] = chip_num
    # tokens["bot1"] = chip_num
    # tokens["bot2"] = chip_num
    # tokens["bot3"] = chip_num

#===========#

def rules():
    rule = input('Would you like to read the rules?: (Yes/No)').strip().lower()

    if rule == "yes":
        print("""
        PoCoLoCo! is a dice-rolling game played with chips. 
        Players take turns repeatedly rolling three dice, 
        and the first player to lose all their chips is the 
        winner. PocoLoco is played in rounds. 
        
        In each round, players take turns rolling three dice 
        and try to get the highest score possible. The order 
        of which player goes first, second, third and fourth
        are randomized.
        
        The first player has up to three chances to roll the 
        score they want, however, you can choose to stop early,
        and the next players can only roll as many times as 
        previous player or less. 
        
        The scores of the dice are as follows:
        1 = 100 points
        2 = 2 points
        3 = 3 points
        4 = 4 points
        5 = 5 points
        6 = 60 points
        
        There is also special scores that are above normal scores.
        These scores, which rank from highest to lowest, are as
        follows: 
        1st: PoCo! (4, 5, 6)
        2nd: (6, 6, 6)
        3rd: (5, 5, 5)
        4th: (4, 4, 4)
        5th: (3, 3, 3)
        6th: (2, 2, 2)
        7th: (1, 1, 1)
        8th: LoCo! (1, 2, 3)
        
        In the case of a tie, a tiebreaker will occur, in which a
        game of rock-paper-scissors will be played, where the winner 
        of that game will win the round.
        
        The loser of the round will receive chips equal to the scores
        as follows:
        PoCo!: 4 chips
        3-of-a-kind: 3 chips
        LoCo!: 2 chips
        Normal Score: 1 chip
        
        Rounds will continue until a player has no chips left, in which
        the game will end and that player will win.
        """)

    elif rule == "no":
        print(f"Understood!")

    else:
        print("Invalid input. Please type 'yes' or 'no'.")
        rules()

#===========#

def tiebreaker():
    while True:
        user_action = input("Enter a choice (rock, paper, scissors): ")
        possible_actions = ["rock", "paper", "scissors"]
        computer_action = random.choice(possible_actions)
        print(f"\nYou chose {user_action}, computer chose {computer_action}.\n")

        if user_action == computer_action:
            print(f"Both players selected {user_action}. It's a tie!")
        elif user_action == "rock":
            if computer_action == "scissors":
                print("Rock smashes scissors! You win!")
                break
            else:
                print("Paper covers rock! You lose.")
                break

        elif user_action == "paper":
            if computer_action == "rock":
                print("Paper covers rock! You win!")
                break
            else:
                print("Scissors cuts paper! You lose.")
                break

        elif user_action == "scissors":
            if computer_action == "paper":
                print("Scissors cuts paper! You win!")
                break
            else:
                print("Rock smashes scissors! You lose.")
                break

#===========#

name = input("What is your name?: ")
player[0] = name
print(f'Hello {name}, Let\'s play a game!')
print(f'Hello! and welcome to...')
print("""
+------------+
| PoCo LoCo! |
+------------+
""")
print(f'Our players are...')
init_players()
print(f'{player[1]}, {player[2]}, {player[3]}, and {name}!')
print(f'Let\'s start the game!')
rules()
chips()
roundnum = 0
user = player[0]
bot1 = player[1]
bot2 = player[2]
bot3 = player[3]
while True:
    if tokens != 0:
        # round start
        roundnum += 1
        round_turn_order = random_turn_order() # returns randomized list of our players
        # eg. ["bot2", "bot1", "user", "bot3"]
        report(roundnum)

        # loop through each user from round_turn_order
        player_tries = 3
        for p in round_turn_order:
            print(f'It is {players[p]["name"]}\'s turn')
            tries_used = three_tries(player_tries, p)
            player_tries = tries_used
        winner()
            
        # print(f'It is {player[1]}\'s turn')
        # three_tries(rolls_left, 1)
        # print(f'It is {player[2]}\'s turn')
        # three_tries(rolls_left, 2)
        # print(f'It is {player[3]}\'s turn')
        # three_tries(rolls_left, 3)

#===========#
