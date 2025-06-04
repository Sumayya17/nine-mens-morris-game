# game_logic.py

from utils import check_mill

class Game:
    def __init__(self):
        self.board = [' '] * 24
        self.current_player = 'W'
        self.white_pieces_in_hand = 9
        self.black_pieces_in_hand = 9
        self.white_pieces_on_board = 0
        self.black_pieces_on_board = 0
        self.winner = None

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'B' if self.current_player == 'W' else 'W'

    def place_piece(self, position):
        """Place a piece on the board during phase 1."""
        if self.board[position] != ' ':
            return False, "Position already occupied."

        # Check if the player has pieces left to place
        if self.current_player == 'W' and self.white_pieces_in_hand <= 0:
            return False, "No pieces left to place."
        if self.current_player == 'B' and self.black_pieces_in_hand <= 0:
            return False, "No pieces left to place."

        self.board[position] = self.current_player
        if self.current_player == 'W':
            self.white_pieces_in_hand -= 1
            self.white_pieces_on_board += 1
        else:
            self.black_pieces_in_hand -= 1
            self.black_pieces_on_board += 1

        formed_mill = check_mill(self.board, position)
        if formed_mill:
            return True, "Mill formed. Remove an opponent's piece."
        else:
            self.switch_player()
            self.check_win_condition()
            return True, "Piece placed."

    def remove_piece(self, position):
        """Remove an opponent's piece when a mill is formed."""
        opponent = 'B' if self.current_player == 'W' else 'W'
        if self.board[position] != opponent:
            return False, "You can only remove an opponent's piece."
        self.board[position] = ' '
        if opponent == 'W':
            self.white_pieces_on_board -= 1
        else:
            self.black_pieces_on_board -= 1
        self.switch_player()
        self.check_win_condition()
        return True, "Piece removed."

    def check_win_condition(self):
        """Check if a player has won the game."""
        if self.black_pieces_on_board < 3 and self.black_pieces_in_hand == 0:
            self.winner = 'W'
        elif self.white_pieces_on_board < 3 and self.white_pieces_in_hand == 0:
            self.winner = 'B'

    def is_over(self):
        """Check if the game is over."""
        return self.winner is not None
