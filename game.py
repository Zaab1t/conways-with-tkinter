import tkinter as tk
from functools import partial


buttons = [  # (title, width, start_set)
    (
        "Pulsar",
        15,
        {
            (1, 3), (1, 4), (1, 5), (1, 9), (1, 10), (1, 11),
            (3, 1), (3, 6), (3, 8), (3, 13),
            (4, 1), (4, 6), (4, 8), (4, 13),
            (5, 1), (5, 6), (5, 8), (5, 13),
            (6, 3), (6, 4), (6, 5), (6, 9), (6, 10), (6, 11),
            (8, 3), (8, 4), (8, 5), (8, 9), (8, 10), (8, 11),
            (9, 1), (9, 6), (9, 8), (9, 13),
            (10, 1), (10, 6), (10, 8), (10, 13),
            (11, 1), (11, 6), (11, 8), (11, 13),
            (13, 3), (13, 4), (13, 5), (13, 9), (13, 10), (13, 11),
        },
    ),
    (
        "Glider",
        30,
        {(28, 28), (29, 28), (30, 28), (28, 29), (29, 30)},
    ),
    (
        "Tetris",
        11,
        {(5, 5), (4, 5), (5, 4), (5, 6)},
    ),
    (
        'Stable',
        8,
        {(3, 3), (4, 3), (3, 4), (4, 4)},
    ),
]


def neighbors_for_cell(x, y):
    return {
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y), (x+1, y),  # exclude center
        (x-1, y+1), (x, y+1), (x+1, y+1),
    }


def step(board):
    new_board = set()
    for cell in board:
        neighborhood = neighbors_for_cell(*cell)
        neighbors_alive = len(neighborhood & board)
        if neighbors_alive in (2, 3):  # should cell stay alive
            new_board.add(cell)

        # should any neighbors (re)spawn
        for neighbor in neighborhood:
            neighbors = neighbors_for_cell(*neighbor)
            if (len(neighbors & board)) == 3:
                new_board.add(neighbor)
    return new_board


def play_game(canvas, width, board):
    canvas.delete('all')
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    smallest_dimension = w if w < h else h
    for cell in board:
        x, y = cell
        scale = smallest_dimension // width
        x1, y1 = x*scale, y*scale
        canvas.create_rectangle(x1, y1, x1+scale, y1+scale, fill='grey')
    board = step(board)
    canvas.timeout_id = canvas.after(250, play_game, canvas, width, board)


def main():
    root = tk.Tk()
    root.title("Conway's game of life by Carl Bordum Hansen")
    button_frame = tk.Frame(root)
    canvas = tk.Canvas(root)
    canvas.timeout_id = 1
    for title, width, start_set in buttons:
        def callback(width, start_set):
            canvas.after_cancel(canvas.timeout_id)
            play_game(canvas, width, start_set)
        button = tk.Button(button_frame, text=title,
                command=partial(callback, width, start_set))
        button.pack(side='top', fill='both', expand=True)
    button_frame.pack(side='left', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
