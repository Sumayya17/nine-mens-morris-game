# gui.py

import tkinter as tk
from tkinter import messagebox
from game_logic import Game
from utils import adjacency_list

class GameGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Nine Men's Morris")
        self.canvas_size = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg='orange')
        self.canvas.pack()
        self.piece_radius = 15
        self.positions = self.calculate_positions()
        self.board_items = {}
        self.create_board()
        self.status_label = tk.Label(self.root, text="Player W's turn. Place your pieces.")
        self.status_label.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

    def calculate_positions(self):
        """Calculate the pixel positions of the board points."""
        size = self.canvas_size
        margin = size * 0.1  # 10% margin
        center = size / 2
        positions = {}

        # Define offsets for the squares
        outer_offset = margin
        middle_offset = margin + (size - 2 * margin) * 1 / 6
        inner_offset = margin + (size - 2 * margin) * 2 / 6

        # Helper function to get coordinates
        def get_coords(offset_x, offset_y):
            return (offset_x, offset_y)

        # Outer square positions
        positions[0] = get_coords(outer_offset, outer_offset)
        positions[1] = get_coords(center, outer_offset)
        positions[2] = get_coords(size - outer_offset, outer_offset)
        positions[9] = get_coords(outer_offset, center)
        positions[14] = get_coords(size - outer_offset, center)
        positions[21] = get_coords(outer_offset, size - outer_offset)
        positions[22] = get_coords(center, size - outer_offset)
        positions[23] = get_coords(size - outer_offset, size - outer_offset)

        # Middle square positions
        positions[3] = get_coords(middle_offset, middle_offset)
        positions[4] = get_coords(center, middle_offset)
        positions[5] = get_coords(size - middle_offset, middle_offset)
        positions[10] = get_coords(middle_offset, center)
        positions[13] = get_coords(size - middle_offset, center)
        positions[18] = get_coords(middle_offset, size - middle_offset)
        positions[19] = get_coords(center, size - middle_offset)
        positions[20] = get_coords(size - middle_offset, size - middle_offset)

        # Inner square positions
        positions[6] = get_coords(inner_offset, inner_offset)
        positions[7] = get_coords(center, inner_offset)
        positions[8] = get_coords(size - inner_offset, inner_offset)
        positions[11] = get_coords(inner_offset, center)
        positions[12] = get_coords(size - inner_offset, center)
        positions[15] = get_coords(inner_offset, size - inner_offset)
        positions[16] = get_coords(center, size - inner_offset)
        positions[17] = get_coords(size - inner_offset, size - inner_offset)

        return positions

    def create_board(self):
        """Create the board lines and positions."""
        # Draw the squares
        squares = [
            [0, 1, 2, 14, 23, 22, 21, 9],   # Outer square
            [3, 4, 5, 13, 20, 19, 18, 10],  # Middle square
            [6, 7, 8, 12, 17, 16, 15, 11]   # Inner square
        ]
        for square in squares:
            coords = [self.positions[pos] for pos in square]
            for i in range(len(coords)):
                self.canvas.create_line(coords[i], coords[(i + 1) % len(coords)], fill='black', width=2)

        # Draw the connecting lines
        connections = [
            (1, 4), (4, 7), (16, 19), (19, 22),
            (9, 10), (10, 11), (12, 13), (13, 14),
            (0, 3), (3, 6), (5, 8), (8, 2),
            (15, 18), (18, 21), (17, 20), (20, 23)
        ]
        for conn in connections:
            self.canvas.create_line(self.positions[conn[0]], self.positions[conn[1]], fill='black', width=2)

        # Draw the positions (circles)
        for pos, (x, y) in self.positions.items():
            item = self.canvas.create_oval(
                x - self.piece_radius, y - self.piece_radius,
                x + self.piece_radius, y + self.piece_radius,
                fill='orange', outline='black', width=2
            )
            self.board_items[pos] = item

    def update_board(self):
        """Update the GUI to reflect the current board state."""
        for pos in range(24):
            piece = self.game.board[pos]
            item = self.board_items[pos]
            if piece == 'W':
                self.canvas.itemconfig(item, fill='white')
            elif piece == 'B':
                self.canvas.itemconfig(item, fill='black')
            else:
                self.canvas.itemconfig(item, fill='orange')
            # Reset outlines
            self.canvas.itemconfig(item, outline='black', width=2)
        self.status_label['text'] = f"Player {self.game.current_player}'s turn. Place your pieces."

    def handle_click(self, event):
        """Handle user clicks on the board."""
        if self.game.is_over():
            messagebox.showinfo("Game Over", f"Player {self.game.winner} wins!")
            return

        clicked_pos = self.get_clicked_position(event.x, event.y)
        if clicked_pos is None:
            return

        success, message = self.game.place_piece(clicked_pos)
        if success:
            self.update_board()
            if "Mill formed" in message:
                self.status_label['text'] = "Mill formed! Remove an opponent's piece."
                self.root.after(100, self.prompt_remove_piece)
            else:
                self.check_game_over()
        else:
            messagebox.showerror("Invalid Move", message)

    def get_clicked_position(self, x, y):
        """Determine which position was clicked based on x and y coordinates."""
        for pos, (px, py) in self.positions.items():
            distance = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            if distance <= self.piece_radius:
                return pos
        return None

    def prompt_remove_piece(self):
        """Prompt the player to remove an opponent's piece."""
        self.status_label['text'] = "Select an opponent's piece to remove."
        self.canvas.bind("<Button-1>", self.handle_remove_click)

    def handle_remove_click(self, event):
        """Handle the click event for removing an opponent's piece."""
        clicked_pos = self.get_clicked_position(event.x, event.y)
        if clicked_pos is None:
            return
        opponent = 'B' if self.game.current_player == 'W' else 'W'
        if self.game.board[clicked_pos] != opponent:
            messagebox.showerror("Invalid Move", "You must select an opponent's piece.")
            return
        success, message = self.game.remove_piece(clicked_pos)
        if success:
            self.update_board()
            self.check_game_over()
            self.canvas.bind("<Button-1>", self.handle_click)
        else:
            messagebox.showerror("Invalid Move", message)

    def check_game_over(self):
        """Check if the game is over and display a message."""
        if self.game.is_over():
            messagebox.showinfo("Game Over", f"Player {self.game.winner} wins!")
            self.root.destroy()

    def start(self):
        """Start the GUI event loop."""
        self.update_board()
        self.root.mainloop()
