import json
from utils import check_mill, is_adjacent, count_pieces, adjacency_list

class Game:
    def __init__(self, ai_player=None, record_game=False):
        self.board = [' '] * 24
        self.current_player = 'W'
        self.ai_player = ai_player
        self.phase = 1  # Game phases: 1 = placing pieces, 2 = moving pieces
        self.white_phase = 1  # Individual phases for flying
        self.black_phase = 1
        self.move_history = []
        self.white_pieces_in_hand = 9
        self.black_pieces_in_hand = 9
        self.white_pieces_on_board = 0
        self.black_pieces_on_board = 0
        self.record_game = record_game
        self.winner = None

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'B' if self.current_player == 'W' else 'W'

    def place_piece(self, position):
        """Place a piece on the board during phase 1."""
        if self.board[position] != ' ':
            return False, "Position already occupied."
        self.board[position] = self.current_player
        if self.current_player == 'W':
            self.white_pieces_in_hand -= 1
            self.white_pieces_on_board += 1
        else:
            self.black_pieces_in_hand -= 1
            self.black_pieces_on_board += 1
        if self.record_game:
            self.move_history.append(('place', position, self.current_player))

        formed_mill = check_mill(self.board, position)
        self.update_phase()
        if formed_mill:
            # Do not switch player; allow current player to remove an opponent's piece
            return True, "Mill formed. Remove an opponent's piece."
        else:
            self.switch_player()
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
        if self.record_game:
            self.move_history.append(('remove', position, opponent))

        self.update_phase()
        if self.check_win_condition():
            return True, "Game over."
        else:
            self.switch_player()
            return True, "Piece removed."

    def move_piece(self, from_pos, to_pos):
        """Move a piece during phase 2 or 3."""
        if self.board[from_pos] != self.current_player:
            return False, "You can only move your own pieces."
        if self.board[to_pos] != ' ':
            return False, "Destination position is occupied."
        player_phase = self.white_phase if self.current_player == 'W' else self.black_phase
        if player_phase == 2 and not is_adjacent(from_pos, to_pos):
            return False, "You can only move to adjacent positions."
        self.board[from_pos] = ' '
        self.board[to_pos] = self.current_player
        if self.record_game:
            self.move_history.append(('move', from_pos, to_pos, self.current_player))

        formed_mill = check_mill(self.board, to_pos)
        if formed_mill:
            # Do not switch player; allow current player to remove an opponent's piece
            return True, "Mill formed. Remove an opponent's piece."
        else:
            self.switch_player()
            return True, "Piece moved."

    def update_phase(self):
        """Update the game phase based on the state of the game."""
        if self.white_pieces_in_hand == 0 and self.black_pieces_in_hand == 0:
            self.phase = 2
        # Update individual player phases
        if self.white_pieces_on_board == 3 and self.phase >= 2:
            self.white_phase = 3
        else:
            self.white_phase = 2
        if self.black_pieces_on_board == 3 and self.phase >= 2:
            self.black_phase = 3
        else:
            self.black_phase = 2

    def check_win_condition(self):
        """Check if a player has won the game."""
        if self.black_pieces_on_board < 3 and self.phase >= 2:
            self.winner = 'W'
            return True
        if self.white_pieces_on_board < 3 and self.phase >= 2:
            self.winner = 'B'
            return True
        # Check if a player cannot move
        if self.phase >= 2:
            if not self.get_possible_moves(self.current_player):
                self.winner = 'B' if self.current_player == 'W' else 'W'
                return True
        return False

    def get_possible_moves(self, player):
        """Get all possible moves for the specified player."""
        moves = []
        if self.phase == 1:
            pieces_in_hand = self.white_pieces_in_hand if player == 'W' else self.black_pieces_in_hand
            if pieces_in_hand > 0:
                for i in range(24):
                    if self.board[i] == ' ':
                        moves.append(('place', i))
        if self.phase >= 2:
            player_phase = self.white_phase if player == 'W' else self.black_phase
            for i in range(24):
                if self.board[i] == player:
                    if player_phase == 3:
                        # Flying
                        for j in range(24):
                            if self.board[j] == ' ':
                                moves.append(('move', i, j))
                    else:
                        # Move to adjacent positions
                        for adj in adjacency_list[i]:
                            if self.board[adj] == ' ':
                                moves.append(('move', i, adj))
        return moves

    def is_over(self):
        """Check if the game is over."""
        return self.winner is not None

    def make_move(self, move):
        """Execute a move."""
        if move[0] == 'place':
            self.place_piece(move[1])
        elif move[0] == 'move':
            self.move_piece(move[1], move[2])
        elif move[0] == 'remove':
            self.remove_piece(move[1])

    def to_dict(self):
        """Convert the game state to a dictionary."""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'phase': self.phase,
            'white_phase': self.white_phase,
            'black_phase': self.black_phase,
            'white_pieces_in_hand': self.white_pieces_in_hand,
            'black_pieces_in_hand': self.black_pieces_in_hand,
            'white_pieces_on_board': self.white_pieces_on_board,
            'black_pieces_on_board': self.black_pieces_on_board,
            'winner': self.winner,
            'move_history': self.move_history
        }

    def from_dict(self, data):
        """Load the game state from a dictionary."""
        self.board = data['board']
        self.current_player = data['current_player']
        self.phase = data['phase']
        self.white_phase = data.get('white_phase', 2)
        self.black_phase = data.get('black_phase', 2)
        self.white_pieces_in_hand = data['white_pieces_in_hand']
        self.black_pieces_in_hand = data['black_pieces_in_hand']
        self.white_pieces_on_board = data['white_pieces_on_board']
        self.black_pieces_on_board = data['black_pieces_on_board']
        self.winner = data['winner']
        self.move_history = data.get('move_history', [])

    def save_game(self, filename):
        """Save the current game state to a file."""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)

    def load_game(self, filename):
        """Load the game state from a file."""
        with open(filename, 'r') as f:
            data = json.load(f)
            self.from_dict(data)
