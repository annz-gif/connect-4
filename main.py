import tkinter as tk
from tkinter import messagebox
import copy

class ConnectFour:
    def _init_(self, rows=6, cols=7):
        self.window = tk.Tk()
        self.window.title("Connect Four")
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.current_player = 'X'
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                self.buttons[i][j] = tk.Button(self.window, text='', font=('normal', 20), width=2, height=1,
                                              command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.check_tie():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.make_computer_move()

    def check_winner(self):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3] != ' ':
                    return True
        # Check vertical
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col] != ' ':
                    return True
        # Check diagonal \
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3] != ' ':
                    return True
        # Check diagonal /
        for row in range(self.rows - 3):
            for col in range(3, self.cols):
                if self.board[row][col] == self.board[row + 1][col - 1] == self.board[row + 2][col - 2] == self.board[row + 3][col - 3] != ' ':
                    return True
        return False

    def check_tie(self):
        return all(self.board[i][j] != ' ' for i in range(self.rows) for j in range(self.cols))

    def reset_game(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text='')
        self.current_player = 'X'

    def make_computer_move(self):
        best_score = float('-inf')
        best_col = None

        for col in range(self.cols):
            if self.is_valid_move(col):
                row = self.get_next_open_row(col)
                temp_board = copy.deepcopy(self.board)
                temp_board[row][col] = 'O'
                score = self.minimax(temp_board, 0, False)
                if score > best_score:
                    best_score = score
                    best_col = col

        if best_col is not None:
            row = self.get_next_open_row(best_col)
            self.board[row][best_col] = 'O'
            self.buttons[row][best_col].config(text='O')
            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
                self.reset_game()
            elif self.check_tie():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = 'X'

    def is_valid_move(self, col):
        return self.board[0][col] == ' '

    def get_next_open_row(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == ' ':
                return row
        return -1

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner():
            return -1 if is_maximizing else 1
        elif self.check_tie():
            return 0

        player = 'O' if is_maximizing else 'X'
        best_score = float('-inf') if is_maximizing else float('inf')

        for col in range(self.cols):
            if self.is_valid_move(col):
                row = self.get_next_open_row(col)
                temp_board = copy.deepcopy(board)
                temp_board[row][col] = player
                score = self.minimax(temp_board, depth + 1, not is_maximizing)

                if is_maximizing:
                    best_score = max(best_score, score)
                else:
                    best_score = min(best_score, score)

        return best_score

    def run(self):
        self.window.mainloop()


if _name_ == "_main_":
    game = ConnectFour()
    game.run()