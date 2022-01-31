import ConstantsGame
from GameSimulation import GameSimulation
from swiplserver import PrologMQI, PrologThread
import os.path


class LotusEngine:

    def __init__(self, owner: str = None):
        if owner is None:
            self.game_simulation = GameSimulation()
        else:
            self.game_simulation = GameSimulation(f"GS_logging_{owner}.log")
            self.game_simulation.add_player(owner)
        self.owner = owner
        if not os.path.isfile("knowledge_base_core.txt"):
            print("knowledge_base_core.txt not present")
        self.prolog = PrologMQI()
        self.prolog.start()
        '''
        with self.prolog.create_thread() as prolog_thread, open("knowledge_base_core.txt", "r") as kb:
            for line in kb:
                if not line:
                    continue
                print(line)
                prolog_thread.query(line)
       '''

    def add_player(self, name: str) -> bool:
        if self.game_simulation.add_player(name):
            with self.prolog.create_thread() as prolog_thread:
                prolog_thread.query(f"assert(player({name})).")
            print(f"player {name.lower()} registered in lotus engine")
            return True
        else:
            print(f"player {name.lower()} is already present in lotus engine")

    def set_current_player(self, current_player: str) -> bool:
        return self.game_simulation.set_current_player(current_player)

    def draw_card(self, name: str, color: str, value: int, index: int = ConstantsGame.index_not_known) -> bool:
        return self.game_simulation.draw_card(name, color, value, index)

    def discard_card(self, name: str, index: int):
        return self.game_simulation.discard_card(name, index)

    def query(self, query: str):
        with self.prolog.create_thread() as prolog_thread:
            result = prolog_thread.query(query)

        return result
