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

    def pawn(self):  # пешка
        board = self.big_list[-1]
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

    def rook(self):  # ладья
        board = self.big_list[-1]
        for i in range(1, 8):
            if self.position[0] + i in range(0, 8) and (
                self.position[0] + i in range(0, 8)
                or board[self.position[0] + i][self.position[1]] != "_"
            ):
                board[self.position[0] + i][self.position[1]] = "X"
            elif self.position[0] - i in range(0, 8) and (
                self.position[0] - i in range(0, 8)
                or board[self.position[0] - i][self.position[1]] != "_"
            ):
                board[self.position[0] - i][self.position[1]] = "X"
            elif self.position[1] + i in range(0, 8) and (
                self.position[1] + i in range(0, 8)
                or board[self.position[0]][self.position[1] + i] != "_"
            ):
                board[self.position[0]][self.position[1] + i] = "X"
            elif self.position[1] - i in range(0,8) and (
                self.position[1] - i in range(0, 8)
                or board[self.position[0]][self.position[1] - i] != "_"
            ):
                board[self.position[0]][self.position[1] - i] = "X"
            elif self.player == "w":
                if self.position[0] + i in range(0,8) and board[self.position[0] + i][self.position[1]] in "prnbq":
                    board[self.position[0] + i][self.position[1]] = "X"
                elif self.position[0] - i in range(0,8) and board[self.position[0] - i][self.position[1]] in "prnbq":
                    board[self.position[0] - i][self.position[1]] = "X"
                elif self.position[1] + i in range(0,8) and board[self.position[0]][self.position[1] + i] in "prnbq":
                    board[self.position[0]][self.position[1] + i] = "X"
                elif self.position[1] - i in range(0,8) and board[self.position[0]][self.position[1] - i] in "prnbq":
                    board[self.position[0]][self.position[1] - i] = "X"
            elif self.player == "b":
                if self.position[0] + i in range(0,8) and board[self.position[0] + i][self.position[1]] in "prnbq".upper():
                    board[self.position[0] + i][self.position[1]] = "X"
                elif self.position[0] - i in range(0,8) and board[self.position[0] - i][self.position[1]] in "prnbq".upper():
                    board[self.position[0] - i][self.position[1]] = "X"
                elif self.position[1] + i in range(0,8) and board[self.position[0]][self.position[1] + i] in "prnbq".upper():
                    board[self.position[0]][self.position[1] + i] = "X"
                elif self.position[1] - i in range(0,8) and board[self.position[0]][self.position[1] - i] in "prnbq".upper():
                    board[self.position[0]][self.position[1] - i] = "X"
        return board

    def knight(self):  # конь
        pass

    def bishop(self):  # слон
        pass

    def queen(self):  # королева
        pass

    def king(self):  # король
        pass


a = MoveFigures([7, 0], player, big_list)
draw(a.rook())
