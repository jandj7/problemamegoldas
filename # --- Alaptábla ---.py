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
def is_valid(board, row, col, num):
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
def find_empty(board):
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                return r, c
    return None

# --- Visszalépéses megoldó ---
def solve(board):
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

# --- Kiválasztott cella nyilvántartása ---
selected_cell = [0, 0]

# --- Billentyűzet kezelése ---
def on_key_press(event):
    global selected_cell
    r, c = selected_cell
    
    # Szám bevitele
    if event.key.isdigit() and 1 <= int(event.key) <= 6:
        num = int(event.key)
        if is_valid(initial_board, r, c, num):
            initial_board[r][c] = num
            draw_board(initial_board, initial_board, "Manuális kitöltés", ax)
    
    # Navigálás a táblán nyilakkal
    if event.key == "up":
        selected_cell[0] = (r - 1) % N
    elif event.key == "down":
        selected_cell[0] = (r + 1) % N
    elif event.key == "left":
        selected_cell[1] = (c - 1) % N
    elif event.key == "right":
        selected_cell[1] = (c + 1) % N
    draw_board(initial_board, initial_board, "Manuális kitöltés", ax)

# --- Tábla kirajzolása ---
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button


def draw_board(board, initial, title, ax):
    ax.clear()
    ax.set_xlim(-0.05, N + 0.05)
    ax.set_ylim(-0.05, N + 0.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=20, pad=15, fontweight='bold', color='#2c3e50')
    ax.invert_yaxis()
    ax.axis('off')

    # Cellák és háttér
    for i in range(N):
        for j in range(N):
            val = board[i][j]
            is_diag = (i, j) in main_diag or (i, j) in anti_diag
            bg_color = '#fdf6b2' if is_diag else '#ffffff'

            rect = patches.FancyBboxPatch(
                (j, i), 1, 1,
                boxstyle="square,pad=0.02",
                linewidth=1,
                edgecolor='#333',
                facecolor=bg_color
            )
            ax.add_patch(rect)

            if val != 0:
                text_color = "#2980b9" if initial[i][j] != 0 else "#27ae60"
                ax.text(j + 0.5, i + 0.5, str(val),
                        ha='center', va='center',
                        fontsize=22, weight='bold', color=text_color)

    # Kiválasztott cella kiemelése
    r, c = selected_cell
    ax.add_patch(patches.Rectangle((c, r), 1, 1, linewidth=3, edgecolor='#e74c3c', facecolor='none'))

    ax.figure.canvas.draw()


# --- Megjelenítés ---
fig, ax = plt.subplots(figsize=(7, 7))
plt.subplots_adjust(bottom=0.2)
draw_board(initial_board, initial_board, "Alapfeladvány", ax)
fig.canvas.mpl_connect('key_press_event', on_key_press)

# --- Gombok: Megoldás és Kilépés ---

def solve_button(event):
    solution = solve([row[:] for row in initial_board])
    if solution:
        draw_board(solution, initial_board, "Megoldott tábla", ax)
    else:
        draw_board(initial_board, initial_board, "Nincs megoldás!", ax)

def exit_button(event):
    plt.close(fig)

solve_ax = plt.axes([0.30, 0.01, 0.4, 0.07])
solve_btn = Button(solve_ax, 'Megoldás')
solve_btn.on_clicked(solve_button)

exit_ax = plt.axes([0.30, 0.1, 0.4, 0.08])
exit_btn = Button(exit_ax, 'Kilépés', color='#f8d7da', hovercolor='#f5c6cb')
exit_btn.on_clicked(exit_button)

plt.show()