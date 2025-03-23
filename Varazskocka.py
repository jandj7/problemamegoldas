from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

import sys

# --- Alaptábla ---
initial_board = [
    [0, 0, 6, 0, 0, 4],
    [0, 2, 0, 6, 0, 0],
    [0, 4, 0, 0, 0, 5],
    [2, 0, 0, 0, 6, 0],
    [0, 0, 4, 0, 5, 0],
    [5, 0, 0, 3, 0, 0],
]

N = 6
main_diag = {(i, i) for i in range(N)}
anti_diag = {(i, N - 1 - i) for i in range(N)}

# --- Érvényes-e egy szám ---
def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    for i in range(N):
        if board[row][i] == num or board[i][col] == num:
            return False
    if (row, col) in main_diag:
        for i in range(N):
            if board[i][i] == num and i != row:
                return False
    if (row, col) in anti_diag:
        for i in range(N):
            if board[i][N - 1 - i] == num and i != row:
                return False
    return True

# --- Üres mező keresése ---
def find_empty(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                return r, c
    return None

# --- Visszalépéses megoldó ---
def solve(board: List[List[int]]) -> Optional[List[List[int]]]:
    empty = find_empty(board)
    if not empty:
        return board
    r, c = empty
    for num in range(1, N + 1):
        if is_valid(board, r, c, num):
            board[r][c] = num
            result = solve(board)
            if result is not None:
                return result
            board[r][c] = 0
    return None

# --- Tábla kirajzolása ---
def draw_board(board: List[List[int]], initial: List[List[int]], title: str, ax):
    ax.clear()
    ax.set_xlim(-0.05, N + 0.05)
    ax.set_ylim(-0.05, N + 0.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=20, pad=25, fontweight='bold', color='#2c3e50')
    ax.invert_yaxis()
    ax.axis('off')

    # Külső keret
    border = patches.FancyBboxPatch(
        (0, 0), N, N,
        boxstyle="round,pad=0.02",
        linewidth=2,
        edgecolor='#2c3e50',
        facecolor='none'
    )
    ax.add_patch(border)

    # Cellák
    for i in range(N):
        for j in range(N):
            val = board[i][j]
            is_diag = (i, j) in main_diag or (i, j) in anti_diag
            bg_color = '#fdf6b2' if is_diag else '#ffffff'

            rect = patches.FancyBboxPatch(
                (j, i), 1, 1,
                boxstyle="round,pad=0.02",
                linewidth=1,
                edgecolor='#333',
                facecolor=bg_color
            )
            ax.add_patch(rect)

            if val != 0:
                text_color = "#2980b9" if initial[i][j] != 0 else "#27ae60"
                ax.text(j + 0.5, i + 0.5, str(val),
                        ha='center', va='center',
                        fontsize=18, weight='bold', color=text_color)

    ax.figure.canvas.draw()

# --- Megjelenítés ---
fig, ax = plt.subplots(figsize=(6.5, 6.5))
plt.subplots_adjust(bottom=0.3)  # több hely a gomboknak
draw_board(initial_board, initial_board, "Alapfeladvány", ax)

# --- Megoldásgomb ---
def on_solve_click(event):
    solution = solve([row[:] for row in initial_board])
    if solution:
        draw_board(solution, initial_board, "Megoldott tábla", ax)
    else:
        draw_board(initial_board, initial_board, "Nincs megoldás!", ax)

# --- Kilépésgomb ---
def on_exit_click(event):
    plt.close(fig)

# Gomb: Megoldás
btn_solve_ax = plt.axes([0.30, 0.1, 0.4, 0.08])
btn_solve = Button(btn_solve_ax, "Megoldás", color='#ecf0f1', hovercolor='#bdc3c7')
btn_solve.label.set_fontsize(14)
btn_solve.label.set_fontweight('bold')
btn_solve.label.set_color('#2c3e50')
btn_solve.on_clicked(on_solve_click)

# Gomb: Kilépés
btn_exit_ax = plt.axes([0.30, 0.01, 0.4, 0.07])
btn_exit = Button(btn_exit_ax, "Kilépés", color='#f8d7da', hovercolor='#f5c6cb')
btn_exit.label.set_fontsize(13)
btn_exit.label.set_fontweight('bold')
btn_exit.label.set_color('#721c24')
btn_exit.on_clicked(on_exit_click)

plt.show()