# Main game entry point
import sys
sys.path.append('src')
from game.engine import Game

if __name__ == '__main__':
    game = Game()
    game.run()
