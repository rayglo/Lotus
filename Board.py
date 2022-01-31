from typing import List

import ConstantsGame
from Card import Card
import numpy as np


class Board:

    def __init__(self):
        self.fireworks = np.array([{'color': i, 'value': 0} for i in ConstantsGame.colors])
        self.deck = np.copy(ConstantsGame.standard_deck)
        self.deck_count = len(self.deck)
        self.discard_pile = np.array([])
        self.blue_token = ConstantsGame.starting_blue_token
        self.red_token = 0
        self.score = 0

    def __str__(self):
        str_board = " Board\n\tfireworks:"
        for i in self.fireworks:
            str_board += f"\n\t\t{i['color']} - {i['value']}"
        str_board += f"\n\tblue tokens = {self.blue_token}"
        str_board += f"\n\tred tokens = {self.red_token}"
        str_board += f"\n\tcards in deck = {self.deck_count}"
        str_board += f"\n\tcards in discard pile = {len(self.discard_pile)}"

        return str_board

    def remove_blue_token(self):
        self.blue_token -= 1

    def add_blue_token(self):
        self.blue_token += 1

    def add_red_token(self):
        self.red_token += 1

    def add_firework(self, card: Card):
        index = 0
        for i in range(self.fireworks.size):
            if self.fireworks[i]['color'] == card.color:
                index = i
                break

        if card.value == self.fireworks[index]['value'] + 1 and card.value < max(ConstantsGame.values):
            self.fireworks[index]['value'] += 1
            self.score += 1
            print(f"Firework {card.value} added to {card.color}")
            return True
        print(f"Cannot add firework {card.value} to {card.color}")

    def reset(self):
        self.fireworks = np.array([{'color': i, 'value': 0} for i in ConstantsGame.colors])
        self.deck = np.copy(ConstantsGame.standard_deck)
        self.deck_count = len(self.deck)
        self.discard_pile = np.array([])
        self.blue_token = ConstantsGame.starting_blue_token
        self.red_token = 0
        self.score = 0

    def add_to_discard_pile(self, card: Card):
        self.discard_pile = np.insert(self.discard_pile, 0, [card], axis=0)
