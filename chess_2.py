import itertools
import copy

mode = input("Выберите режим: 1 - шахматы, 2 - шашки: ")

player = "w"
big_list = []

# ================= ШАХМАТНАЯ ДОСКА =================
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

# ===== ДОБАВЛЯЕМ НОВЫЕ ФИГУРЫ =====
board[4][1] = "C"
board[4][3] = "Z"
board[4][5] = "G"

board[3][2] = "c"
board[3][4] = "z"
board[3][6] = "g"

big_list.append(board)


def draw(board):
    print("   A B C D E F G H  ")
    print()
    for i in range(len(board)):
        print(f"{(i-8)*-1} ", *board[i], sep=" ", end=" ")
        print(f" {(i-8)*-1}")
    print()
    print("   A B C D E F G H  ")


def clean_board(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] == "X":
                board[i][j] = "_"
    return board


def choose_figure(player, board):
    figures = "PRNBQKCGZ" if player == "w" else "prnbqkcgz"

    a = input("Введите координату фигуры: ")
    a = a.lower()

    d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    pos = [8 - int(a[1]), d[a[0]]]

    if board[pos[0]][pos[1]] in figures:
        return pos
    else:
        raise ValueError


class MoveFigures:

    def __init__(self, position, player, big_list):
        self.position = position
        self.player = player
        self.big_list = big_list

    def knight(self, board=None):
        if board is None:
            board = self.big_list[-1]

        moves = [(-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2)]

        for dr, dc in moves:
            r = self.position[0] + dr
            c = self.position[1] + dc

            if 0 <= r <= 7 and 0 <= c <= 7:
                board[r][c] = "X"

        return board

    # ===== НОВЫЕ ФИГУРЫ =====

    def camel(self, board=None):
        if board is None:
            board = self.big_list[-1]

        moves = [(3,1),(3,-1),(-3,1),(-3,-1),(1,3),(1,-3),(-1,3),(-1,-3)]

        for dr, dc in moves:
            r = self.position[0] + dr
            c = self.position[1] + dc
            if 0 <= r <= 7 and 0 <= c <= 7:
                board[r][c] = "X"

        return board

    def zebra(self, board=None):
        if board is None:
            board = self.big_list[-1]

        moves = [(3,2),(3,-2),(-3,2),(-3,-2),(2,3),(2,-3),(-2,3),(-2,-3)]

        for dr, dc in moves:
            r = self.position[0] + dr
            c = self.position[1] + dc
            if 0 <= r <= 7 and 0 <= c <= 7:
                board[r][c] = "X"

        return board

    def giraffe(self, board=None):
        if board is None:
            board = self.big_list[-1]

        moves = [(4,1),(4,-1),(-4,1),(-4,-1),(1,4),(1,-4),(-1,4),(-1,-4)]

        for dr, dc in moves:
            r = self.position[0] + dr
            c = self.position[1] + dc
            if 0 <= r <= 7 and 0 <= c <= 7:
                board[r][c] = "X"

        return board


# ================= ШАШКИ =================

def create_checkers_board():
    board = [["_"] * 8 for _ in range(8)]

    for i in range(3):
        for j in range(8):
            if (i + j) % 2 == 1:
                board[i][j] = "b"

    for i in range(5, 8):
        for j in range(8):
            if (i + j) % 2 == 1:
                board[i][j] = "w"

    return board


def choose_checker(player, board):
    figures = "w" if player == "w" else "b"

    a = input("Введите координату шашки: ")
    a = a.lower()

    d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    pos = [8 - int(a[1]), d[a[0]]]

    if board[pos[0]][pos[1]] in figures:
        return pos
    else:
        raise ValueError


# ================= ЗАПУСК =================

if mode == "1":

    player = "w"
    draw(board)

    while True:
        try:
            pos = choose_figure(player, big_list[-1])
            move = MoveFigures(pos, player, big_list)

            piece = big_list[-1][pos[0]][pos[1]]

            if piece.lower() == "n":
                cross = move.knight()
            elif piece.lower() == "c":
                cross = move.camel()
            elif piece.lower() == "z":
                cross = move.zebra()
            elif piece.lower() == "g":
                cross = move.giraffe()
            else:
                continue

            draw(cross)

            player = "b" if player == "w" else "w"

        except:
            continue

else:

    board = create_checkers_board()
    big_list = [board]
    player = "w"

    draw(board)

    while True:
        try:
            pos = choose_checker(player, big_list[-1])
            print("Ход выполнен")

            player = "b" if player == "w" else "w"

        except:
            continue