"""
Classes (actually just one) for implementing Connect-M
(a general version of Connect-4).

Examples:

    1) Creating a board::

        board = ConnectMBoard(6, 7, 4)

    2) Dropping a piece::

        if board.can_drop(col):
            board.drop(col, PieceColor.RED)

    3) Checking for a winner::

        winner = board.get_winner()
        if winner == PieceColor.RED:
            print("Red wins!")
        elif winner == PieceColor.YELLOW:
            print("Yellow wins!")
        else:
            print("No winner")

"""

from enum import Enum
from typing import Optional, List


PieceColor = Enum("PieceColor", ["RED", "YELLOW"])
"""
Enum type for representing piece colors.
"""


class ConnectMBoard:
    """
    Class for representing a Connect-M board
    """

    #
    # PRIVATE ATTRIBUTES
    #

    # The board itself
    _board: List[List[Optional[PieceColor]]]

     # Number of rows and columns
    _nrows: int
    _ncols: int

    # Number of contiguous pieces needed to win
    _m: int

    # The winner (if any) on the board
    _winner: Optional[PieceColor]

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
        self._board = [[None] * ncols for _ in range(nrows)]
        self._top = [0] * ncols
        self._nrows = nrows
        self._ncols = ncols
        self._m = m
        self._winner = None

    def __str__(self) -> str:
        """ Returns a string representation of the board """
        raise NotImplementedError

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

    def reset(self) -> None:
        """ Resets the board (removes all pieces)

        Args: None

        Returns: None

        """
        raise NotImplementedError

    def is_done(self) -> bool:
        """ Checks whether the game is done

        A game can be done either because there is a winner,
        or because no more pieces can be dropped

        Args: None

        Returns:
            bool: True if the game is done. False otherwise.

        """
        raise NotImplementedError        

    def get_winner(self) -> Optional[PieceColor]:
        """ Returns the winner (if any) in the board

        Returns:
            Optional[PieceColor]: If there is a winner,
            return its color. Otherwise, return None.

        """
        # Only needs to return the value of _winner
        # (does not check for a winner in every cell
        # of the board)
        raise NotImplementedError

    def get_num_cols(self) -> int:
        """ Returns the number of columns in the board"""
        raise NotImplementedError

    def to_piece_grid(self) -> List[List[Optional[PieceColor]]]:
        """ Returns the board as a list of list of PieceColors

        Not suitable for JSON serialization, but can be useful
        to display the board in a GUI or TUI.

        Returns:
            list[list[PieceColor]]: A list of lists with the same
            dimensions as the board. In each row, the values
            in the list will be None (no piece), PieceColor.RED
            (red piece), or PieceColor.YELLOW (yellow piece)
        """
        raise NotImplementedError

    def to_str_grid(self) -> List[List[str]]:
        """ Returns the board as a list of list of strings

        The returned list is suitable for JSON serialization.

        Returns:
            list[list[str]]: A list of lists with the same
            dimensions as the board. In each row, the values
            in the list will be " " (no piece), "R" (red piece),
            or "Y" (yellow piece)
        """
        raise NotImplementedError

    #
    # PRIVATE METHODS
    #

    def _get(self, row: int, col: int) -> Optional[PieceColor]:
        """ Gets piece color (if any) at a given location.

        Rows are numbered from 0 starting at the bottom of the board.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            Optional[PieceColor]: If there is a piece in the provided
            location, returns the PieceColor object at that location.
            Otherwise, returns None. Also returns None if the (row, col)
            coordinates are not valid.
        """
        raise NotImplementedError

    def _set(self, row: int, col: int, color: Optional[PieceColor]) -> None:
        """ Sets piece color at a given location.

        Rows are numbered from 0 starting at the bottom of the board.

        Args:
            row (int): Row index
            col (int): Column index
            color (Optional[PieceColor]): Color to set the location to.
              Can also be None to clear the piece in that location.

        Raises:
            ValueError: If the provided location is not valid

        Returns: None
        """
        raise NotImplementedError

    def _winner_at(self, row: int, col: int) -> bool:
        """ Checks for a winner at a location

        Checks whether the specified location contains
        a winning row, column, or diagonal.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            bool: True if there is a winner at the specified
            location. False otherwise.
        """
        raise NotImplementedError
