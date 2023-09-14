from game import Game

game = Game()
print(game)

valid_moves = game.get_valid_actions()

for action in valid_moves:
    print(action)
