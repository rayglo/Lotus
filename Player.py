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

    def draw_card(self, card: Card, index: int = ConstantsGame.index_not_known) -> bool:
        if index == ConstantsGame.index_not_known:
            for i in range(ConstantsGame.cards_per_hand):
                if self.hand[i] is None:
                    self.hand[i] = card
                    return True
            return False
        if self.hand[index] is not None:
            return False
        self.hand[index] = card
        return True

    def has_card(self, card: Card) -> bool:
        return np.array([x for x in self.hand if x == card]).size > 0

    def reset(self):
        self.hand = np.array([None for x in range(ConstantsGame.cards_per_hand)])

    def discard_card(self, index: int) -> bool:
        if not um.index_allowed(index):
            return False
        self.hand = np.delete(self.hand, index)
        self.hand = np.append(self.hand, None)
        return True

    def get_card_by_index(self, index: int):
        if not um.index_allowed(index):
            return None
        return self.hand[index]
