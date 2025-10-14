"""
I Am The Fool - Auto-Runner Platformer
Entry point for the game
"""

import sys
sys.path.append('src')
from src.game import Game

if __name__ == '__main__':
    game = Game()
    game.run()
