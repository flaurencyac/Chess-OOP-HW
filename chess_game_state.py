from game_state import GameState
from checkers_moves import CheckersMoveSet
from constants import BLACK, WHITE
from chess_pieces import King


class ChessGameState(GameState):

    def all_possible_moves(self, side=None):
        if not side:
            side = self._current_side
        pieces = self._board.pieces_iterator(side)
        # uses CheckersMoveSet to enforce restriction on basic moves when at least once piece has a jump
        options = []
        for piece in pieces:
            options.extend(piece.enumerate_moves())

        return options
        pass

    def check_loss(self, side=None):
        if not side:
            side = self._current_side
        # no more pieces
        pieces_list = (list(self._board.pieces_iterator(side)))
        return not any(isinstance(x, King) for x in pieces_list)
