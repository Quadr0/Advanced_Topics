from random import randint
import numpy as np

num_players = 100
dice_movement = {1:-1, 2:0, 3:0, 4:0, 5:0, 6:1}

def play_one_round(players):
    die1, die2 = roll_dice(2)
    p1,p2 = np.where(np.array(players) == 1)[0]

    players[p1] -= 1
    players[(p1+dice_movement[die1])%num_players] += 1

    players[p2] -= 1
    players[(p2+dice_movement[die2])%num_players] += 1

def play_one_game():
    count = 0
    players = [0]*num_players
    players[0] = 1
    players[num_players//2] = 1
    while 2 not in players:
        play_one_round(players)
        count += 1
    return count

def roll_dice(n):
    return (randint(1,6) for _ in range(n))

def main():
    rounds_count = []
    for _ in range(1):
        num_rounds = play_one_game()
        rounds_count.append(num_rounds)
    print(int(np.mean(rounds_count)))

main()
