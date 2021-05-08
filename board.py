"""
1 ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆
2 ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼
3 ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆
4 ◻ ◼ ◻ ◼ ◻ ◼ ◻ ◼
5 ◼ ◻ ◼ ◻ ◼ ◻ ◼ ◻
6 ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼
7 ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈
8 ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼
  a b c d e f g h
"""
# ⛀
# ⛁
# ⛂
# ⛃
# ⚆
# ⚇
# ⚈
# ⚉


from constants import ALPHABET


def convert_checker_coord(coord):
    col = coord[:1]
    row = coord[1:]
    col = ord(col) - 96
    row = int(row)
    return (row - 1, col - 1)


def convert_matrix_coord(coord):
    row, col = coord
    return chr(col + 96 + 1) + str(row + 1)


class Space:
    def __init__(self, row, col, p=None):
        # row and col are read only properties
        self._row = row
        self._col = col
        # _piece is read/write as "piece" property
        self._piece = p

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, p):
        self._piece = p

    def __repr__(self):
        return str(self)

    def __str__(self):
        "coordinates for this space in the format b5 where the letter corresponds to the row and the number to the column"
        return convert_matrix_coord((self._row, self._col))

    def draw(self) -> str:
        "Draw the symbol of the piece in this space or the appropriate square color if empty"
        if not self._piece:
            if abs(self._row - self._col) % 2 == 0:
                return u"◻"
            else:
                return u"◼"
        else:
            return str(self._piece)

    def is_free(self) -> bool:
        return self._piece is None

    def has_opponent(self, side) -> bool:
        if self._piece:
            return self._piece.side != side
        else:
            return False


class Board:
    def __init__(self, size, factory):
        """
        Args:
            size (int): number of rows and columns in the board
            factory (PieceFactory): concrete piece factory to set up the board for a particular game
        """
        self._board = [[Space(i, j) for j in range(size)] for i in range(size)]
        self._factory = factory

        # read only property
        self._size = size

    @property
    def size(self):
        return self._size

    def set_up(self):
        "Uses an abstract piece factory to set up all spaces in the board"
        for x in range(self._size):
            for y in range(self._size):
                p = self._factory.create_piece(self, self._board[x][y])
                self._board[x][y].piece = p

    def get_space(self, coord):
        "Gets the space in the board for the given coordinate such as b5 or a1"
        coord = convert_checker_coord(coord)
        return self._board[coord[0]][coord[1]]

    def __str__(self):
        "String for printing the spaces in the board with alphanumeric coordinates"
        output = ""
        for x in range(self._size):
            output += str(x + 1) + " "
            for y in range(self._size):
                output += (self._board[x][y]).draw() + " "

            output += "\n"
        output += "  "
        output += " ".join(ALPHABET[:self._size])
        return output

    def n(self, space):
        "Returns the space to the north of the given space there is one"
        if space.row > 0:
            return self._board[space.row - 1][space.col]
        else:
            None

    def e(self, space):
        "Returns the space to the east of the given space there is one"
        if space.col < self._size - 1:
            return self._board[space.row][space.col + 1]
        else:
            None

    def s(self, space):
        "Returns the space to the south of the given space there is one"
        if space.row < self._size - 1:
            return self._board[space.row + 1][space.col]
        else:
            None

    def w(self, space):
        "Returns the space to the west of the given space there is one"
        if space.col > 0:
            return self._board[space.row][space.col - 1]
        else:
            None

    def ne(self, space):
        "Returns the space to the northeast of the given space there is one"
        if space.col < self._size - 1 and space.row > 0:
            return self._board[space.row - 1][space.col + 1]
        else:
            None

    def se(self, space):
        "Returns the space to the southeast of the given space there is one"
        if space.row < self._size - 1 and space.col < self._size - 1:
            return self._board[space.row + 1][space.col + 1]
        else:
            None

    def sw(self, space):
        "Returns the space to the southwest of the given space there is one"
        if space.row < self._size - 1 and space.col > 0:
            return self._board[space.row + 1][space.col - 1]
        else:
            None

    def nw(self, space):
        "Returns the space to the northwest of the given space there is one"
        if space.col > 0 and space.row > 0:
            return self._board[space.row - 1][space.col - 1]
        else:
            None

    def get_dir(self, space, dir) -> Space:
        """Takes in a space and a direction and delegates to the proper directional method

        Args:
            space (Space): origin space
            dir (string): Either "n", "e", "s", "w", "ne", "se", "sw", or "nw"

        Returns:
            Space: the space in the given direction from the origin space or None if that space is off the board
        """
        return getattr(self, dir)(space)

    def pieces_iterator(self, side=None):
        "Iterator over pieces for the given side, or all pieces if side is omitted or None"
        for space in self:
            if space.piece:
                if side == None or space.piece.side == side:
                    yield space.piece

    def __iter__(self):
        "Iterator over all spaces in the board"
        for x in range(self._size):
            for y in range(self._size):
                yield self._board[x][y]
