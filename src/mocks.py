"""
Stub and mock implementations of the ConnectMBase class
"""

from connectm import ConnectMBase, PieceColor
from typing import Optional, List
from copy import deepcopy


class ConnectMStub(ConnectMBase):
    """
    Stub implementation of the ConnectMBase class
    """

    _board: List[List[Optional[PieceColor]]]

    def __init__(self, nrows: int, ncols: int, m: int):
        super().__init__(nrows, ncols, m)
        self._board = [[None] * ncols for _ in range(nrows)]

    def __str__(self) -> str:
        return "BOARD"

    def can_drop(self, col: int) -> bool:
        return True

    def drop_wins(self, col: int, color: PieceColor) -> bool:
        return False

    def drop(self, col: int, color: PieceColor) -> None:
        pass

    def reset(self) -> None:
        pass

    @property
    def done(self) -> bool:
        return False

    @property
    def winner(self) -> Optional[PieceColor]:
        return None

    @property
    def grid(self) -> List[List[Optional[PieceColor]]]:
        return deepcopy(self._board)


class ConnectMMock(ConnectMBase):
    """
    Mock implementation of the ConnectMBase class

    Expected behaviours:
    - Stores the full board internally, but we only ever
      modify the bottom row of the board. i.e., we
      effectively have a 1-row board, even if we display
      a larger board.
    - Game ends after M moves. If M is even, Red wins;
      otherwise, Yellow wins.
    """

    _board: List[List[Optional[PieceColor]]]
    _nummoves: int

    def __init__(self, nrows: int, ncols: int, m: int):
        super().__init__(nrows, ncols, m)
        self._board = [[None] * ncols for _ in range(nrows)]
        self._nummoves = 0

    def __str__(self) -> str:
        lines = []
        for row in self._board:
            s = ""
            for p in row:
                if p is None:
                    s += "·"
                else:
                    s += p.name[0]
            lines.append(s)
            
        return "\n".join(lines)

    def can_drop(self, col: int) -> bool:
        return self._board[-1][col] is None

    def drop_wins(self, col: int, color: PieceColor) -> bool:
        # Check if the next move ends the game:
        if self._nummoves == self._m - 1:
            if self._m % 2 == 0:
                return color == PieceColor.RED
            else:
                return color == PieceColor.YELLOW

        return False

    def drop(self, col: int, color: PieceColor) -> None:
        self._board[-1][col] = color
        self._nummoves += 1

    def reset(self) -> None:
        self._board = [[None] * self._ncols for _ in range(self._nrows)]

    @property
    def done(self) -> bool:
        return self._nummoves == self._m

    @property
    def winner(self) -> Optional[PieceColor]:
        if self._nummoves == self._m:
            if self._m % 2 == 0:
                return PieceColor.RED
            else:
                return PieceColor.YELLOW
        else:
            return None

    @property
    def grid(self) -> List[List[Optional[PieceColor]]]:
        return deepcopy(self._board)


class ConnectMBotMock(ConnectMBase):
    """
    Mock implementation of the ConnectMBase class,
    specifically for testing the bots.

    Since the bots only care about whether a drop is
    possible, or whether it will result in a win for
    a player, we only mock up can_drop, drop_wins,
    and get_num_cols (and stub out the remaining
    methods).

    The mock will use two lists: one to specify
    whether a piece can be dropped in a given column,
    and another to specify whether a drop in a column
    will result in a win for a player. can_drop
    and drop_wins will just return whatever is in
    those lists.

    """

    _can_drop: List[bool]
    _drop_wins: List[Optional[PieceColor]]

    def __init__(self, nrows: int, ncols: int, m: int):
        super().__init__(nrows, ncols, m)
        self._can_drop = [True] * ncols
        self._drop_wins = [None] * ncols

    def __str__(self) -> str:
        return "BOARD"

    def can_drop(self, col: int) -> bool:
        if not 0 <= col < self._ncols:
            return False
        else:
            return self._can_drop[col]

    def drop_wins(self, col: int, color: PieceColor) -> bool:
        if not 0 <= col < self._ncols:
            return False
        else:
            return self._drop_wins[col] == color

    def drop(self, col: int, color: PieceColor) -> None:
        return None

    def reset(self) -> None:
        return None

    @property
    def done(self) -> bool:
        return False

    @property
    def winner(self) -> Optional[PieceColor]:
        return None

    @property
    def grid(self) -> List[List[Optional[PieceColor]]]:
        return []
