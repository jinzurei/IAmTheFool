import sys
sys.path.append('src')
from src.game import Game

if __name__ == '__main__':
    game = Game()
    game.run()