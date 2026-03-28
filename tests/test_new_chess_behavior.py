import ast
import copy
import unittest
from pathlib import Path
from unittest.mock import patch


def _load_symbols():
    module_path = Path(__file__).resolve().parents[1] / "new_chess.py"
    source = module_path.read_text(encoding="utf-8")
    parsed = ast.parse(source, filename=str(module_path))

    allowed_assign_names = {
        "BOARD_SIZE",
        "EMPTY_CELL",
        "MOVE_MARK",
        "CHESS_PIECES",
        "WHITE_CHESS_PIECES",
        "BLACK_CHESS_PIECES",
        "FILES_TO_COL",
    }
    kept_nodes = []
    for node in parsed.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
            kept_nodes.append(node)
            continue
        if isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in allowed_assign_names:
                    kept_nodes.append(node)

    reduced_module = ast.Module(body=kept_nodes, type_ignores=[])
    namespace = {}
    exec(compile(reduced_module, str(module_path), "exec"), namespace)
    return namespace


SYMBOLS = _load_symbols()
MoveFigures = SYMBOLS["MoveFigures"]
clean_board = SYMBOLS["clean_board"]
choose_figure = SYMBOLS["choose_figure"]
step = SYMBOLS["step"]
back_move = SYMBOLS["back_move"]
checkers_moves = SYMBOLS["checkers_moves"]
has_capture_from = SYMBOLS["has_capture_from"]
get_moves_board_for_piece = SYMBOLS["get_moves_board_for_piece"]


def _empty_board():
    return [["_"] * 8 for _ in range(8)]


class NewChessBehaviorTests(unittest.TestCase):
    def test_clean_board_replaces_only_marked_cells(self):
        board = _empty_board()
        board[1][1] = "X"
        board[2][2] = "P"

        result = clean_board(board)

        self.assertIs(result, board)
        self.assertEqual(result[1][1], "_")
        self.assertEqual(result[2][2], "P")

    def test_choose_figure_supports_back_command(self):
        board = _empty_board()
        with patch("builtins.input", return_value="Back 3"):
            result = choose_figure("w", board)
        self.assertEqual(result, ["back", "3"])

    def test_choose_figure_returns_position_for_own_piece(self):
        board = _empty_board()
        board[6][0] = "P"
        with patch("builtins.input", return_value="a2"):
            result = choose_figure("w", board)
        self.assertEqual(result, [6, 0])

    def test_step_applies_move_when_target_is_marked(self):
        current_board = _empty_board()
        current_board[6][0] = "P"
        history = [copy.deepcopy(current_board)]
        cross_board = copy.deepcopy(current_board)
        cross_board[5][0] = "X"

        with patch("builtins.input", return_value="a3"):
            new_board = step(history, cross_board, [6, 0])

        self.assertEqual(new_board[5][0], "P")
        self.assertEqual(new_board[6][0], "_")
        self.assertEqual(len(history), 2)

    def test_back_move_pops_history_when_n_is_valid(self):
        history = [1, 2, 3]

        current_player = back_move(history, 1)

        self.assertEqual(history, [1, 2])
        self.assertEqual(current_player, "b")

    def test_back_move_too_far_keeps_original_list_object_state(self):
        history = [1, 2]
        original_snapshot = history[:]

        current_player = back_move(history, 5)

        self.assertEqual(current_player, "w")
        self.assertEqual(history, original_snapshot)

    def test_white_pawn_marks_only_first_available_capture_diagonal(self):
        board = _empty_board()
        board[6][3] = "P"
        board[5][2] = "p"
        board[5][4] = "p"
        mover = MoveFigures([6, 3], "w", [board])

        result = mover.pawn(copy.deepcopy(board))

        self.assertEqual(result[5][3], "X")
        self.assertEqual(result[4][3], "X")
        self.assertEqual(result[5][2], "X")
        self.assertEqual(result[5][4], "p")

    def test_checkers_moves_prioritizes_capture_over_simple_moves(self):
        board = _empty_board()
        board[5][2] = "w"
        board[4][3] = "b"

        result = checkers_moves([5, 2], "w", copy.deepcopy(board))

        self.assertEqual(result[3][4], "X")
        self.assertEqual(result[4][1], "_")

    def test_checkers_moves_marks_simple_moves_when_no_capture(self):
        board = _empty_board()
        board[5][2] = "w"

        result = checkers_moves([5, 2], "w", copy.deepcopy(board))

        self.assertEqual(result[4][1], "X")
        self.assertEqual(result[4][3], "X")

    def test_has_capture_from_detects_available_capture(self):
        board = _empty_board()
        board[5][2] = "w"
        board[4][3] = "b"

        self.assertTrue(has_capture_from([5, 2], "w", board))

    def test_get_moves_board_for_piece_returns_empty_list_for_unknown_piece(self):
        board = _empty_board()
        mover = MoveFigures([0, 0], "w", [board])

        result = get_moves_board_for_piece(mover, "?", board)

        self.assertEqual(result, [])

    def test_shah_reports_check_for_line_attack(self):
        board = _empty_board()
        board[7][4] = "K"
        board[0][4] = "r"
        checker = MoveFigures([0, 0], "w", [board])

        result = checker.shah(board)

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
