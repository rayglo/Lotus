import numpy as np

from Card import Card

colors = ['white', 'blue', 'yellow', 'green', 'red']
values = [1, 2, 3, 4, 5]

cards_per_hand = 5
starting_blue_token = 8
limit_red_token = 3

# Standard deck that has 3 of 1, 1 of max and 2 of each other value
standard_deck = np.array([Card(x, y)
                          for x in colors
                          for y in values
                          for k in range(1 if y == max(values) else (3 if y == 1 else 2))])
