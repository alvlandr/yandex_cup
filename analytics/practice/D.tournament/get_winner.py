import math
from collections import Counter


pairs = []
num_pairs = int(input())
for i in range(num_pairs):
    pairs.append(input().split(' '))

max_games = int(math.log2(num_pairs + 1))
participants_num = num_pairs + 1
flatten_players = [i for p in pairs for i in p]

counter = Counter(flatten_players)
games_counter = Counter([i for i in counter.values()])
games_counter[max_games] -= 1
is_possible = True

for pair in pairs:
    gamer_1, gamer_2 = pair
    game_round = min(counter[gamer_1], counter[gamer_2])
    if game_round > max_games:
        is_possible = False
        print('NO SOLUTION')
        break

for r in range(1, max_games+1):
    game_num_cond = games_counter[r] == 2 ** (max_games - r)
    round_players = {i for i in counter if counter[i] >= r}
    num_round_players = len(round_players)
    player_num_cond = num_round_players == (participants_num // r)
    if player_num_cond and game_num_cond:
        continue
    else:
        print('NO SOLUTION')
        is_possible = False
        break

while is_possible:
    if len(counter.keys()) != participants_num:
        print('NO SOLUTION')
        is_possible = False
        break

    for pair in pairs:
        if (counter[pair[0]] == counter[pair[1]]) and (counter[pair[0]] < max_games):
            print('NO SOLUTION')
            is_possible = False
            break
        continue

    print(' '.join(list(round_players)))
