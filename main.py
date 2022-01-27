from GameSimulation import GameSimulation
from Card import Card

gs = GameSimulation()
gs.add_player("marco")
gs.draw_card("marco", "yellow", 1, 0)
gs.draw_card("marco", "red", 1, 1)
gs.draw_card("marco", "blue", 1, 2)
gs.draw_card("marco", "yellow", 1, 3)
gs.draw_card("marco", "yellow", 1, 4)
print(gs.calculate_points())
print(gs.board)
gs.play_card("marco", "yellow", 1)
gs.play_card("marco", "red", 1)
gs.play_card("marco", "yellow", 1)
gs.play_card("marco", "white", 1)
print(gs.board)
print(gs.calculate_points())
