from piece import Piece
from piece_factory import PieceFactory
from constants import BLACK, WHITE
from chess.moves import ChessMove, ChessMoveSet


class ChessFactory(PieceFactory):
    "Concrete piece factory for setting up a checkers game"

    def create_piece(self, board, space):
        x = space.row
        y = space.col

        # set up pawns
        if x == 1:
            return Pawn(BLACK, board, space)
        if x == board.size - 2:
            return Pawn(WHITE, board, space)

        # set up special pieces black
        if x == 0:
            if y == 0 or y == board.size - 1:
                return Rook(BLACK, board, space)
            if y == 1 or y == board.size - 2:
                return Knight(BLACK, board, space)
            if y == 2 or y == board.size - 3:
                return Bishop(BLACK, board, space)
            if y == 3:
                return Queen(BLACK, board, space)
            if y == 4:
                return King(BLACK, board, space)

        # set up special pieces white
        elif x == board.size - 1:
            if y == 0 or y == board.size - 1:
                return Rook(WHITE, board, space)
            if y == 1 or y == board.size - 2:
                return Knight(WHITE, board, space)
            if y == 2 or y == board.size - 3:
                return Bishop(WHITE, board, space)
            if y == 3:
                return Queen(WHITE, board, space)
            if y == 4:
                return King(WHITE, board, space)
        return None


class Pawn(Piece):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♙"
            self._directions = ["ne", "nw", "n"]
        if self._side == BLACK:
            self._symbol = u"♟︎"
            self._directions = ["se", "sw", "s"]
        self._first_move = True

    def enumerate_moves(self):
        moves = ChessMoveSet()
        # add checks for double move forward at the start of the game, add checks for captures
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            if direction == 'n' or direction == 's':
                if one_step and one_step.is_free():
                    m = ChessMove(self._current_space, one_step)
                    moves.append(m)
                    if (self._side == WHITE and one_step.row == 0) or \
                            (self._side == BLACK and one_step.row == self._board.size - 1):
                        m.add_promotion()
                    elif self._first_move:
                        one_step = self._board.get_dir(one_step, direction)
                        if one_step and one_step.is_free():
                            m = ChessMove(self._current_space, one_step)
                            moves.append(m)
            else:
                if one_step and one_step.piece is not None and one_step.piece.side != self._side:
                    m = ChessMove(self._current_space, one_step, [one_step])
                    moves.append(m)
                    if (self._side == WHITE and one_step.row == 0) or \
                            (self._side == BLACK and one_step.row == self._board.size - 1):
                        m.add_promotion()
        return moves

    def promote(self):
        "Overrides promote to return a KingChecker in the same space for the same side"
        return Queen(self._side, self._board, self._current_space)



class Bishop(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♗"
            self._directions = ["ne", "nw"]
        if self._side == BLACK:
            self._symbol = u"♝"
            self._directions = ["se", "sw"]

    def enumerate_moves(self):
        moves = ChessMoveSet()
        # add checks for double move forward at the start of the game, add checks for captures
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            while(True):
                if one_step and one_step.is_free():
                    m = ChessMove(self._current_space, one_step)
                    moves.append(m)
                elif one_step and one_step.piece is not None and one_step.piece.side != self._side:
                    m = ChessMove(self._current_space, one_step, [one_step])
                    moves.append(m)
                    break
                elif one_step and one_step.piece is not None and one_step.piece.side == self._side:
                    break
                elif not one_step:
                    break
                one_step = self._board.get_dir(one_step, direction)
        return moves

class Queen(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♕"
        if self._side == BLACK:
            self._symbol = u"♛"
        self._directions = ["ne", "nw", "se", "sw", "n", "s", "e", "w"]

    def enumerate_moves(self):
        moves = ChessMoveSet()
        # add checks for double move forward at the start of the game, add checks for captures
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            while(True):
                if one_step and one_step.is_free():
                    m = ChessMove(self._current_space, one_step)
                    moves.append(m)
                elif one_step and one_step.piece is not None and one_step.piece.side != self._side:
                    m = ChessMove(self._current_space, one_step, [one_step])
                    moves.append(m)
                    break
                elif one_step and one_step.piece is not None and one_step.piece.side == self._side:
                    break
                elif not one_step:
                    break
                one_step = self._board.get_dir(one_step, direction)
        return moves


class King(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♔"
        if self._side == BLACK:
            self._symbol = u"♚"
        self._directions = ["ne", "nw", "se", "sw", "n", "s", "e", "w"]

    def enumerate_moves(self):
        moves = ChessMoveSet()
        # add checks for double move forward at the start of the game, add checks for captures
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            if one_step and one_step.is_free():
                m = ChessMove(self._current_space, one_step)
                moves.append(m)
            elif one_step and one_step.piece is not None and one_step.piece.side != self._side:
                m = ChessMove(self._current_space, one_step, [one_step])
                moves.append(m)
        return moves


class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♖"
        if self._side == BLACK:
            self._symbol = u"♜"
        self._directions = ["n", "s", "e", "w"]

    def enumerate_moves(self):
        moves = ChessMoveSet()
        # add checks for double move forward at the start of the game, add checks for captures
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            while(True):
                if one_step and one_step.is_free():
                    m = ChessMove(self._current_space, one_step)
                    moves.append(m)
                elif one_step and one_step.piece is not None and one_step.piece.side != self._side:
                    m = ChessMove(self._current_space, one_step, [one_step])
                    moves.append(m)
                    break
                elif one_step and one_step.piece is not None and one_step.piece.side == self._side:
                    break
                elif not one_step:
                    break
                one_step = self._board.get_dir(one_step, direction)
        return moves


class Knight(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♘"
        if self._side == BLACK:
            self._symbol = u"♞"
        self._directions = ["kne", "kse", "knw", "ksw", "ken", "kes", "kwn", "kws"]

    def enumerate_moves(self):
        moves = ChessMoveSet()
        # add checks for double move forward at the start of the game, add checks for captures
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            if one_step and one_step.is_free():
                m = ChessMove(self._current_space, one_step)
                moves.append(m)
            elif one_step and one_step.piece is not None and one_step.piece.side != self._side:
                m = ChessMove(self._current_space, one_step, [one_step])
                moves.append(m)
        return moves
