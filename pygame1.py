import tkinter as tk
from tkinter import messagebox
import random

# Constants for representing the players and empty cells
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

# Define the Tic-Tac-Toe board
board = [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]
]

# Function to check if the board is full
def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Function to check if the game is over
def is_game_over(board):
    return check_winner(board, HUMAN) or check_winner(board, AI) or is_full(board)

# Function to check if a player has won
def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to evaluate the board for the AI player
def evaluate_board(board):
    if check_winner(board, AI):
        return 1
    elif check_winner(board, HUMAN):
        return -1
    else:
        return 0

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if is_game_over(board):
        return evaluate_board(board)
    
    if is_maximizing:
        max_eval = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = AI
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = HUMAN
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Function to make the best move for the AI player
def make_ai_move():
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = AI
                eval = minimax(board, 0, False, alpha, beta)
                board[row][col] = EMPTY
                
                if eval > best_eval:
                    best_eval = eval
                    best_move = (row, col)
    
    if best_move:
        row, col = best_move
        buttons[row][col].config(text=AI, state=tk.DISABLED)
        board[row][col] = AI

# Function to handle human player's move
def human_move(row, col):
    if board[row][col] == EMPTY:
        buttons[row][col].config(text=HUMAN, state=tk.DISABLED)
        board[row][col] = HUMAN
        if not is_game_over(board):
            make_ai_move()
            if is_game_over(board):
                if check_winner(board, HUMAN):
                    messagebox.showinfo("Game Over", "You win!")
                elif check_winner(board, AI):
                    messagebox.showinfo("Game Over", "AI wins!")
                else:
                    messagebox.showinfo("Game Over", "It's a draw!")
            elif is_full(board):
                messagebox.showinfo("Game Over", "It's a draw!")
                
# Function to restart the game
def restart_game():
    global board
    board = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=EMPTY, state=tk.NORMAL)

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create buttons for the Tic-Tac-Toe grid
buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(root, text=EMPTY, font=('normal', 24), width=5, height=2,
                           command=lambda row=i, col=j: human_move(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Create a restart button
restart_button = tk.Button(root, text="Restart", command=restart_game)
restart_button.grid(row=3, column=1, columnspan=3)

# Start the game
make_ai_move()

# Run the Tkinter main loop
root.mainloop()
