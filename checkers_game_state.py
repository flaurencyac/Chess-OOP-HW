from game_state import GameState
from checkers.moves import CheckersMoveSet
from constants import BLACK, WHITE


class CheckersGameState(GameState):

    def all_possible_moves(self, side=None):
        if not side:
            side = self._current_side
        pieces = self._board.pieces_iterator(side)
        # uses CheckersMoveSet to enforce restriction on basic moves when at least once piece has a jump
        options = CheckersMoveSet()
        for piece in pieces:
            options.extend(piece.enumerate_moves())

        return options

    def check_loss(self, side=None):
        if not side:
            side = self._current_side
        # no more pieces
        return len(list(self._board.pieces_iterator(side))) == 0
