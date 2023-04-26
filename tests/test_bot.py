import random

from bot import RandomBot, SmartBot
from connectm import PieceColor
from mocks import ConnectMBotMock


def test_random_1():
    """
    Checks that the random bot returns a valid
    column number (when pieces can be dropped
    in any column)
    """
    board = ConnectMBotMock(6, 7, 4)
    bot = RandomBot(board, PieceColor.YELLOW, PieceColor.RED)

    col = bot.suggest_move()

    assert 0 <= col < 7


def test_random_2():
    """
    Checks that, if pieces can't be dropped in certain
    columns, we don't get back any of those columns.
    """
    board = ConnectMBotMock(6, 7, 4)
    bot = RandomBot(board, PieceColor.YELLOW, PieceColor.RED)

    board._can_drop = [True, True, False, True, False, True, True]

    # Do this multiple times to make sure we
    # generate enough random numbers
    random.seed("test_random_2")
    for _ in range(100):
        col = bot.suggest_move()
        assert col in (0, 1, 3, 5, 6)


def test_random_3():
    """
    Checks that, if pieces can only be dropped in a single
    column, we only get back that column
    """
    board = ConnectMBotMock(6, 7, 4)
    bot = RandomBot(board, PieceColor.YELLOW, PieceColor.RED)

    board._can_drop = [False, False, False, True, False, False, False]

    # Do this multiple times to make sure we
    # generate enough random numbers
    random.seed("test_random_3")
    for _ in range(100):
        col = bot.suggest_move()
        assert col == 3


def test_smart_1():
    """
    Checks that, if there is a winning move for the bot's
    color, it will take it.
    """
    board = ConnectMBotMock(6, 7, 4)
    bot = SmartBot(board, PieceColor.YELLOW, PieceColor.RED)

    board._drop_wins = [None, None, PieceColor.YELLOW,
                        None, PieceColor.RED, None, PieceColor.RED]

    col = bot.suggest_move()

    assert col == 2


def test_smart_2():
    """
    Checks that, if there is no winning move, but there is a
    blocking move, it will take it.
    """
    board = ConnectMBotMock(6, 7, 4)
    bot = SmartBot(board, PieceColor.YELLOW, PieceColor.RED)

    bot._drop_wins = [None, None, None, None, PieceColor.RED,
                      None, PieceColor.RED]

    col = bot.suggest_move()

    assert col in (4, 6)


def test_smart_3():
    """
    Checks that, if there is neither a winning move nor
    a blocking move, it returns columns you can drop pieces
    into.
    """
    board = ConnectMBotMock(6, 7, 4)
    bot = SmartBot(board, PieceColor.YELLOW, PieceColor.RED)

    board._can_drop = [True, True, False, True, False, True, True]

    # Do this multiple times to make sure we
    # generate enough random numbers
    random.seed("test_smart_3")
    for _ in range(100):
        col = bot.suggest_move()
        assert col in (0, 1, 3, 5, 6)
