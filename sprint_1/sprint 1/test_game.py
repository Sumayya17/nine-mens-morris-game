# test_game.py

import unittest
from game_logic import Game

class TestGamePiecePlacement(unittest.TestCase):
    def test_piece_placement(self):
        game = Game()
        # Player W places a piece at position 0
        success, message = game.place_piece(0)
        self.assertTrue(success)
        self.assertEqual(game.board[0], 'W')
        self.assertEqual(game.current_player, 'B')
        # Player B places a piece at position 1
        success, message = game.place_piece(1)
        self.assertTrue(success)
        self.assertEqual(game.board[1], 'B')
        self.assertEqual(game.current_player, 'W')
        # Attempt to place on an occupied position
        success, message = game.place_piece(0)
        self.assertFalse(success)
        self.assertEqual(message, "Position already occupied.")
        # Place remaining pieces
        positions = [2, 3, 4, 5, 6, 7, 8, 9]
        for pos in positions:
            success, message = game.place_piece(pos)
            self.assertTrue(success)
        # Check win condition (should not be over yet)
        self.assertFalse(game.is_over())

    def test_mill_formation(self):
        game = Game()
        # Player W places at 0, Player B at 3, Player W at 1, Player B at 4, Player W at 2 forming a mill
        game.place_piece(0)  # W
        game.place_piece(3)  # B
        game.place_piece(1)  # W
        game.place_piece(4)  # B
        success, message = game.place_piece(2)  # W forms a mill
        self.assertTrue(success)
        self.assertEqual(message, "Mill formed. Remove an opponent's piece.")
        # Ensure the game is still not over
        self.assertFalse(game.is_over())

    def test_piece_removal(self):
        game = Game()
        # Setup a mill for Player W
        game.place_piece(0)  # W
        game.place_piece(3)  # B
        game.place_piece(1)  # W
        game.place_piece(4)  # B
        game.place_piece(2)  # W forms a mill
        # Player W removes Player B's piece at position 3
        success, message = game.remove_piece(3)
        self.assertTrue(success)
        self.assertEqual(game.board[3], ' ')
        self.assertEqual(game.current_player, 'B')

    def test_win_condition(self):
        game = Game()
        # Reduce Player B's pieces to less than 3
        game.black_pieces_on_board = 2
        game.black_pieces_in_hand = 0
        game.check_win_condition()
        self.assertTrue(game.is_over())
        self.assertEqual(game.winner, 'W')

    def test_piece_placement_limit(self):
        game = Game()
        # Player W places 9 pieces
        for pos in range(9):
            game.current_player = 'W'  # Manually set current player to W
            success, message = game.place_piece(pos)
            self.assertTrue(success)
        # Attempt to place a 10th piece for Player W
        game.current_player = 'W'  # Ensure it's Player W's turn
        success, message = game.place_piece(9)
        self.assertFalse(success)
        self.assertEqual(message, "No pieces left to place.")

if __name__ == '__main__':
    unittest.main()
