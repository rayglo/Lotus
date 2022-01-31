import numpy as np

from Card import Card

debug = True

colors = ['white', 'blue', 'yellow', 'green', 'red']
values = [1, 2, 3, 4, 5]
replicas = [3, 2, 2, 2, 1]

cards_per_hand = 5
index_not_known = -527  # Used when an index is not known
starting_blue_token = 8
limit_red_token = 3

# Standard deck that has 3 of 1, 1 of max and 2 of each other value
standard_deck = np.array([Card(x, y)
                          for x in colors
                          for y in values
                          for k in range(replicas[y - 1])])
