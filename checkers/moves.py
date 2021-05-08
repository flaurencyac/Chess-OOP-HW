from move import Move

class CheckersMove(Move):
    def __repr__(self):
        return str(self)

    def __str__(self):
        if not self.is_jump():
            return f"basic move: {self._start}->{self._end}"
        else:
            return f"jump move: {self._start}->{self._end}, capturing {self._captures}"

    def is_jump(self):
        return len(self._captures) > 0





class CheckersMoveSet(list):
    """
    An extension to a list meant to hold checkers moves. When using append this ensures that the list does not mix jumps and non-jumps.
    """

    def __init__(self):
        self.has_jump = False

    def append(self, move):
        if move.is_jump():
            if not self.has_jump:
                #this is the first jump so clear out any basic moves that might be here already
                self.has_jump = True
                self.clear()
            super().append(move)
           
        elif not self.has_jump:
            # only add basic moves if there are no jumps so far
            super().append(move)

    def extend(self, other):
        """
        Overrides extend to use this version of append
        """
        for m in other:
            self.append(m)

