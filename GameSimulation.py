import Board
import ConstantsGame
from Player import Player
from Board import Board
from Card import Card
import UtilMethods as um
import numpy as np


class GameSimulation:

    def __init__(self):
        self.board = Board()
        self.players = np.array([])
        self.lost = False

    def add_player(self, name: str):
        if self.contains_player(name):
            print(f"System already contains player {name}")
            return
        new_player = Player(name)
        self.players = np.append(self.players, [new_player])
        print(f"Player {name} added to GameSimulation")

    def contains_player(self, name: str):
        return np.array([x for x in self.players if x.name == name]).size == 1

    def draw_card(self, name: str, color: str, value: int, index: int):
        if not self.contains_player(name):
            print(f"System does not contain player {name}")
            return
        if not um.value_allowed(value):
            print(f"Value {value} not allowed")
            return
        if not um.color_allowed(color):
            print(f"Color {color} not allowed")
            return
        if not um.index_allowed(index):
            print(f"Index {index} not allowed")
            return

        player_obj = self.get_player(name)
        player_obj.draw_card(Card(color, value), index)

    def get_player(self, name: str) -> Player:
        if not self.contains_player(name):
            print(f"System does not contain player {name}")
            return None
        return np.array([x for x in self.players if x.name == name])[0]

    def hint_player(self) -> bool:
        if self.board.blue_token <= 0:
            print("You cannot remove any blue token")
            return False
        self.board.remove_blue_token()
        return True

    def wrong_play(self):
        self.board.add_red_token()
        if self.board.red_token >= ConstantsGame.limit_red_token:
            print("Gods are very angry! You've lost!")
            self.lost = True
        else:
            print("Bad move! Gods are angry!")

    def play_card(self, name: str, color: str, value: int):
        if not self.contains_player(name):
            print(f"System does not contain player {name}")
            return
        if not um.value_allowed(value):
            print(f"Value {value} not allowed")
            return
        if not um.color_allowed(color):
            print(f"Color {color} not allowed")
            return
        if not self.get_player(name).has_card(Card(color, value)):
            print(f"Player has not the requested card")

        self.board.add_firework(Card(color, value))

    def calculate_points(self):
        return self.board.calculate_points()
