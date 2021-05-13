from constants import BLACK, WHITE


class GameState():
    def __init__(self, board, side, players):
        
        self._players = players
        self._turn_counter = 1
        # read only properties
        self._current_side = side
        self._board = board
        # public property
        self._draw_counter = 0

    @property
    def current_side(self):
        return self._current_side

    @property
    def board(self):
        return self._board

    @property
    def draw_counter(self):
        return self._draw_counter

    @draw_counter.setter
    def draw_counter(self, c):
        self._draw_counter = c

    def next_turn(self):
        self._current_side = not self._current_side
        self._turn_counter += 1

    def prev_turn(self):
        self._current_side = not self._current_side
        self._turn_counter -= 1

    def __str__(self):
        if self._current_side == WHITE:
            side_string = "white"
        elif self._current_side == BLACK:
            side_string = "black"
        else:
            raise ValueError("Current player is neither black nor white")
        return f"{self._board}\nTurn: {self._turn_counter}, {side_string}"

    def all_possible_moves(self, side=None):
        """Iterates over a side's pieces and returns a list containing all legal moves

        Args:
            side ([type], optional): side for which moves should be retrieved. Defaults to the game state's current side.

        Returns:
            list: list of Move objects 
        """
        if not side:
            side = self._current_side
        pieces = self._board.pieces_iterator(side)
        options = []
        for piece in pieces:
            options.extend(piece.enumerate_moves())

        return options

    def check_draw(self, side=None):
        if not side:
            side = self._current_side
        # no moves available
        if len(self.all_possible_moves(side)) == 0:
            return True
        # 50 turn rule
        if self._draw_counter >= 50:
            return True
        # default to no draw
        return False

    def check_loss(self, side=None):
        # Specific rules for loss should be implemented per game
        raise NotImplementedError()
