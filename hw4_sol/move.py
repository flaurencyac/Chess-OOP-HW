class Move:
    """
    Implements a command pattern for moves
    start and end must be space objects
    captures may be empty
    """

    def __init__(self, start, end, captures=None, promotion=False):
        self._start = start
        self._end = end
        if captures == None:
            self._captures = []
        else:
            self._captures = captures
        self._promotion = promotion
        self._promoted_piece = None
        self._captured_pieces = {}

    def __str__(self) -> str:
        return f"move: {self._start}->{self._end}"

    def __eq__(self, other) -> bool:
        return self._start == other._start and self._end == other._end and self._captures == other._captures

    def execute(self, game_state):
        "Interacts with the start end and capture Space objects to carry out this move command"

        # capture first so we don't overwrite the piece
        for cap in self._captures:
            self._captured_pieces[cap] = cap.piece
            cap.piece = None

        if not self._start is self._end:
            self._end.piece = self._start.piece  # move to new space
            self._start.piece = None             # clear old space
            self._end.piece.move(self._end)      # update piece object

        # promote piece
        if self._promotion:
            self._promoted_piece = self._end.piece
            self._end.piece = self._end.piece.promote()

        # advance turn and update draw counter
        game_state.next_turn()
        if self.num_captures() > 0:
            self._prev_draw_counter = game_state.draw_counter
            game_state.draw_counter = 0
        else:
            game_state.draw_counter += 1

    def undo(self, game_state):
        "Inverse operation of execute"

        # reverse turn and restore draw counter
        game_state.prev_turn()
        if self.num_captures() > 0:
            game_state.draw_counter = self._prev_draw_counter
        else:
            game_state.draw_counter -= 1

        # undo promotion
        if self._promoted_piece:
            self._end.piece = self._promoted_piece

        # undo move
        if not self._start is self._end:
            self._start.piece = self._end.piece
            self._end.piece = None
            self._start.piece.move(self._start)

        # undo captures
        for space, piece in self._captured_pieces.items():
            space.piece = piece

    def add_promotion(self):
        self._promotion = True

    def num_captures(self):
        return len(self._captures)
