# main.py

from game_logic import Game
from gui import GameGUI

def main():
    game = Game()
    gui = GameGUI(game)
    gui.start()

if __name__ == "__main__":
    main()
