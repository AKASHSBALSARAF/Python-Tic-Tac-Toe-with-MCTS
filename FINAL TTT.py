import tkinter as tk
import tkinter.messagebox as messagebox
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.ai_player = 'O'
        self.empty_cell = ' '
        self.is_game_over = False

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def check_draw(self):
        return all(cell != self.empty_cell for cell in self.board)

    def make_move(self, move, player):
        if self.board[move] == self.empty_cell and not self.is_game_over:
            self.board[move] = player
            if self.check_winner(player):
                self.is_game_over = True
                return f"{player} wins!"
            elif self.check_draw():
                self.is_game_over = True
                return "It's a draw!"
            return None
        return "Invalid move"

    def play_random_simulation(self, board, player):
        while True:
            available_moves = [i for i in range(9) if board[i] == self.empty_cell]
            if not available_moves:
                return self.empty_cell

            move = random.choice(available_moves)
            board[move] = player

            if self.check_winner(player):
                return player
            elif self.check_draw():
                return self.empty_cell

            player = self.ai_player if player == 'X' else 'X'

    def monte_carlo_simulation(self, move, player, num_simulations=1000):
        wins = 0
        for _ in range(num_simulations):
            board_copy = self.board[:]
            board_copy[move] = player
            current_player = self.current_player
            self.current_player = self.ai_player if player == 'X' else 'X'
            result = self.play_random_simulation(board_copy, self.current_player)
            if result == self.ai_player:
                wins += 1
            self.current_player = current_player
        return wins

    def get_best_move(self):
        best_move = None
        best_win_rate = -1

        for move in self.get_available_moves():
            win_rate = self.monte_carlo_simulation(move, self.ai_player)
            if win_rate > best_win_rate:
                best_move = move
                best_win_rate = win_rate

        return best_move

    def get_available_moves(self):
        return [i for i in range(9) if self.board[i] == self.empty_cell]


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.buttons = []

        for i in range(9):
            button = tk.Button(self.root, text='', width=8, height=3, command=lambda i=i: self.on_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        # AI makes the first move from the center (position 4)
        ai_move = 4
        self.buttons[ai_move]['text'] = self.game.ai_player
        self.game.make_move(ai_move, self.game.ai_player)

    def on_click(self, position):
        if self.buttons[position]['text'] == '' and not self.game.is_game_over:
            self.buttons[position]['text'] = self.game.current_player
            result = self.game.make_move(position, self.game.current_player)
            if result is not None:
                messagebox.showinfo("Game Over", result)
            else:
                self.game.current_player = 'X' if self.game.current_player == 'O' else 'O'
                if not self.game.is_game_over:
                    ai_move = self.game.get_best_move()
                    self.buttons[ai_move]['text'] = self.game.ai_player
                    result = self.game.make_move(ai_move, self.game.ai_player)
                    if result is not None:
                        messagebox.showinfo("Game Over", result)
                    else:
                        self.game.current_player = 'X' if self.game.current_player == 'O' else 'O'

if __name__ == "__main__":
    root = tk.Tk()
    game_gui = TicTacToeGUI(root)
    root.mainloop()
