import itertools


player = "w"

big_list = []


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

big_list.append(board)


def draw(board):
    print("   A B C D E F G H  ")
    print()
    for i in range(len(board)):
        print(f"{(i-8)*-1} ", *board[i], sep=" ", end=" ")
        print(f" {(i-8)*-1}")
    print()
    print("   A B C D E F G H  ")


draw(board)


def clean_board(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] == "X":
                board[i][j] = "_"
    return board


def choose_figure(player, board):
    if player == "w":
        figures = "prnbqk".upper()
        name = "белых"
    else:
        figures = "prnbqk"
        name = "чёрных"
    a = input("Введите координату, где стоит фигура, которой вы хотите походить: ")
    a = a.lower()
    d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    if a[0] not in d.keys() or 8 - int(a[1]) not in range(0,8):
        print(f"На этой точке нет фигуры {name}")
        raise ValueError
    pos = [8 - int(a[1]), d[a[0]]]
    if board[pos[0]][pos[1]] in figures:
        return pos
    else:
        print(f"На этой точке нет фигуры {name}")
        raise ValueError





class MoveFigures:
    def __init__(self, position, player, big_list):
        self.position = position
        self.player = player
        self.big_list = big_list

    def pawn(self, board=big_list[-1]):  # пешка
        # board = self.big_list[-1]
        if self.player == "w" and self.position[0] in range(1, 7):
            if self.position[0] == 6:
                n = 3
            else:
                n = 2
            for i in range(1, n):
                if board[self.position[0] - i][self.position[1]] == "_":
                    board[self.position[0] - i][self.position[1]] = "X"
                else:
                    break
            if board[self.position[0] - 1][self.position[1] - 1] in "prnbqk":
                board[self.position[0] - 1][self.position[1] - 1] = "X"
            elif board[self.position[0] - 1][self.position[1] + 1] in "prnbqk":
                board[self.position[0] - 1][self.position[1] + 1] = "X"
        elif self.player == "b" and self.position[0] in range(1, 7):
            if self.position[0] == 1:
                n = 3
            else:
                n = 2
            for i in range(1, n):
                if board[self.position[0] + i][self.position[1]] == "_":
                    board[self.position[0] + i][self.position[1]] = "X"
                else:
                    break
            if board[self.position[0] + 1][self.position[1] - 1] in "prnbq".upper():
                board[self.position[0] + 1][self.position[1] - 1] = "X"
            elif board[self.position[0] + 1][self.position[1] + 1] in "prnbq".upper():
                board[self.position[0] + 1][self.position[1] + 1] = "X"
        return board

    def rook(self, board=big_list[-1]):  # ладья
        if self.player == "w":
            own = "prnbqk".upper()
            kill = "prnbqk"
        elif self.player == "b":
            own = "prnbqk"
            kill = "prnbqk".upper()
        for i in range(1, 8):
            if self.position[0] - i in range(0, 8):
                if board[self.position[0] - i][self.position[1]] == "_":
                    board[self.position[0] - i][self.position[1]] = "X"
                elif board[self.position[0] - i][self.position[1]] in kill:
                    board[self.position[0] - i][self.position[1]] = "X"
                    break
                elif board[self.position[0] - i][self.position[1]] in own:
                    break
            else:
                break
        for i in range(1, 8):
            if self.position[0] + i in range(0, 8):
                if board[self.position[0] + i][self.position[1]] == "_":
                    board[self.position[0] + i][self.position[1]] = "X"
                elif board[self.position[0] + i][self.position[1]] in kill:
                    board[self.position[0] + i][self.position[1]] = "X"
                    break
                elif board[self.position[0] + i][self.position[1]] in own:
                    break
            else:
                break
        for i in range(1, 8):
            if self.position[1] - i in range(0, 8):
                if board[self.position[0]][self.position[1] - i] == "_":
                    board[self.position[0]][self.position[1] - i] = "X"
                elif board[self.position[0]][self.position[1] - i] in kill:
                    board[self.position[0]][self.position[1] - i] = "X"
                    break
                elif board[self.position[0]][self.position[1] - i] in own:
                    break
            else:
                break
        for i in range(1, 8):
            if self.position[1] + i in range(0, 8):
                if board[self.position[0]][self.position[1] + i] == "_":
                    board[self.position[0]][self.position[1] + i] = "X"
                elif board[self.position[0]][self.position[1] + i] in kill:
                    board[self.position[0]][self.position[1] + i] = "X"
                    break
                elif board[self.position[0]][self.position[1] + i] in own:
                    break
            else:
                break
        return board

    def knight(self, board=big_list[-1]):  # конь
        if self.player == "w":
            own = "prnbqk".upper()
            kill = "prnbqk"
        elif self.player == "b":
            own = "prnbqk"
            kill = "prnbqk".upper()
        for _ in range(8):
            if (
                self.position[0] - 2 in range(0, 8)
                and self.position[1] - 1 in range(0, 8)
                and board[self.position[0] - 2][self.position[1] - 1] not in "X" + own
            ):
                board[self.position[0] - 2][self.position[1] - 1] = "X"
            elif (
                self.position[0] - 2 in range(0, 8)
                and self.position[1] + 1 in range(0, 8)
                and board[self.position[0] - 2][self.position[1] + 1] not in "X" + own
            ):
                board[self.position[0] - 2][self.position[1] + 1] = "X"
            elif (
                self.position[0] - 1 in range(0, 8)
                and self.position[1] + 2 in range(0, 8)
                and board[self.position[0] - 1][self.position[1] + 2] not in "X" + own
            ):
                board[self.position[0] - 1][self.position[1] + 2] = "X"
            elif (
                self.position[0] + 1 in range(0, 8)
                and self.position[1] + 2 in range(0, 8)
                and board[self.position[0] + 1][self.position[1] + 2] not in "X" + own
            ):
                board[self.position[0] + 1][self.position[1] + 2] = "X"
            elif (
                self.position[0] + 2 in range(0, 8)
                and self.position[1] + 1 in range(0, 8)
                and board[self.position[0] + 2][self.position[1] + 1] not in "X" + own
            ):
                board[self.position[0] + 2][self.position[1] + 1] = "X"
            elif (
                self.position[0] + 2 in range(0, 8)
                and self.position[1] - 1 in range(0, 8)
                and board[self.position[0] + 2][self.position[1] - 1] not in "X" + own
            ):
                board[self.position[0] + 2][self.position[1] - 1] = "X"
            elif (
                self.position[0] + 1 in range(0, 8)
                and self.position[1] - 2 in range(0, 8)
                and board[self.position[0] + 1][self.position[1] - 2] not in "X" + own
            ):
                board[self.position[0] + 1][self.position[1] - 2] = "X"
            elif (
                self.position[0] - 1 in range(0, 8)
                and self.position[1] - 2 in range(0, 8)
                and board[self.position[0] - 1][self.position[1] - 2] not in "X" + own
            ):
                board[self.position[0] - 1][self.position[1] - 2] = "X"
        return board

    def bishop(self, board=big_list[-1]):  # слон
        if self.player == "w":
            own = "prnbqk".upper()
            kill = "prnbqk"
        elif self.player == "b":
            own = "prnbqk"
            kill = "prnbqk".upper()
        for i in range(1, 8):
            if self.position[0] + i in range(0, 8) and self.position[1] + i in range(
                0, 8
            ):
                if board[self.position[0] + i][self.position[1] + i] == "_":
                    board[self.position[0] + i][self.position[1] + i] = "X"
                elif board[self.position[0] + i][self.position[1] + i] in kill:
                    board[self.position[0] + i][self.position[1] + i] = "X"
                    break
                elif board[self.position[0] + i][self.position[1] + i] in own:
                    break
            else:
                break
        for i in range(1, 8):
            if self.position[0] + i in range(0, 8) and self.position[1] - i in range(
                0, 8
            ):
                if board[self.position[0] + i][self.position[1] - i] == "_":
                    board[self.position[0] + i][self.position[1] - i] = "X"
                elif board[self.position[0] + i][self.position[1] - i] in kill:
                    board[self.position[0] + i][self.position[1] - i] = "X"
                    break
                elif board[self.position[0] + i][self.position[1] - i] in own:
                    break
            else:
                break
        for i in range(1, 8):
            if self.position[0] - i in range(0, 8) and self.position[1] + i in range(
                0, 8
            ):
                if board[self.position[0] - i][self.position[1] + i] == "_":
                    board[self.position[0] - i][self.position[1] + i] = "X"
                elif board[self.position[0] - i][self.position[1] + i] in kill:
                    board[self.position[0] - i][self.position[1] + i] = "X"
                    break
                elif board[self.position[0] - i][self.position[1] + i] in own:
                    break
            else:
                break
        for i in range(1, 8):
            if self.position[0] - i in range(0, 8) and self.position[1] - i in range(
                0, 8
            ):
                if board[self.position[0] - i][self.position[1] - i] == "_":
                    board[self.position[0] - i][self.position[1] - i] = "X"
                elif board[self.position[0] - i][self.position[1] - i] in kill:
                    board[self.position[0] - i][self.position[1] - i] = "X"
                    break
                elif board[self.position[0] - i][self.position[1] - i] in own:
                    break
            else:
                break
        return board

    def queen(self, board=big_list[-1]):  # королева
        return self.bishop(self.rook(board))

    def king(self):  # король
        if self.player == "w":
            own = "prnbqk".upper()
            kill = "prnbqk"
        elif self.player == "b":
            own = "prnbqk"
            kill = "prnbqk".upper()

    def shah(self, board=big_list[-1]):
        kill_board = []
        if player == "w":
            p = "P"
            r = "R"
            n = "N"
            b = "B"
            q = "Q"
            k = "k"
        else:
            p = "p"
            r = "r"
            n = "n"
            b = "b"
            q = "q"
            k = "K"
        for i in range(8):
            for j in range(8):
                if board[i][j] == p:
                    kill_board = self.pawn()
                    if k not in list(itertools.chain(*kill_board)):
                        print("шах")
                        flag = 1
                        break
                elif board[i][j] == r:
                    kill_board = self.pawn()
                    if k not in list(itertools.chain(*kill_board)):
                        print("шах")
                        flag = 1
                        break
                elif board[i][j] == n:
                    kill_board = self.pawn()
                    if k not in list(itertools.chain(*kill_board)):
                        print("шах")
                        flag = 1
                        break
                elif board[i][j] == b:
                    kill_board = self.pawn()
                    if k not in list(itertools.chain(*kill_board)):
                        print("шах")
                        flag = 1
                        break
                elif board[i][j] == q:
                    kill_board = self.pawn()
                    if k not in list(itertools.chain(*kill_board)):
                        print("шах")
                        flag = 1
                        break
            if flag == 1:
                return 1
            else:
                return 0

    # def mat(self, board=big_list[-1]):


# a = MoveFigures([6, 6], player, big_list)
# draw(a.pawn())


player_1 = 'w'
player_2 = 'b'
player = player_1


for _ in range(10):
    if player == 'w':
        figuers = 'PRNBQK'
    else:
        figuers = 'PRNBQK'.lower()
    try:
        big_list[-1] = clean_board(big_list[-1])
        pos = choose_figure(player, big_list[-1])
        move = MoveFigures(pos, player, big_list)
        if big_list[-1][pos[0]][pos[1]] == figuers[0]:
            cross_board = move.pawn()
        elif big_list[-1][pos[0]][pos[1]] == figuers[1]:
            cross_board = move.rook()
        elif big_list[-1][pos[0]][pos[1]] == figuers[2]:
            cross_board = move.knight()
        elif big_list[-1][pos[0]][pos[1]] == figuers[3]:
            cross_board = move.bishop()
        elif big_list[-1][pos[0]][pos[1]] == figuers[4]:
            cross_board = move.queen()
        elif big_list[-1][pos[0]][pos[1]] == figuers[5]:
            cross_board = move.king()
        draw(cross_board)
        big_list.append([row[:] for row in clean_board(cross_board)])
        player_1, player_2 = player_2, player_1
        player = player_1
    except ValueError:
        continue