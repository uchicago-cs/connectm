"""
TUI for Connect Four
"""
import sys
import time
from typing import Union, Dict, Optional, List

import click
from colorama import Fore, Style

from connectm import ConnectMBase, ConnectM, PieceColor
from mocks import ConnectMMock, ConnectMStub
from bot import RandomBot, SmartBot


class TUIPlayer:
    """
    Simple class to store information about a TUI player

    A TUI player can either a human player using the keyboard,
    or a bot.
    """

    name: str
    bot: Union[None, RandomBot, SmartBot]
    connectm: ConnectMMock
    color: PieceColor
    bot_delay: float

    def __init__(self, n: int, player_type: str, connectm: ConnectMMock,
                 color: PieceColor, opponent_color: PieceColor, bot_delay: float):
        """ Constructor

        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The Connect-M board
            color: The player's color
            opponent_color: The opponent's color
            bot_delay: When playing as a bot, an artificial delay
             (in seconds) to wait before making a move.
        """

        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(connectm, color, opponent_color)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(connectm, color, opponent_color)
        self.connectm = connectm
        self.color = color
        self.bot_delay = bot_delay

    def get_move(self) -> int:
        """ Gets a move from the player

        If the player is a human player, prompt the player for a column.
        If the player is a bot, ask the bot to suggest a move.

        Returns: None

        """
        if self.bot is not None:
            time.sleep(self.bot_delay)
            column = self.bot.suggest_move()
            # Print prompt with column already filled in
            print(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL + str(column+1))
            return column
        else:
            # Ask for a column (and re-ask if
            # a valid column is not provided)
            while True:
                v = input(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL)
                if v.isnumeric():
                    try:
                        col = int(v) - 1
                        if col < self.connectm.num_cols and self.connectm.can_drop(col):
                            return col
                    except ValueError:
                        continue


def print_board(grid: List[List[Optional[PieceColor]]]) -> None:
    """ Prints the board to the screen

    Args:
        grid: The board to print

    Returns: None
    """

    nrows = len(grid)
    ncols = len(grid[0])

    # Top row
    print(Fore.BLUE + "┌" + ("─┬" * (ncols-1)) + "─┐")

    for r in range(nrows):
        crow = "│"
        for c in range(ncols):
            v = grid[r][c]
            if v is None:
                crow += " "
            elif v == PieceColor.RED:
                crow += Fore.RED + Style.BRIGHT + "●"
            elif v == PieceColor.YELLOW:
                crow += Fore.YELLOW + Style.BRIGHT + "●"
            crow += Fore.BLUE + Style.NORMAL + "│"
        print(crow)

        if r < nrows - 1:
            print(Fore.BLUE + "├" + ("─┼" * (ncols-1)) + "─┤")
        else:
            print(Fore.BLUE + "└" + ("─┴" * (ncols-1)) + "─┘" + Style.RESET_ALL)


def play_connect_4(connectm: ConnectMBase, players: Dict[PieceColor, TUIPlayer]) -> None:
    """ Plays a game of Connect Four on the terminal

    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
          TUIPlayer objects.

    Returns: None

    """
    # The starting player is yellow
    current = players[PieceColor.YELLOW]

    # Keep playing until there is a winner:
    while not connectm.done:
        # Print the board
        print()
        print_board(connectm.grid)
        print()

        column = current.get_move()

        # Drop the piece
        connectm.drop(column, current.color)

        # Update the player
        if current.color == PieceColor.YELLOW:
            current = players[PieceColor.RED]
        elif current.color == PieceColor.RED:
            current = players[PieceColor.YELLOW]

    print()
    print_board(connectm.grid)

    winner = connectm.winner
    if winner is not None:
        print(f"The winner is {players[winner].name}!")
    else:
        print("It's a tie!")


#
# Command-line interface
#

@click.command(name="connect4-tui")
@click.option('--rows', type=click.INT, default=6)
@click.option('--cols', type=click.INT, default=7)
@click.option('--m', type=click.INT, default=4)
@click.option('--mode',
              type=click.Choice(['real', 'stub', 'mock'], case_sensitive=False),
              default="real")
@click.option('--player1',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="human")
@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="human")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)
def cmd(rows, cols, m, mode, player1, player2, bot_delay):
    if mode == "real":
        board = ConnectM(rows, cols, m)
    elif mode == "stub":
        board = ConnectMStub(rows, cols, m)
    elif mode == "mock":
        board = ConnectMMock(rows, cols, m)

    player1 = TUIPlayer(1, player1, board, PieceColor.YELLOW, PieceColor.RED, bot_delay)
    player2 = TUIPlayer(2, player2, board, PieceColor.RED, PieceColor.YELLOW, bot_delay)

    players = {PieceColor.YELLOW: player1, PieceColor.RED: player2}

    play_connect_4(board, players)


if __name__ == "__main__":
    cmd()
