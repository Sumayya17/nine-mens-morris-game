#main.py
from game_logic import Game
from ai import AIPlayer
from gui import GameGUI
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    game_mode = simpledialog.askstring(
        "Game Mode",
        "Select game mode:\n1. Human vs Human\n2. Human vs AI\n3. Load Saved Game\nEnter 1, 2, or 3:",
        parent=root
    )
    root.destroy()
    if game_mode == '1':
        root = tk.Tk()
        game = Game()
        gui = GameGUI(game, root)
        gui.start()
    elif game_mode == '2':
        root = tk.Tk()
        ai_player = AIPlayer(depth=3)
        game = Game(ai_player=ai_player)
        game.current_player = 'W'  # Ensure the human starts first
        gui = GameGUI(game, root)
        gui.start()
    elif game_mode == '3':
        filename = filedialog.askopenfilename(
            defaultextension='.json',
            filetypes=[('JSON Files', '*.json')],
            title='Load Game'
        )
        if filename:
            root = tk.Tk()
            game = Game()
            game.load_game(filename)
            # Check if the game involves an AI player
            ai_option = messagebox.askyesno("AI Player", "Is this a game against the AI?")
            if ai_option:
                ai_player = AIPlayer(depth=3)
                game.ai_player = ai_player
            gui = GameGUI(game, root)
            gui.update_board()
            gui.start()
        else:
            messagebox.showerror("Load Game", "No file selected. Exiting.")
            main()  # Restart the main menu
    else:
        messagebox.showerror("Invalid Selection", "Please enter a valid option (1, 2, or 3).")
        main()  # Restart the main menu

if __name__ == "__main__":
    main()
