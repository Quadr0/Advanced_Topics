from random import randint
num_players = 500
num_round_round = 5
dice_rolls = {1:-1, 2:-1, 3:0, 4:0, 5:1, 6:1}

def play_turn(p1, p2, round_players):
    m1 = dice_rolls[randint(1, 6)]
    m2 = dice_rolls[randint(1, 6)]

    if p1 + m1 > round_players:
        p1 = 1

    elif p1 + m1 < 1:
        p1 = round_players

    else:
        p1 += m1

    if p2 + m2 > round_players:
        p2 = 1

    elif p2 + m2 < 1:
        p2 = round_players

    else:
        p2 += m2

    return (p1, p2)

def play_round(round_players):
    turns = 0
    p1 = randint(1, round_players)
    p2 = randint(1, round_players)

    while p1 != p2:
        p1, p2 = play_turn(p1, p2, round_players)
        turns += 1

    return turns


def main():
    total_pot = 0
    for _ in range(num_round_round):
        pot = 0
        round_players = num_players
        while round_players > 1:
            turn_pot = play_round(round_players) ** 2
            pot += turn_pot
            round_players -= 1

        total_pot += pot
        print(pot)
    
    print(total_pot/num_round_round)


main()
