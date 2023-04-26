from typing import Dict, Tuple
from connectm import ConnectM, PieceColor

def validate_grid(connectm: ConnectM,
                  pieces: Dict[Tuple[int, int], PieceColor]):
    """
    Helper function that validates whether a ConnectM object
    has pieces in the expected positions.
    """
    nrows = connectm.num_rows
    ncols = connectm.num_cols

    grid = connectm.grid
    assert len(grid) == nrows
    assert all(len(row) == ncols for row in grid)

    for r in range(nrows):
        for c in range(ncols):
            expected = pieces.get((r,c))
            assert grid[r][c] == expected, \
                f"Expected ({r},{c}) to be {expected} but got {grid[r][c]} instead"


def sample_board() -> ConnectM:
    """
    Generates a 5x5 board with
    the following pieces::

         
        Y
       RY
      RYR
     YRYR
    YRRYY
    """

    connectm = ConnectM(5, 5, 4)

    connectm.drop(0, PieceColor.YELLOW)

    connectm.drop(1, PieceColor.RED)
    connectm.drop(1, PieceColor.YELLOW)

    connectm.drop(2, PieceColor.RED)
    connectm.drop(2, PieceColor.RED)
    connectm.drop(2, PieceColor.RED)

    connectm.drop(3, PieceColor.YELLOW)
    connectm.drop(3, PieceColor.YELLOW)
    connectm.drop(3, PieceColor.YELLOW)
    connectm.drop(3, PieceColor.RED)

    connectm.drop(4, PieceColor.YELLOW)
    connectm.drop(4, PieceColor.RED)
    connectm.drop(4, PieceColor.RED)
    connectm.drop(4, PieceColor.YELLOW)
    connectm.drop(4, PieceColor.YELLOW)

    return connectm

def test_create_1():
    """
    Tests creating a 6x7 board
    """
    connectm = ConnectM(6, 7, 4)
    validate_grid(connectm, {})
    assert not connectm.done
    assert connectm.winner is None

def test_create_2():
    """
    Tests creating a 20x20 board
    """
    connectm = ConnectM(20, 20, 4)
    validate_grid(connectm, {})
    assert not connectm.done
    assert connectm.winner is None

def test_can_drop_1():
    """
    Tests that we can drop a piece in every column
    of an empty board
    """
    connectm = ConnectM(6, 7, 4)

    for i in range(7):
        assert connectm.can_drop(i)

def test_can_drop_2():
    """
    Tests that we can drop a piece in every column
    of the sample board (except column 4, which is full)
    """
    connectm = sample_board()

    for i in range(4):
        assert connectm.can_drop(i)
    
    assert not connectm.can_drop(4)

def test_drop_wins_1():
    """
    Tests that dropping a piece in any of the columns in an
    empty board does not result in a win.
    """
    connectm = ConnectM(6, 7, 4)

    for i in range(7):
        assert not connectm.drop_wins(i, PieceColor.RED)
        assert not connectm.drop_wins(i, PieceColor.YELLOW)

def test_drop_wins_2():
    """
    Tests that dropping a piece in any of the columns in an
    empty board does not result in a win, except dropping
    a red piece in column 2, which result in a win.
    """
    connectm = sample_board()

    for i in (0, 1, 3, 4):
        assert not connectm.drop_wins(i, PieceColor.RED)
        assert not connectm.drop_wins(i, PieceColor.YELLOW)

    assert connectm.drop_wins(2, PieceColor.RED)
    assert not connectm.drop_wins(2, PieceColor.YELLOW)

def test_drop_1():
    """
    Tests that we can correctly drop a piece
    """
    connectm = ConnectM(6, 7, 4)

    connectm.drop(0, PieceColor.YELLOW)

    validate_grid(connectm, {(5,0): PieceColor.YELLOW})

def test_drop_2():
    """
    Tests that we can correctly drop two pieces
    (in two separate columns)
    """
    connectm = ConnectM(6, 7, 4)

    connectm.drop(0, PieceColor.YELLOW)
    connectm.drop(1, PieceColor.RED)

    validate_grid(connectm, {(5,0): PieceColor.YELLOW,
                             (5,1): PieceColor.RED})
    
def test_drop_3():
    """
    Tests that we can correctly drop two pieces
    (in the same column)
    """
    connectm = ConnectM(6, 7, 4)

    connectm.drop(0, PieceColor.YELLOW)
    connectm.drop(0, PieceColor.RED)

    validate_grid(connectm, {(5,0): PieceColor.YELLOW,
                             (4,0): PieceColor.RED})

def test_reset():
    """
    Tests that we can correctly reset the board
    (starting from the sample board)
    """
    connectm = sample_board()
    connectm.reset()
    validate_grid(connectm, {})

def test_win():
    """
    Tests that dropping a red piece in column 2
    results in a win.
    """
    connectm = sample_board()
    connectm.drop(2, PieceColor.RED)
    
    assert connectm.done
    assert connectm.winner == PieceColor.RED
