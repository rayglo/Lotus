import logging

import Board
import ConstantsGame
from Player import Player
from Board import Board
from Card import Card
import UtilMethods as um
import numpy as np


class GameSimulation:

    def __init__(self, filename_logging: str):
        self.current_player = None
        self.board = Board()
        self.players = np.array([])
        self.lost = False
        logging.basicConfig(filename=filename_logging, filemode="w", level=logging.DEBUG,
                            format='[%(levelname)s][%(asctime)s]  %(message)s')
        logging.info("Game Simulation Starting")

    def add_player(self, name: str) -> bool:
        if self.contains_player(name):
            logging.info(f"System already contains player {name}")
            return False
        new_player = Player(name)
        self.players = np.append(self.players, [new_player])
        logging.info(f"Player {name} added")
        return True

    def contains_player(self, name: str):
        return np.array([x for x in self.players if x.name == name]).size == 1

    def draw_card(self, name: str, color: str, value: int, index: int = ConstantsGame.index_not_known):
        if not self.contains_player(name):
            logging.info(f"System does not contain player {name}")
            return
        if not um.value_allowed(value):
            logging.info(f"Value {value} not allowed")
            return
        if not um.color_allowed(color):
            logging.info(f"Color {color} not allowed")
            return
        if not um.index_allowed(index):
            logging.info(f"Index {index} not allowed")
            return

        player_obj = self.__get_player(name)
        player_obj.draw_card(Card(color, value), index)
        logging.info(f"Player {name} draws card ({color}, {value}) at index {index}")

    def __get_player(self, name: str) -> Player:
        if not self.contains_player(name):
            logging.info(f"System does not contain player {name}")
            return None
        return np.array([x for x in self.players if x.name == name])[0]

    def hint_player(self) -> bool:
        if self.board.blue_token <= 0:
            logging.info("You cannot remove any blue token")
            return False
        logging.info("An hint has been given, a blue token has been removed")
        self.board.remove_blue_token()
        return True

    def wrong_play(self):
        self.board.add_red_token()
        if self.board.red_token >= ConstantsGame.limit_red_token:
            logging.info("Max number of red tokens reached. Lost condition")
            self.lost = True
        else:
            logging.info("Number of red tokens increased")

    def play_card(self, name: str, color: str, value: int):
        if not self.contains_player(name):
            logging.info(f"System does not contain player {name}")
            return
        if not um.value_allowed(value):
            logging.info(f"Value {value} not allowed")
            return
        if not um.color_allowed(color):
            logging.info(f"Color {color} not allowed")
            return
        if not self.__get_player(name).has_card(Card(color, value)):
            logging.info(f"Player {name} has not the card ({color}, {value})")
            return

        self.board.add_firework(Card(color, value))
        logging.info(f"Firework ({color}, {value}) added to the board")

    def calculate_score(self):
        return self.board.score

    def reset(self):
        self.board.reset()
        for i in self.players:
            i.reset()
        logging.info(f"Resetting board and players")

    def set_current_player(self, current_player: str) -> bool:
        player_obj = self.__get_player(current_player)
        if player_obj is None:
            logging.info(f"Player {current_player} not found")
            return False
        logging.info(f"Current player is {player_obj.name}")
        self.current_player = player_obj
        return True

    def discard_card(self, name: str, index: int):
        if not self.contains_player(name):
            logging.info(f"System does not contain player {name}")
            return False
        if not um.index_allowed(index):
            logging.info(f"Index {index} not allowed")
            return False

        player_obj = self.__get_player(name)
        card_obj = player_obj.get_card_by_index(index)
        self.board.add_to_discard_pile(card_obj)
        self.board.add_blue_token()
        player_obj.discard_card(index)
