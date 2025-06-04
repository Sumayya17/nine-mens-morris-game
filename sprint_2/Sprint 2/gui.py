#gui.py
import tkinter as tk
from tkinter import messagebox, filedialog
from game_logic import Game
from ai import AIPlayer
from utils import adjacency_list, check_mill
import copy

class GameGUI:
    def __init__(self, game, root):
        self.game = game
        self.root = root
        self.create_menu()
        self.canvas_size = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg='orange')
        self.canvas.pack()
        self.piece_radius = 15
        self.positions = self.calculate_positions()
        self.board_items = {}
        self.selected_piece = None
        self.create_board()
        self.status_label = tk.Label(self.root, text="Player W's turn. Phase 1: Placing pieces.")
        self.status_label.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.is_replaying = False
        self.is_playing = False
        self.playback_after_id = None
        self.replay_index = 0
        self.saved_game_state = None
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.record_button = tk.Button(self.button_frame, text="Record", command=self.start_recording)
        self.rewind_button = tk.Button(self.button_frame, text="⏪", command=self.rewind)
        self.back_button = tk.Button(self.button_frame, text="◀️", command=self.step_back)
        self.play_pause_button = tk.Button(self.button_frame, text="⏯️", command=self.play_pause)
        self.next_button = tk.Button(self.button_frame, text="▶️", command=self.step_forward)
        self.forward_button = tk.Button(self.button_frame, text="⏩", command=self.forward)
        self.resume_button = tk.Button(self.button_frame, text="Resume", command=self.resume_game)
        self.save_button = tk.Button(self.button_frame, text="Save Game", command=self.save_game)
        self.record_button.pack(side=tk.LEFT)
        self.rewind_button.pack(side=tk.LEFT)
        self.back_button.pack(side=tk.LEFT)
        self.play_pause_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.forward_button.pack(side=tk.LEFT)
        self.resume_button.pack(side=tk.LEFT)
        self.save_button.pack(side=tk.LEFT)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Game', menu=game_menu)
        game_menu.add_command(label='Load Game', command=self.load_game)
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.root.quit)

    def calculate_positions(self):
        size = self.canvas_size
        margin = size * 0.1
        center = size / 2
        positions = {}
        outer_offset = margin
        middle_offset = margin + (size - 2 * margin) * 1 / 6
        inner_offset = margin + (size - 2 * margin) * 2 / 6

        def get_coords(offset_x, offset_y):
            return (offset_x, offset_y)

        positions[0] = get_coords(outer_offset, outer_offset)
        positions[1] = get_coords(center, outer_offset)
        positions[2] = get_coords(size - outer_offset, outer_offset)
        positions[9] = get_coords(outer_offset, center)
        positions[14] = get_coords(size - outer_offset, center)
        positions[21] = get_coords(outer_offset, size - outer_offset)
        positions[22] = get_coords(center, size - outer_offset)
        positions[23] = get_coords(size - outer_offset, size - outer_offset)
        positions[3] = get_coords(middle_offset, middle_offset)
        positions[4] = get_coords(center, middle_offset)
        positions[5] = get_coords(size - middle_offset, middle_offset)
        positions[10] = get_coords(middle_offset, center)
        positions[13] = get_coords(size - middle_offset, center)
        positions[18] = get_coords(middle_offset, size - middle_offset)
        positions[19] = get_coords(center, size - middle_offset)
        positions[20] = get_coords(size - middle_offset, size - middle_offset)
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
        squares = [
            [0, 1, 2, 14, 23, 22, 21, 9],
            [3, 4, 5, 13, 20, 19, 18, 10],
            [6, 7, 8, 12, 17, 16, 15, 11]
        ]
        for square in squares:
            coords = [self.positions[pos] for pos in square]
            for i in range(len(coords)):
                self.canvas.create_line(coords[i], coords[(i + 1) % len(coords)], fill='black', width=2)
        connections = [
            (1, 4), (4, 7), (16, 19), (19, 22),
            (9, 10), (10, 11), (12, 13), (13, 14),
            (0, 3), (3, 6), (6, 11), (11, 15), (15, 18), (18, 21),
            (2, 5), (5, 8), (8, 12), (12, 17), (17, 20), (20, 23)
        ]
        for conn in connections:
            self.canvas.create_line(self.positions[conn[0]], self.positions[conn[1]], fill='black', width=2)
        for pos, (x, y) in self.positions.items():
            item = self.canvas.create_oval(
                x - self.piece_radius, y - self.piece_radius,
                x + self.piece_radius, y + self.piece_radius,
                fill='orange', outline='black', width=2
            )
            self.board_items[pos] = item

    def update_board(self):
        for pos in range(24):
            piece = self.game.board[pos]
            item = self.board_items[pos]
            if piece == 'W':
                self.canvas.itemconfig(item, fill='white')
            elif piece == 'B':
                self.canvas.itemconfig(item, fill='black')
            else:
                self.canvas.itemconfig(item, fill='orange')
            self.canvas.itemconfig(item, outline='black', width=2)
        if not self.is_replaying:
            player_phase = self.game.white_phase if self.game.current_player == 'W' else self.game.black_phase
            phase_text = "Flying phase" if player_phase == 3 else f"Phase {self.game.phase}"
            self.status_label['text'] = f"Player {self.game.current_player}'s turn. {phase_text}."
        else:
            self.status_label['text'] = f"Replaying move {self.replay_index} of {len(self.game.move_history)}"

    def handle_click(self, event):
        if self.is_replaying:
            return
        if self.game.is_over():
            self.end_game()
            return
        if self.game.ai_player and self.game.current_player == 'B':
            return
        clicked_pos = self.get_clicked_position(event.x, event.y)
        if clicked_pos is None:
            return
        if self.game.phase == 1:
            self.handle_phase_one(clicked_pos)
        elif self.game.phase >= 2:
            self.handle_phase_two(clicked_pos)

    def end_game(self):
        messagebox.showinfo("Game Over", f"Player {self.game.winner} wins!")
        self.canvas.unbind("<Button-1>")
        self.root.destroy()
        from main import main
        main()

    def handle_phase_one(self, clicked_pos):
        success, message = self.game.place_piece(clicked_pos)
        if success:
            self.update_board()
            if "Mill formed" in message:
                self.prompt_mill_removal()
            else:
                self.check_game_over()
                self.ai_move()
        else:
            self.show_error("Invalid Move", message)

    def handle_phase_two(self, clicked_pos):
        if self.selected_piece is None:
            self.select_piece(clicked_pos)
        else:
            self.move_selected_piece(clicked_pos)

    def prompt_mill_removal(self):
        self.status_label['text'] = "Mill formed! Remove an opponent's piece."
        self.root.after(100, self.prompt_remove_piece)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def select_piece(self, clicked_pos):
        if self.game.board[clicked_pos] == self.game.current_player:
            self.selected_piece = clicked_pos
            self.canvas.itemconfig(self.board_items[clicked_pos], outline='yellow', width=4)

    def move_selected_piece(self, clicked_pos):
        success, message = self.game.move_piece(self.selected_piece, clicked_pos)
        self.canvas.itemconfig(self.board_items[self.selected_piece], outline='black', width=2)
        if success:
            self.update_board()
            self.selected_piece = None
            if "Mill formed" in message:
                self.prompt_mill_removal()
            else:
                self.check_game_over()
                self.ai_move()
        else:
            self.show_error("Invalid Move", message)
            self.selected_piece = None

    def get_clicked_position(self, x, y):
        for pos, (px, py) in self.positions.items():
            distance = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            if distance <= self.piece_radius:
                return pos
        return None

    def prompt_remove_piece(self):
        self.status_label['text'] = "Select an opponent's piece to remove."
        self.canvas.bind("<Button-1>", self.handle_remove_click)

    def handle_remove_click(self, event):
        try:
            if not self.root.winfo_exists():
                return
        except tk.TclError:
            return
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
            if self.root.winfo_exists():
                self.canvas.bind("<Button-1>", self.handle_click)
                self.ai_move()
        else:
            messagebox.showerror("Invalid Move", message)

    def ai_move(self):
        if self.game.ai_player and self.game.current_player == 'B':
            self.status_label['text'] = "AI is thinking..."
            self.root.after(1000, self.perform_ai_move)

    def perform_ai_move(self):
        move = self.game.ai_player.get_move(self.game)
        if move is None:
            self.game.winner = 'W'
            self.check_game_over()
            return
        if move[0] == 'place':
            self.game.place_piece(move[1])
            move_pos = move[1]
        elif move[0] == 'move':
            self.game.move_piece(move[1], move[2])
            move_pos = move[2]
        self.update_board()
        if self.game.check_win_condition():
            self.end_game()
            return
        if check_mill(self.game.board, move_pos):
            self.perform_ai_remove_piece()
        else:
            self.update_board()

    def perform_ai_remove_piece(self):
        opponent = 'W'
        for pos in range(24):
            if self.game.board[pos] == opponent:
                self.game.remove_piece(pos)
                break
        self.update_board()
        if self.game.check_win_condition():
            self.end_game()
        else:
            self.update_board()

    def check_game_over(self):
        if self.game.check_win_condition():
            self.end_game()

    def save_game(self):
        filename = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON Files', '*.json')],
            title='Save Game'
        )
        if filename:
            self.game.save_game(filename)
            messagebox.showinfo("Save Game", "Game saved successfully.")

    def load_game(self):
        filename = filedialog.askopenfilename(
            defaultextension='.json',
            filetypes=[('JSON Files', '*.json')],
            title='Load Game'
        )
        if filename:
            self.game.load_game(filename)
            self.update_board()
            messagebox.showinfo("Load Game", "Game loaded successfully.")

    def start(self):
        self.update_board()
        self.root.mainloop()

    def start_recording(self):
        if self.game.record_game:
            messagebox.showinfo("Recording", "Recording is already in progress.")
            return
        self.game.record_game = True
        messagebox.showinfo("Recording", "Game recording started.")

    def rewind(self):
        if self.is_playing:
            self.is_playing = False
            if self.playback_after_id:
                self.root.after_cancel(self.playback_after_id)
                self.playback_after_id = None
        if not self.game.move_history:
            messagebox.showinfo("Rewind", "No moves to rewind.")
            return
        if not self.is_replaying:
            self.saved_game_state = copy.deepcopy(self.game)
        self.is_replaying = True
        self.replay_index = 0
        self.replay_game_state()

    def step_back(self):
        if self.is_playing:
            self.is_playing = False
            if self.playback_after_id:
                self.root.after_cancel(self.playback_after_id)
                self.playback_after_id = None
        if not self.game.move_history or self.replay_index <= 0:
            messagebox.showinfo("Back", "No previous moves.")
            return
        if not self.is_replaying:
            self.saved_game_state = copy.deepcopy(self.game)
            self.replay_index = len(self.game.move_history)
        self.is_replaying = True
        self.replay_index -= 1
        self.replay_game_state()

    def play_pause(self):
        if not self.game.move_history:
            messagebox.showinfo("Play/Pause", "No moves to play.")
            return
        if not self.is_replaying:
            self.saved_game_state = copy.deepcopy(self.game)
            self.replay_index = 0
            self.is_replaying = True
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_replay()
        else:
            if self.playback_after_id:
                self.root.after_cancel(self.playback_after_id)
                self.playback_after_id = None

    def step_forward(self):
        if self.is_playing:
            self.is_playing = False
            if self.playback_after_id:
                self.root.after_cancel(self.playback_after_id)
                self.playback_after_id = None
        if not self.game.move_history or self.replay_index >= len(self.game.move_history):
            messagebox.showinfo("Next", "No next moves.")
            return
        if not self.is_replaying:
            self.saved_game_state = copy.deepcopy(self.game)
            self.replay_index = 0
        self.is_replaying = True
        self.replay_index += 1
        self.replay_game_state()

    def forward(self):
        if self.is_playing:
            self.is_playing = False
            if self.playback_after_id:
                self.root.after_cancel(self.playback_after_id)
                self.playback_after_id = None
        if not self.game.move_history:
            messagebox.showinfo("Forward", "No moves to fast forward.")
            return
        if not self.is_replaying:
            self.saved_game_state = copy.deepcopy(self.game)
        self.is_replaying = True
        self.replay_index = len(self.game.move_history)
        self.replay_game_state()

    def resume_game(self):
        if self.is_playing:
            self.is_playing = False
            if self.playback_after_id:
                self.root.after_cancel(self.playback_after_id)
                self.playback_after_id = None
        if self.saved_game_state is not None:
            self.game = self.saved_game_state
            self.saved_game_state = None
            self.is_replaying = False
            self.is_playing = False
            self.replay_index = 0
            self.update_board()
            self.canvas.bind("<Button-1>", self.handle_click)
            self.status_label['text'] = f"Player {self.game.current_player}'s turn. Phase {self.game.phase}."
        else:
            messagebox.showinfo("Resume", "Not in replay mode.")

    def replay_game_state(self):
        if self.replay_index < 0:
            self.replay_index = 0
        elif self.replay_index > len(self.game.move_history):
            self.replay_index = len(self.game.move_history)
        replay_game = Game()
        replay_game.record_game = False
        for i in range(self.replay_index):
            move = self.game.move_history[i]
            replay_game.make_move(move)
        self.game.board = replay_game.board.copy()
        self.game.current_player = replay_game.current_player
        self.game.phase = replay_game.phase
        self.game.white_pieces_in_hand = replay_game.white_pieces_in_hand
        self.game.black_pieces_in_hand = replay_game.black_pieces_in_hand
        self.game.white_pieces_on_board = replay_game.white_pieces_on_board
        self.game.black_pieces_on_board = replay_game.black_pieces_on_board
        self.game.winner = replay_game.winner
        self.update_board()
        self.canvas.unbind("<Button-1>")

    def play_replay(self):
        if self.replay_index >= len(self.game.move_history):
            self.is_playing = False
            self.playback_after_id = None
            return
        self.replay_index += 1
        self.replay_game_state()
        if self.is_playing:
            self.playback_after_id = self.root.after(1000, self.play_replay)
