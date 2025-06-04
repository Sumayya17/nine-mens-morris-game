#ai.py
import math
import copy
from utils import evaluate_board
from game_logic import Game

class AIPlayer:
    def __init__(self, depth=3):
        self.depth = depth

    def get_move(self, game):
        """Get the best move for the AI player."""
        best_score = -math.inf
        best_move = None
        player = game.current_player
        possible_moves = game.get_possible_moves(player)
        if not possible_moves:
            return None  # No possible moves
        for move in possible_moves:
            temp_game = copy.deepcopy(game)
            temp_game.record_game = False  # Prevent recording during AI simulation
            temp_game.make_move(move)
            score = self.minimax(temp_game, self.depth - 1, -math.inf, math.inf, False, player)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing_player, player):
        """Minimax algorithm with alpha-beta pruning."""
        opponent = 'B' if player == 'W' else 'W'
        if depth == 0 or game.is_over():
            return evaluate_board(game.board, player)
        possible_moves = game.get_possible_moves(player if maximizing_player else opponent)
        if not possible_moves:
            return evaluate_board(game.board, player)
        if maximizing_player:
            max_eval = -math.inf
            for move in possible_moves:
                temp_game = copy.deepcopy(game)
                temp_game.record_game = False  # Prevent recording during AI simulation
                temp_game.make_move(move)
                eval = self.minimax(temp_game, depth - 1, alpha, beta, False, player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in possible_moves:
                temp_game = copy.deepcopy(game)
                temp_game.record_game = False  # Prevent recording during AI simulation
                temp_game.make_move(move)
                eval = self.minimax(temp_game, depth - 1, alpha, beta, True, player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
