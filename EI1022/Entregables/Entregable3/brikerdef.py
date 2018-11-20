from typing import *
# ---------------------------------------------------------------------------------------------------------


class Move:
    Left = "L"
    Right = "R"
    Up = "U"
    Down = "D"

# ---------------------------------------------------------------------------------------------------------


class Pos2D:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def add_row(self, d) -> "Pos2D":
        return Pos2D(self.row + d, self.col)

    def add_col(self, d) -> "Pos2D":
        return Pos2D(self.row, self.col + d)

    def __eq__(self, other):
        if not isinstance(other, Pos2D): return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return "Pos2D({}, {})".format(self.row, self.col)


# ---------------------------------------------------------------------------------------------------------

class Level:
    def __init__(self, filename: str):
        self._mat = [line.strip() for line in open(filename).readlines()]
        self.rows = len(self._mat)
        self.cols = len(self._mat[0])
        self._sPos = Pos2D ([(r,c) if self._mat[r][c] == "S" else "" for r in range(self.rows) for c in range(self.cols)])
        self._tPos = Pos2D ([(r,c) if self._mat[r][c] == "T" else "" for r in range(self.rows) for c in range(self.cols)])

    def is_valid(self, pos: Pos2D) -> bool:
        # posiciones marcadas con '-'. Para todos los demás casos debe devolver True.
        r = pos.row
        c = pos.col
        if 0 <= r <= self.rows and 0 <= c <= self.cols:
            if self._mat[r][c] == "o" or self._mat[r][c] == self._sPos or self._mat[r][c] == self._tPos:
                return True
        return False

    def get_startpos(self) -> Pos2D:
        return self._sPos

    def get_targetpos(self) -> Pos2D:
        return self._tPos


# ---------------------------------------------------------------------------------------------------------

class Block:
    def __init__(self, b1: Pos2D, b2: Pos2D):
        assert isinstance(b1, Pos2D) and isinstance(b2, Pos2D)
        if b2.row < b1.row or (b2.row == b1.row and b2.col < b1.col):
            self._b1, self._b2 = b2, b1
        else:
            self._b1, self._b2 = b1, b2

    # -----------------------------------------------------------------------------
    # <BEGIN> Funciones para comparar correctamente objetos de tipo Block

    def __eq__(self, other):
        if not isinstance(other, Block): return False
        return self._b1 == other._b1 and self._b2 == other._b2

    # Necesario para poder meter objetos de tipo Block en colecciones
    def __hash__(self):
        return hash((self._b1, self._b2))

    # <END> Funciones para comparar correctamente objetos de tipo Block
    # -----------------------------------------------------------------------------

    def __repr__(self):
        return "Block({}, {})".format(self._b1, self._b2)

    def is_standing(self) -> bool:  # true si el bloque está de pie
        return self._b1.row == self._b2.row and self._b1.col == self._b2.col

    def is_standing_at_pos(self, pos: Pos2D) -> bool:
        # Devuelve true si el bloque está de pie en la posición indicada en el parámetro
        return self.is_standing() and self._b1.row == pos.row and self._b1.col == pos.col

    def is_lying_on_a_row(self) -> bool:  # true si el bloque está tumbado en una fila
        return self._b1.row == self._b2.row and self._b1.col != self._b2.col

    def is_lying_on_a_col(self) -> bool:  # true si el bloque está tumbado en una columna
        return self._b1.row != self._b2.row and self._b1.col == self._b2.col

    def valid_moves(self, is_valid_pos: Callable[[Pos2D], bool]) -> Iterable[Move]:

        moves = []
        # Si el bloque esta de pie
        if self.is_standing():
            if is_valid_pos(self._b1.add_col(1)) and is_valid_pos(self._b1.add_col(2)):
                moves.append(Move.Right)
            if is_valid_pos(self._b1.add_col(-1)) and is_valid_pos(self._b1.add_col(-2)):
                moves.append(Move.Left)
            if is_valid_pos(self._b1.add_row(1)) and is_valid_pos(self._b1.add_row(2)):
                moves.append(Move.Down)
            if is_valid_pos(self._b1.add_row(-1)) and is_valid_pos(self._b1.add_row(-2)):
                moves.append(Move.Up)

        # Si el bloque esta horizontal
        elif self.is_lying_on_a_row():
            if is_valid_pos(self._b1.add_col(2)):
                moves.append(Move.Right)
            if is_valid_pos(self._b1.add_col(-1)):
                moves.append(Move.Left)
            if is_valid_pos(self._b1.add_row(1)) and is_valid_pos(self._b2.add_row(1)):
                moves.append(Move.Down)
            if is_valid_pos(self._b1.add_row(-1)) and is_valid_pos(self._b2.add_row(-1)):
                moves.append(Move.Up)

        # Si el bloque esta vertical
        elif self.is_lying_on_a_col():
            if is_valid_pos(self._b1.add_col(1)) and is_valid_pos(self._b2.add_col(1)):
                moves.append(Move.Right)
            if is_valid_pos(self._b1.add_col(-1)) and is_valid_pos(self._b2.add_col(-1)):
                moves.append(Move.Left)
            if is_valid_pos(self._b1.add_row(2)):
                moves.append(Move.Down)
            if is_valid_pos(self._b1.add_row(-1)):
                moves.append(Move.Up)

        return moves

    def move(self, m: Move) -> "Block":
        # TODO: IMPLEMENTAR - Debe devolver un nuevo objeto 'Block', sin modificar el originaL
        # Si el bloque esta de pie
        if self.is_standing():
            if m == "R":
                block = Block(self._b1.add_col(1),  self._b2.add_col(2))
            elif m == "L":
                block = Block(self._b1.add_col(-2), self._b2.add_col(-1))
            elif m == "D":
                block = Block(self._b1.add_row(1), self._b2.add_row(2))
            else:
                block = Block(self._b1.add_row(-2), self._b2.add_row(-1))

        # Si el bloque esta horizontal
        elif self.is_lying_on_a_row():
            if m == "R":
                block = Block(self._b1.add_col(2), self._b2.add_col(1))
            elif m == "L":
                block = Block(self._b1.add_col(-1), self._b2.add_col(-2))
            elif m == "D":
                block = Block(self._b1.add_row(1), self._b2.add_row(1))
            else:
                block = Block(self._b1.add_row(-1), self._b2.add_row(-1))

        # Si el bloque esta vertical
        elif self.is_lying_on_a_col():
            if m == "R":
                block = Block(self._b1.add_col(1), self._b2.add_col(1))
            elif m == "L":
                block = Block(self._b1.add_col(-1), self._b2.add_col(-1))
            elif m == "D":
                block = Block(self._b1.add_row(2), self._b2.add_row(1))
            else:
                block = Block(self._b1.add_row(-1), self._b2.add_row(-2))

        return block



# ---------------------------------------------------------------------------------------------------------
