"""
Bots for Connect-M

(and command for running simulations with bots)
"""
import random
from typing import Union

import click

from connectm import ConnectMBase, ConnectM, PieceColor


#
# BOTS
#

class RandomBot:
    """
    Simple Bot that just picks a move at random
    """

    _connectm: ConnectMBase
    _color: PieceColor
    _opponent_color: PieceColor

    def __init__(self, connectm: ConnectMBase, color: PieceColor,
                 opponent_color: PieceColor):
        """ Constructor

        Args:
            board: Board the bot will play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        self._connectm = connectm
        self._color = color
        self._opponent_color = opponent_color

    def suggest_move(self) -> int:
        """ Suggests a move

        Returns: None

        """
        possible_cols = []
        for col in range(self._connectm.num_cols):
            if self._connectm.can_drop(col):
                possible_cols.append(col)

        return random.choice(possible_cols)


class SmartBot:
    """
    Smart bot. Will do the following:

    - If there is a winning move, take it.
    - Otherwise, check if there is a move that will block
      the opponent from winning. If so, take it.
    - Otherwise, pick a column at random.
    """

    _connectm: ConnectMBase
    _color: PieceColor
    _opponent_color: PieceColor

    def __init__(self, connectm: ConnectMBase, color: PieceColor,
                 opponent_color: PieceColor):
        """ Constructor

        Args:
            board: Board the bot will play on
            color: Bot's color
            opponent_color: Opponent's color
        """

        self._connectm = connectm
        self._color = color
        self._opponent_color = opponent_color

    def suggest_move(self) -> int:
        """ Suggests a move

        Returns: None

        """

        opponent_win_moves = []
        nonwinning_moves = []

        for col in range(self._connectm.num_cols):
            if not self._connectm.can_drop(col):
                continue

            if self._connectm.drop_wins(col, self._color):
                # If dropping a piece in this column
                # wins us the game, then we make that
                # move
                return col
            elif self._connectm.drop_wins(col, self._opponent_color):
                # If our opponent would win the game
                # if they dropped a piece in this column,
                # we save that column. We don't immediately
                # suggest it because there could still be
                # a column that wins us the game, and we
                # would preference that over blocking out
                # opponent
                opponent_win_moves.append(col)
            else:
                # Otherwise, we mark this as a non-winning move
                nonwinning_moves.append(col)

        if len(opponent_win_moves) > 0:
            # If there is a column where our opponent would win
            # the game in the next move, we block that move.
            return opponent_win_moves[0]
        else:
            # Otherwise, we just choose between the non-winning
            # moves at random. We would have to apply further
            # heuristics (or explore the game tree) to decide
            # which of these moves actually increases our
            # probability of winning.
            return random.choice(nonwinning_moves)


#
# SIMULATION CODE
#
# This is not strictly required in the course project,
# but writing something like this may be useful to
# test your bot(s)
#

class BotPlayer:
    """
    Simple class to store information about a
    bot player in a simulation.

    """

    name: str
    bot: Union[RandomBot, SmartBot]
    color: PieceColor
    wins: int

    def __init__(self, name: str, connectm: ConnectMBase, color: PieceColor,
                 opponent_color: PieceColor):
        """ Constructor

        Args:
            name: Name of the bot
            board: Board to play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        self.name = name

        if self.name == "random":
            self.bot = RandomBot(connectm, color, opponent_color)
        elif self.name == "smart":
            self.bot = SmartBot(connectm, color, opponent_color)
        self.color = color
        self.wins = 0


def simulate(connectm: ConnectMBase, n: int, bots) -> None:
    """ Simulates multiple games between two bots

    Args:
        board: The board to play on
        n: The number of matches to play
        bots: Dictionary mapping piece colors to
            BotPlayer objects (the bots what will
            face off in each match)

    Returns: None

    """
    for _ in range(n):
        # Reset the board
        connectm.reset()

        # The starting player is Yellow
        current = bots[PieceColor.YELLOW]

        # While the game isn't over, make a move
        while not connectm.done:
            column = current.bot.suggest_move()
            connectm.drop(column, current.color)

            # Update the player
            if current.color == PieceColor.YELLOW:
                current = bots[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = bots[PieceColor.YELLOW]

        # If there is a winner, add one to that
        # bot's tally
        winner = connectm.winner
        if winner is not None:
            bots[winner].wins += 1


@click.command(name="connect4-bot")
@click.option('-n', '--num-games',  type=click.INT, default=10000)
@click.option('--player1',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option('--player2',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
def cmd(num_games, player1, player2):
    board = ConnectM(nrows=6, ncols=7, m=4)

    bot1 = BotPlayer(player1, board, PieceColor.YELLOW, PieceColor.RED)
    bot2 = BotPlayer(player2, board, PieceColor.RED, PieceColor.YELLOW)

    bots = {PieceColor.YELLOW: bot1, PieceColor.RED: bot2}

    simulate(board, num_games, bots)

    bot1_wins = bots[PieceColor.YELLOW].wins
    bot2_wins = bots[PieceColor.RED].wins
    ties = num_games - (bot1_wins + bot2_wins)

    print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
    print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")


if __name__ == "__main__":
    cmd()
