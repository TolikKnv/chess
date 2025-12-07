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
                elif board[self.position[0] - 1][self.position[1] - 1] in "prnbq":
                    board[self.position[0] - 1][self.position[1] - 1] = "X"
                elif board[self.position[0] - 1][self.position[1] + 1] in "prnbq":
                    board[self.position[0] - 1][self.position[1] + 1] = "X"
                else:
                    break
        elif self.player == "b" and self.position[0] in range(1, 7):
            if self.position[0] == 1:
                n = 3
            else:
                n = 2
            for i in range(1, n):
                if board[self.position[0] + i][self.position[1]] == "_":
                    board[self.position[0] + i][self.position[1]] = "X"
                elif (
                    board[self.position[0] + 1][self.position[1] - 1] in "prnbq".upper()
                ):
                    board[self.position[0] + 1][self.position[1] - 1] = "X"
                elif (
                    board[self.position[0] + 1][self.position[1] + 1] in "prnbq".upper()
                ):
                    board[self.position[0] + 1][self.position[1] + 1] = "X"
                else:
                    break
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
            k = 'k'
        else:
            p = "p"
            r = "r"
            n = "n"
            b = "b"
            q = "q"
            k = 'K'
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
                break


# a = MoveFigures([7, 1], player, big_list)
# draw(a.knight())
