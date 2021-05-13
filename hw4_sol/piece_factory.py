class PieceFactory():
    "Interface for abstract piece factory"

    def create_piece(self, board, space):
        raise NotImplementedError()
