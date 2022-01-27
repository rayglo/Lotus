import numpy as np
import Card
import ConstantsGame
import UtilMethods as um


class Player:

    def __init__(self, name: str):
        self.name = name
        self.hand = np.array([None for x in range(ConstantsGame.cards_per_hand)])

    def __str__(self):
        return f"Player - {self.name}"

    def print_hand(self):
        print(f"{self.name}'s hand:")
        for i in range(self.hand.size):
            print(f"\t{self.hand[i]} - index: {i}")

    def draw_card(self, card: Card, index: int) -> bool:
        if self.hand[index] is not None:
            return False
        self.hand[index] = card
        return True

    def has_card(self, card: Card) -> bool:
        return np.array([x for x in self.hand if x == card]).size > 0
