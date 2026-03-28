import copy

BOARD_SIZE = 8
EMPTY_CELL = "_"
MOVE_MARK = "X"
CHESS_PIECES = "prnbqkcgz"
WHITE_CHESS_PIECES = CHESS_PIECES.upper()
BLACK_CHESS_PIECES = CHESS_PIECES
FILES_TO_COL = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

mode = input("Выберите режим: chess / checkers: ").strip().lower()

player = "w"
big_list = []

board = [
    ["z", "g", "c", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "C", "G", "Z"],
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
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == MOVE_MARK:
                board[i][j] = EMPTY_CELL
    return board


def choose_figure(player, board):
    if player == "w":
        figures = WHITE_CHESS_PIECES
        name = "белых"
    else:
        figures = BLACK_CHESS_PIECES
        name = "чёрных"

    a = input(f"Ход {name}. Введите координату фигуры (или 'back N' для отката): ")

    if a.lower().startswith("back"):
        return a.lower().split()

    a = a.lower()
    if (
        len(a) < 2
        or a[0] not in FILES_TO_COL.keys()
        or BOARD_SIZE - int(a[1]) not in range(0, BOARD_SIZE)
    ):
        print("Некорректный ввод")
        raise ValueError
    pos = [BOARD_SIZE - int(a[1]), FILES_TO_COL[a[0]]]
    if board[pos[0]][pos[1]] in figures:
        return pos
    else:
        print(f"На этой точке нет фигуры {name}")
        raise ValueError


def _is_on_board(row, col):
    return 0 <= row <= BOARD_SIZE - 1 and 0 <= col <= BOARD_SIZE - 1


class MoveFigures:
    def __init__(self, position, player, big_list):
        self.position = position
        self.player = player
        self.big_list = big_list

    def _resolve_board(self, board):
        if board is None:
            return self.big_list[-1]
        return board

    def _piece_sets(self):
        if self.player == "w":
            return WHITE_CHESS_PIECES, BLACK_CHESS_PIECES
        return BLACK_CHESS_PIECES, WHITE_CHESS_PIECES

    def _mark_jump_moves(self, board, moves):
        own, _ = self._piece_sets()
        for dr, dc in moves:
            row = self.position[0] + dr
            col = self.position[1] + dc
            if _is_on_board(row, col):
                if board[row][col] not in own:
                    board[row][col] = MOVE_MARK
        return board

    def camel(self, board=None):
        board = self._resolve_board(board)
        moves = [(3, 1), (3, -1), (-3, 1), (-3, -1), (1, 3), (1, -3), (-1, 3), (-1, -3)]
        return self._mark_jump_moves(board, moves)

    def zebra(self, board=None):
        board = self._resolve_board(board)
        moves = [(3, 2), (3, -2), (-3, 2), (-3, -2), (2, 3), (2, -3), (-2, 3), (-2, -3)]
        return self._mark_jump_moves(board, moves)

    def giraffe(self, board=None):
        board = self._resolve_board(board)
        moves = [(4, 1), (4, -1), (-4, 1), (-4, -1), (1, 4), (1, -4), (-1, 4), (-1, -4)]
        return self._mark_jump_moves(board, moves)

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
                and board[self.position[0] - 1][self.position[1] - 1] in "prnbqkcgz"
            ):
                board[self.position[0] - 1][self.position[1] - 1] = "X"
            elif (
                self.position[1] + 1 <= 7
                and board[self.position[0] - 1][self.position[1] + 1] in "prnbqkcgz"
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
                and board[self.position[0] + 1][self.position[1] - 1] in "prnbqkcgz".upper()
            ):
                board[self.position[0] + 1][self.position[1] - 1] = "X"
            elif (
                self.position[1] + 1 <= 7
                and board[self.position[0] + 1][self.position[1] + 1] in "prnbqkcgz".upper()
            ):
                board[self.position[0] + 1][self.position[1] + 1] = "X"
        return board

    def rook(self, board=None):  # ладья
        board = self._resolve_board(board)
        if self.player == "w":
            own = WHITE_CHESS_PIECES
            kill = BLACK_CHESS_PIECES
        elif self.player == "b":
            own = BLACK_CHESS_PIECES
            kill = WHITE_CHESS_PIECES

        for i in range(1, BOARD_SIZE):
            if self.position[0] - i >= 0:
                if board[self.position[0] - i][self.position[1]] == EMPTY_CELL:
                    board[self.position[0] - i][self.position[1]] = MOVE_MARK
                elif board[self.position[0] - i][self.position[1]] in kill:
                    board[self.position[0] - i][self.position[1]] = MOVE_MARK
                    break
                elif board[self.position[0] - i][self.position[1]] in own:
                    break
            else:
                break

        for i in range(1, BOARD_SIZE):
            if self.position[0] + i <= BOARD_SIZE - 1:
                if board[self.position[0] + i][self.position[1]] == EMPTY_CELL:
                    board[self.position[0] + i][self.position[1]] = MOVE_MARK
                elif board[self.position[0] + i][self.position[1]] in kill:
                    board[self.position[0] + i][self.position[1]] = MOVE_MARK
                    break
                elif board[self.position[0] + i][self.position[1]] in own:
                    break
            else:
                break

        for i in range(1, BOARD_SIZE):
            if self.position[1] - i >= 0:
                if board[self.position[0]][self.position[1] - i] == EMPTY_CELL:
                    board[self.position[0]][self.position[1] - i] = MOVE_MARK
                elif board[self.position[0]][self.position[1] - i] in kill:
                    board[self.position[0]][self.position[1] - i] = MOVE_MARK
                    break
                elif board[self.position[0]][self.position[1] - i] in own:
                    break
            else:
                break

        for i in range(1, BOARD_SIZE):
            if self.position[1] + i <= BOARD_SIZE - 1:
                if board[self.position[0]][self.position[1] + i] == EMPTY_CELL:
                    board[self.position[0]][self.position[1] + i] = MOVE_MARK
                elif board[self.position[0]][self.position[1] + i] in kill:
                    board[self.position[0]][self.position[1] + i] = MOVE_MARK
                    break
                elif board[self.position[0]][self.position[1] + i] in own:
                    break
            else:
                break
        return board

    def bishop(self, board=None):  # слон
        board = self._resolve_board(board)
        if self.player == "w":
            own = WHITE_CHESS_PIECES
            kill = BLACK_CHESS_PIECES
        elif self.player == "b":
            own = BLACK_CHESS_PIECES
            kill = WHITE_CHESS_PIECES
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in directions:
            for i in range(1, BOARD_SIZE):
                r, c = self.position[0] + d[0] * i, self.position[1] + d[1] * i
                if _is_on_board(r, c):
                    if board[r][c] == EMPTY_CELL:
                        board[r][c] = MOVE_MARK
                    elif board[r][c] in kill:
                        board[r][c] = MOVE_MARK
                        break
                    elif board[r][c] in own:
                        break
                else:
                    break
        return board

    def knight(self, board=None):  # конь
        board = self._resolve_board(board)
        moves = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        if self.player == "w":
            own = WHITE_CHESS_PIECES
        elif self.player == "b":
            own = BLACK_CHESS_PIECES
        for dr, dc in moves:
            row = self.position[0] + dr
            col = self.position[1] + dc
            if _is_on_board(row, col):
                if board[row][col] not in own:
                    board[row][col] = MOVE_MARK
        return board

    def queen(self, board=None):  # королева
        board = self._resolve_board(board)
        return self.bishop(self.rook(board))

    def king(self, board=None):  # король
        board = self._resolve_board(board)

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._mark_jump_moves(board, moves)

    def shah(self, board=None):
        board = self._resolve_board(board)

        if self.player == "w":
            target_king = "K"
            kill_color = "b"
            kill_pieces = BLACK_CHESS_PIECES
        else:
            target_king = "k"
            kill_color = "w"
            kill_pieces = WHITE_CHESS_PIECES

        king_pos = None
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == target_king:
                    king_pos = (i, j)
                    break

        if not king_pos:
            return 1

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece = board[i][j]
                if piece in kill_pieces:
                    temp_board = [row[:] for row in board]
                    attacker = MoveFigures([i, j], kill_color, [temp_board])
                    attack_board = get_moves_board_for_piece(attacker, piece, temp_board)

                    if attack_board[king_pos[0]][king_pos[1]] == MOVE_MARK:
                        return 1
        return 0


def get_moves_board_for_piece(mover, piece, board):
    method_by_piece = {
        "p": mover.pawn,
        "r": mover.rook,
        "n": mover.knight,
        "b": mover.bishop,
        "q": mover.queen,
        "k": mover.king,
        "z": mover.zebra,
        "c": mover.camel,
        "g": mover.giraffe,
    }
    move_method = method_by_piece.get(piece.lower())
    if move_method is None:
        return []
    return move_method(board)


def step(big_list, cross_board, pos):
    a = input("Введите координату, на которую хотите сходить: ")
    a = a.lower()
    if (
        len(a) < 2
        or a[0] not in FILES_TO_COL.keys()
        or BOARD_SIZE - int(a[1]) not in range(0, BOARD_SIZE)
    ):
        print("Выбранная фигура не может походить в эту клетку")
        raise ValueError
    new_pos = [BOARD_SIZE - int(a[1]), FILES_TO_COL[a[0]]]

    if cross_board[new_pos[0]][new_pos[1]] == MOVE_MARK:
        new_board = copy.deepcopy(big_list[-1])
        new_board[new_pos[0]][new_pos[1]] = cross_board[pos[0]][pos[1]]
        new_board[pos[0]][pos[1]] = EMPTY_CELL
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
    my_figure = WHITE_CHESS_PIECES if player == "w" else BLACK_CHESS_PIECES

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if current_board[i][j] in my_figure:
                temp_board_for_moves = clean_board(copy.deepcopy(current_board))
                mover = MoveFigures([i, j], player, [temp_board_for_moves])
                moves_board = get_moves_board_for_piece(
                    mover, current_board[i][j], temp_board_for_moves
                )

                for r in range(BOARD_SIZE):
                    for c in range(BOARD_SIZE):
                        if moves_board[r][c] == MOVE_MARK:
                            simulated_board = copy.deepcopy(current_board)
                            simulated_board[r][c] = simulated_board[i][j]
                            simulated_board[i][j] = EMPTY_CELL
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

# шашки
def create_checkers_board():
    board = [[EMPTY_CELL] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    for i in range(3):
        for j in range(BOARD_SIZE):
            if (i + j) % 2 == 1:
                board[i][j] = "b"

    for i in range(BOARD_SIZE - 3, BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (i + j) % 2 == 1:
                board[i][j] = "w"

    return board


def choose_checker(player, board):
    if player == "w":
        figures = "w"
    else:
        figures = "b"

    a = input("Введите координату шашки: ")
    a = a.lower()

    pos = [BOARD_SIZE - int(a[1]), FILES_TO_COL[a[0]]]

    if board[pos[0]][pos[1]] in figures:
        return pos
    else:
        raise ValueError


def _get_checkers_enemy(player):
    if player == "w":
        return "bB"
    return "wW"


def checkers_moves(pos, player, board):
    i, j = pos

    piece = board[i][j]

    if piece == "w":
        directions = [(-1, -1), (-1, 1)]
    elif piece == "b":
        directions = [(1, -1), (1, 1)]
    else:  # дамка
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    enemy = _get_checkers_enemy(player)

    can_capture = False

    # проверка рубки
    for dr, dc in directions:
        r1 = i + dr
        c1 = j + dc
        r2 = i + 2 * dr
        c2 = j + 2 * dc

        if _is_on_board(r2, c2):
            if board[r1][c1] in enemy and board[r2][c2] == EMPTY_CELL:
                board[r2][c2] = MOVE_MARK
                can_capture = True

    # если есть рубка — обычные ходы запрещены
    if can_capture:
        return board

    # обычные ходы
    for dr, dc in directions:
        r = i + dr
        c = j + dc
        if _is_on_board(r, c):
            if board[r][c] == EMPTY_CELL:
                board[r][c] = MOVE_MARK

    return board

def has_capture_from(pos, player, board):
    i, j = pos
    piece = board[i][j]

    if piece == "w":
        directions = [(-1, -1), (-1, 1)]
    elif piece == "b":
        directions = [(1, -1), (1, 1)]
    else:  # дамка
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    enemy = _get_checkers_enemy(player)

    for dr, dc in directions:
        r1 = i + dr
        c1 = j + dc
        r2 = i + 2 * dr
        c2 = j + 2 * dc

        if _is_on_board(r2, c2):
            if board[r1][c1] in enemy and board[r2][c2] == EMPTY_CELL:
                return True

    return False


if mode == "chess":
    player_1 = "w"
    player_2 = "b"
    player = player_1
    draw(board)
    while True:
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
            cross_board = get_moves_board_for_piece(
                move, piece_char, copy.deepcopy(big_list[-1])
            )

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


else:
    board = create_checkers_board()
    big_list = [board]
    player = "w"

    draw(board)

    while True:
        try:
            pos = choose_checker(player, big_list[-1])

            temp = clean_board(copy.deepcopy(big_list[-1]))
            temp = checkers_moves(pos, player, temp)

            draw(temp)

            # ход
            a = input("Куда ходить: ").lower()
            d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
            new_pos = [8 - int(a[1]), d[a[0]]]


            if temp[new_pos[0]][new_pos[1]] == "X":
                new_board = copy.deepcopy(big_list[-1])

                dr = new_pos[0] - pos[0]
                dc = new_pos[1] - pos[1]

                # если это рубка
                if abs(dr) == 2:
                    mid_r = (pos[0] + new_pos[0]) // 2
                    mid_c = (pos[1] + new_pos[1]) // 2
                    new_board[mid_r][mid_c] = "_"

                new_board[new_pos[0]][new_pos[1]] = new_board[pos[0]][pos[1]]
                new_board[pos[0]][pos[1]] = "_"
                big_list.append(new_board)

                draw(new_board)

                # проверяем цепную рубку
                if abs(new_pos[0] - pos[0]) == 2:
                    if has_capture_from(new_pos, player, new_board):
                        print("Продолжайте рубку этой же фигурой!")

                        # остаёмся тем же игроком
                        big_list[-1] = new_board
                        draw(new_board)

                        # новая позиция становится текущей
                        pos = new_pos

                        while True:
                            temp = clean_board(copy.deepcopy(new_board))
                            temp = checkers_moves(pos, player, temp)
                            draw(temp)

                            try:
                                a = input("Продолжите рубку: ").lower()
                                d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
                                next_pos = [8 - int(a[1]), d[a[0]]]

                                if temp[next_pos[0]][next_pos[1]] == "X":
                                    dr = next_pos[0] - pos[0]
                                    dc = next_pos[1] - pos[1]

                                    if abs(dr) == 2:
                                        mid_r = (pos[0] + next_pos[0]) // 2
                                        mid_c = (pos[1] + next_pos[1]) // 2
                                        new_board[mid_r][mid_c] = "_"

                                    new_board[next_pos[0]][next_pos[1]] = new_board[pos[0]][pos[1]]
                                    new_board[pos[0]][pos[1]] = "_"

                                    pos = next_pos
                                    draw(new_board)

                                    if not has_capture_from(pos, player, new_board):
                                        break
                                else:
                                    print("Нельзя так ходить")
                            except:
                                continue

                # только после завершения всей цепочки
                player = "b" if player == "w" else "w"
            else:
                print("Нельзя ходить")

            piece = new_board[new_pos[0]][new_pos[1]]

            if piece == "w" and new_pos[0] == 0:
                new_board[new_pos[0]][new_pos[1]] = "W"

            if piece == "b" and new_pos[0] == 7:
                new_board[new_pos[0]][new_pos[1]] = "B"

        except:
            continue
