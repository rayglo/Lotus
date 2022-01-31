import ConstantsGame
from GameSimulation import GameSimulation


class LotusEngine:

    def __init__(self, owner: str = None):
        if owner is None:
            self.game_simulation = GameSimulation()
        else:
            self.game_simulation = GameSimulation(f"GS_logging_{owner}.log")
            self.game_simulation.add_player(owner)
        self.owner = owner

    def add_player(self, name: str) -> bool:
        if self.game_simulation.add_player(name):
            print(f"player {name} registered in lotus engine")
            return True
        else:
            print(f"player {name} is already present in lotus engine")

    def set_current_player(self, current_player: str) -> bool:
        return self.game_simulation.set_current_player(current_player)

    def draw_card(self, name: str, color: str, value: int, index: int = ConstantsGame.index_not_known) -> bool:
        return self.game_simulation.draw_card(name, color, value, index)

    def discard_card(self, name: str, index: int):
        return self.game_simulation.discard_card(name, index)
