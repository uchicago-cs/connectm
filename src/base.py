"""
Base class for Connect-M
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

PieceColor = Enum("PieceColor", ["RED", "YELLOW"])
"""
Enum type for representing piece colors.
"""


class ConnectMBase(ABC):
    """
    Class for representing a Connect-M board
    """

    #
    # PRIVATE ATTRIBUTES
    #

    # Number of rows and columns
    _nrows: int
    _ncols: int

    # Number of contiguous pieces needed to win
    _m: int


    #
    # PUBLIC METHODS
    #

    def __init__(self, nrows: int, ncols: int, m: int):
        """
        Constructor

        Args:
            nrows (int): Number of rows
            ncols (int): Number of columns
            m (int): Number of contiguous pieces needed to win
        """
        if nrows < m:
            raise ValueError(f"Number of rows ({nrows}) must be at least M ({m}")

        if ncols < m:
            raise ValueError(f"Number of columns ({ncols}) must be at least M ({m}")

        self._nrows = nrows
        self._ncols = ncols
        self._m = m

    @abstractmethod
    def __str__(self) -> str:
        """ Returns a string representation of the board """
        raise NotImplementedError

    @abstractmethod
    def can_drop(self, col: int) -> bool:
        """ Checks if a piece can be dropped into a column

        Args:
            col (int): Column index

        Raises:
            ValueError: if col is not a valid column index

        Returns:
            bool: True if a piece can be dropped in the
            specified column. False otherwise.

        """
        raise NotImplementedError

    @abstractmethod
    def drop_wins(self, col: int, color: PieceColor) -> bool:
        """ Checks whether dropping a piece in this
        column will result in a win.

        Args:
            col: Column index
            color: Color of the piece to drop

        Raises:
            ValueError: if col is not a valid column index,
            or if the column is already full.

        Returns:
            bool: True if dropping a piece of the given
            color would result in a win; False otherwise.

        """
        raise NotImplementedError

    @abstractmethod
    def drop(self, col: int, color: PieceColor) -> None:
        """ Drops a piece in a column

        Args:
            col: Column index
            color: Color of the piece to drop

        Raises:
            ValueError: if col is not a valid column index,
            or if the column is already full.

        Returns: None

        """

        # After dropping the piece, we would use _winner_at
        # to check whether adding that piece results in a
        # winning row/column/diagonal. If there is a winner
        # we update the _winner attribute.
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """ Resets the board (removes all pieces)

        Args: None

        Returns: None

        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """ Checks whether the game is done

        A game can be done either because there is a winner,
        or because no more pieces can be dropped

        Args: None

        Returns:
            bool: True if the game is done. False otherwise.

        """
        raise NotImplementedError

    @property
    @abstractmethod
    def winner(self) -> Optional[PieceColor]:
        """ Returns the winner (if any) in the board

        Returns:
            Optional[PieceColor]: If there is a winner,
            return its color. Otherwise, return None.

        """
        # Only needs to return the value of _winner
        # (does not check for a winner in every cell
        # of the board)
        raise NotImplementedError

    @property
    def num_cols(self) -> int:
        """ Returns the number of columns in the board"""
        return self._ncols

    @property
    def num_rows(self) -> int:
        """ Returns the number of rows in the board"""
        return self._nrows

    @property
    def m(self) -> int:
        """ Returns the number of contiguous pieces
            needed to win"""
        return self._m

    @property
    @abstractmethod
    def grid(self) -> list[list[Optional[PieceColor]]]:
        """ Returns the board as a list of list of PieceColors

        Returns:
            list[list[PieceColor]]: A list of lists with the same
            dimensions as the board. In each row, the values
            in the list will be None (no piece), PieceColor.RED
            (red piece), or PieceColor.YELLOW (yellow piece)
        """
        raise NotImplementedError
