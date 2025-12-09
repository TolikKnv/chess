import itertools
import copy

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

    a = input(f"Ход {name}. Введите координату фигуры (или 'back N' для отката): ")

    if a.lower().startswith("back"):
        return a.lower().split()

    a = a.lower()
    d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    if len(a) < 2 or a[0] not in d.keys() or 8 - int(a[1]) not in range(0, 8):
        print("Некорректный ввод")
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

    def pawn(self, board=None):  # пешка
        if board is None:
            board = self.big_list[-1]
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
            if (
                self.position[1] - 1 >= 0
                and board[self.position[0] - 1][self.position[1] - 1] in "prnbqk"
            ):
                board[self.position[0] - 1][self.position[1] - 1] = "X"
            elif (
                self.position[1] + 1 <= 7
                and board[self.position[0] - 1][self.position[1] + 1] in "prnbqk"
            ):
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
            if (
                self.position[1] - 1 >= 0
                and board[self.position[0] + 1][self.position[1] - 1] in "prnbq".upper()
            ):
                board[self.position[0] + 1][self.position[1] - 1] = "X"
            elif (
                self.position[1] + 1 <= 7
                and board[self.position[0] + 1][self.position[1] + 1] in "prnbq".upper()
            ):
                board[self.position[0] + 1][self.position[1] + 1] = "X"
        return board

    def rook(self, board=None):  # ладья
        if board is None:
            board = self.big_list[-1]
        if self.player == "w":
            own = "prnbqk".upper()
            kill = "prnbqk"
        elif self.player == "b":
            own = "prnbqk"
            kill = "prnbqk".upper()

        for i in range(1, 8):
            if self.position[0] - i >= 0:
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
            if self.position[0] + i <= 7:
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
            if self.position[1] - i >= 0:
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
            if self.position[1] + i <= 7:
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

    def bishop(self, board=None):  # слон
        if board is None:
            board = self.big_list[-1]

        if self.player == "w":
            own = "prnbqk".upper()
            kill = "prnbqk"
        elif self.player == "b":
            own = "prnbqk"
            kill = "prnbqk".upper()
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in directions:
            for i in range(1, 8):
                r, c = self.position[0] + d[0] * i, self.position[1] + d[1] * i
                if 0 <= r <= 7 and 0 <= c <= 7:
                    if board[r][c] == "_":
                        board[r][c] = "X"
                    elif board[r][c] in kill:
                        board[r][c] = "X"
                        break
                    elif board[r][c] in own:
                        break
                else:
                    break
        return board

    def knight(self, board=None):  # конь
        if board is None:
            board = self.big_list[-1]
        if self.player == "w":
            own = "prnbqk".upper()
        elif self.player == "b":
            own = "prnbqk"

        moves = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        for m in moves:
            r, c = self.position[0] + m[0], self.position[1] + m[1]
            if 0 <= r <= 7 and 0 <= c <= 7:
                if board[r][c] not in own:
                    board[r][c] = "X"
        return board

    def queen(self, board=None):  # королева
        if board is None:
            board = self.big_list[-1]
        return self.bishop(self.rook(board))

    def king(self, board=None):  # король
        if board is None:
            board = self.big_list[-1]
        if self.player == "w":
            own = "prnbqk".upper()
        else:
            own = "prnbqk"

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for m in moves:
            r, c = self.position[0] + m[0], self.position[1] + m[1]
            if 0 <= r <= 7 and 0 <= c <= 7:
                if board[r][c] not in own:
                    board[r][c] = "X"
        return board

    def shah(self, board=None):
        if board is None:
            board = self.big_list[-1]

        if self.player == "w":
            target_king = "K"
            enemy_color = "b"
            enemy_pieces = "prnbqk"
        else:
            target_king = "k"
            enemy_color = "w"
            enemy_pieces = "PRNBQK"

        king_pos = None
        for i in range(8):
            for j in range(8):
                if board[i][j] == target_king:
                    king_pos = (i, j)
                    break

        if not king_pos:
            return 1

        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece in enemy_pieces:
                    temp_board = [row[:] for row in board]
                    attacker = MoveFigures([i, j], enemy_color, [temp_board])

                    attack_board = []
                    if piece.lower() == "p":
                        attack_board = attacker.pawn(temp_board)
                    elif piece.lower() == "r":
                        attack_board = attacker.rook(temp_board)
                    elif piece.lower() == "n":
                        attack_board = attacker.knight(temp_board)
                    elif piece.lower() == "b":
                        attack_board = attacker.bishop(temp_board)
                    elif piece.lower() == "q":
                        attack_board = attacker.queen(temp_board)
                    elif piece.lower() == "k":
                        attack_board = attacker.king(temp_board)

                    if attack_board[king_pos[0]][king_pos[1]] == "X":
                        return 1
        return 0


def step(big_list, cross_board, pos):
    a = input("Введите координату, на которую хотите сходить: ")
    a = a.lower()
    d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    if len(a) < 2 or a[0] not in d.keys() or 8 - int(a[1]) not in range(0, 8):
        print("Выбранная фигура не может походить в эту клетку")
        raise ValueError
    new_pos = [8 - int(a[1]), d[a[0]]]

    if cross_board[new_pos[0]][new_pos[1]] == "X":
        new_board = copy.deepcopy(big_list[-1])
        new_board[new_pos[0]][new_pos[1]] = cross_board[pos[0]][pos[1]]
        new_board[pos[0]][pos[1]] = "_"
        big_list.append(new_board)
        return new_board
    else:
        print("Выбранная фигура не может походить в эту клетку")
        raise ValueError


def mat(player, big_list):
    dummy = MoveFigures([0, 0], player, big_list)
    if dummy.shah() == 0:
        return False

    print(f"ШАХ игроку {player}!")

    current_board = big_list[-1]
    my_figure = "PRNBQK" if player == "w" else "prnbqk"

    for i in range(8):
        for j in range(8):
            if current_board[i][j] in my_figure:
                temp_board_for_moves = clean_board(copy.deepcopy(current_board))
                mover = MoveFigures([i, j], player, [temp_board_for_moves])

                figure_type = current_board[i][j].lower()
                moves_board = []
                if figure_type == "p":
                    moves_board = mover.pawn(temp_board_for_moves)
                elif figure_type == "r":
                    moves_board = mover.rook(temp_board_for_moves)
                elif figure_type == "n":
                    moves_board = mover.knight(temp_board_for_moves)
                elif figure_type == "b":
                    moves_board = mover.bishop(temp_board_for_moves)
                elif figure_type == "q":
                    moves_board = mover.queen(temp_board_for_moves)
                elif figure_type == "k":
                    moves_board = mover.king(temp_board_for_moves)

                for r in range(8):
                    for c in range(8):
                        if moves_board[r][c] == "X":
                            simulated_board = copy.deepcopy(current_board)
                            simulated_board[r][c] = simulated_board[i][j]
                            simulated_board[i][j] = "_"
                            checker = MoveFigures([0, 0], player, [simulated_board])
                            if checker.shah(simulated_board) == 0:

                                return False

    return True


def back_move(big_list, n):
    if len(big_list) <= n:
        print("Нельзя откатиться так далеко! Сброс в начало.")
        big_list = [big_list[0]]
        return "w"

    for _ in range(n):
        big_list.pop()

    print(f"Откат на {n} ходов выполнен.")

    if len(big_list) % 2 != 0:
        return "w"
    else:
        return "b"



player_1 = "w"
player_2 = "b"
player = player_1
draw(board)
while True:
    if player == "w":
        figuers = "PRNBQK"
    else:
        figuers = "PRNBQK".lower()

    try:
        if mat(player, big_list):
            print(f"МАТ! Победил игрок {'ЧЕРНЫЕ' if player == 'w' else 'БЕЛЫЕ'}!")
            break

        big_list[-1] = clean_board(big_list[-1])


        result = choose_figure(player, big_list[-1])


        if (
            isinstance(result, list)
            and isinstance(result[0], str)
            and result[0] == "back"
        ):
            try:
                steps_back = int(result[1])
                player = back_move(big_list, steps_back)
                draw(big_list[-1])
                continue
            except (IndexError, ValueError):
                print("Введите корректное число ходов: back 1")
                continue

        pos = result

        move = MoveFigures(pos, player, big_list)
        piece_char = big_list[-1][pos[0]][pos[1]]

        cross_board = []
        if piece_char.lower() == "p":
            cross_board = move.pawn()
        elif piece_char.lower() == "r":
            cross_board = move.rook()
        elif piece_char.lower() == "n":
            cross_board = move.knight()
        elif piece_char.lower() == "b":
            cross_board = move.bishop()
        elif piece_char.lower() == "q":
            cross_board = move.queen()
        elif piece_char.lower() == "k":
            cross_board = move.king()

        draw(cross_board)

        new_board = step(big_list, cross_board, pos)


        check_self = MoveFigures([0, 0], player, big_list)
        if check_self.shah() == 1:
            print("Нельзя делать этот ход! Король под ударом.")
            big_list.pop()
            continue

        big_list[-1] = clean_board(big_list[-1])
        draw(big_list[-1])

        player = player_2 if player == player_1 else player_1

    except ValueError:
        continue
