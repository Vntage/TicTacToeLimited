import tkinter as tk
from tkinter import messagebox
from collections import deque

class TicTacToeLimited:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Tic Tac Toe: 3-Move Limit")
        self.init_game()

    def init_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.moves = {"X": deque(), "O": deque()}

        for widget in self.root.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=('Helvetica', 22, 'bold'),
                                width=5, height=2, bg="#f0f0f0",
                                command=lambda row=i, col=j: self.make_move(row, col))
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = btn

        self.label = tk.Label(self.root, text="Player X's Turn", font=('Helvetica', 14, 'bold'), fg="red")
        self.label.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        self.replay_button = tk.Button(self.root, text="🔁 Play Again", font=('Helvetica', 12),
                                       command=self.init_game, state="disabled", bg="#dddddd")
        self.replay_button.grid(row=4, column=0, columnspan=3, pady=10)

    def make_move(self, row, col):
        if self.board[row][col] != "":
            return

        player = self.current_player
        opponent = "O" if player == "X" else "X"

        # Reset ALL buttons to default bg before any move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != "":
                    self.buttons[i][j].config(bg="#f0f0f0")

        # Add new move
        self.board[row][col] = player
        color = "red" if player == "X" else "blue"
        self.buttons[row][col].config(text=player, fg=color)
        self.moves[player].append((row, col))

        # Remove oldest if more than 3
        if len(self.moves[player]) > 3:
            old_r, old_c = self.moves[player].popleft()
            self.board[old_r][old_c] = ""
            self.buttons[old_r][old_c].config(text="", bg="#f0f0f0")

        # Check win condition
        if self.check_winner(player):
            self.end_game(f"🎉 Player {player} Wins!")
            return

        # Highlight opponent's oldest move (about to be replaced)
        if len(self.moves[opponent]) == 3:
            old_r, old_c = self.moves[opponent][0]
            self.buttons[old_r][old_c].config(bg="#ffcccb")  # soft coral

        # Switch turn
        self.current_player = opponent
        next_color = "red" if self.current_player == "X" else "blue"
        self.label.config(text=f"Player {self.current_player}'s Turn", fg=next_color)

    def check_winner(self, player):
        positions = set(self.moves[player])
        win_combos = [
            {(0, 0), (0, 1), (0, 2)},
            {(1, 0), (1, 1), (1, 2)},
            {(2, 0), (2, 1), (2, 2)},
            {(0, 0), (1, 0), (2, 0)},
            {(0, 1), (1, 1), (2, 1)},
            {(0, 2), (1, 2), (2, 2)},
            {(0, 0), (1, 1), (2, 2)},
            {(0, 2), (1, 1), (2, 0)},
        ]
        for combo in win_combos:
            if combo.issubset(positions):
                for r, c in combo:
                    self.buttons[r][c].config(bg="#90ee90")  # light green
                return True
        return False

    def end_game(self, message):
        self.label.config(text=message, fg="green")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")
        messagebox.showinfo("Game Over", message)
        self.replay_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeLimited(root)
    root.mainloop()
