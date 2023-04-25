"""
GUI for Connect Four
"""

import os
import sys
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import click

from connectm import ConnectMBase, ConnectM, PieceColor
from mocks import ConnectMStub, ConnectMMock
from bot import RandomBot, SmartBot

DEFAULT_SIDE = 75
SMALL_SIDE = 40

class GUIPlayer:
    """
    Simple class to store information about a GUI player

    A TUI player can either a human player using the keyboard,
    or a bot.
    """

    name: str
    bot: Union[None, RandomBot, SmartBot]
    connectm: ConnectMBase
    color: PieceColor

    def __init__(self, n: int, player_type: str, connectm: ConnectMBase,
                 color: PieceColor, opponent_color: PieceColor):
        """ Constructor

        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The Connect-M board
            color: The player's color
            opponent_color: The opponent's color
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


def draw_board(surface: pygame.surface.Surface, connectm: ConnectMBase) -> None:
    """ Draws the current state of the board in the window

    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw

    Returns: None

    """
    grid = connectm.grid
    nrows = connectm.num_rows
    ncols = connectm.num_cols

    width, height = surface.get_size()

    surface.fill((64, 128, 255))

    # Compute the row height and column width
    rh = height // nrows
    cw = width // ncols

    # Draw the borders around each cell
    for row in range(nrows):
        for col in range(ncols):
            rect = (col * cw, row * rh, cw, rh)
            pygame.draw.rect(surface, color=(32, 32, 192),
                             rect=rect, width=2)

    # Draw the circles
    for i, r in enumerate(grid):
        for j, piece_color in enumerate(r):
            if piece_color is None:
                color = (255, 255, 255)
            elif piece_color == PieceColor.RED:
                color = (255, 0, 0)
            elif piece_color == PieceColor.YELLOW:
                color = (255, 255, 0)

            center = (j * cw + cw // 2, i * rh + rh // 2)
            radius = rh // 2 - 8
            pygame.draw.circle(surface, color=color,
                               center=center, radius=radius)


def play_connect_4(connectm: ConnectMBase, players: Dict[PieceColor, GUIPlayer],
                   bot_delay: float) -> None:
    """ Plays a game of Connect Four on a Pygame window

    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
          TUIPlayer objects.
        bot_delay: When playing as a bot, an artificial delay
          (in seconds) to wait before making a move.

    Returns: None

    """

    if connectm.num_rows * connectm.num_cols <= 42:
        side = DEFAULT_SIDE
    else:
        side = SMALL_SIDE

    width = side * connectm.num_cols
    height = side * connectm.num_rows

    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Connect Four")
    surface = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # The starting player is yellow
    current = players[PieceColor.YELLOW]

    while not connectm.done:
        # Process Pygame events
        # If a key is pressed, check whether it's
        # a column key (1-7).
        # If the user closes the window, quit the game.
        events = pygame.event.get()
        column = None
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for key and mouse events, but only if the
            # current player is a human
            if current.bot is None: 
                if event.type == pygame.KEYUP and connectm.num_cols <= 10:
                    key = event.unicode
                    v = None
                    if key in "123456789":
                        v = int(key) - 1
                    elif key == "0":
                        v = 9

                    if v is not None and connectm.can_drop(v):
                        column = v
                elif event.type == pygame.MOUSEBUTTONUP:
                    x = event.pos[0]
                    column = x // side

        # If the current player is a bot, have it suggest
        # a move
        if current.bot is not None:
            pygame.time.wait(int(bot_delay * 1000))
            column = current.bot.suggest_move()

        # If there is a column to drop a piece in
        # (either because a human user pressed a key,
        # or a bot suggested one), make a move
        if column is not None:
            connectm.drop(column, current.color)

            # Update the player
            if current.color == PieceColor.YELLOW:
                current = players[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = players[PieceColor.YELLOW]

        # Update the display
        draw_board(surface, connectm)
        pygame.display.update()
        clock.tick(24)

    # Print the winner (on the terminal)
    winner = connectm.winner
    if winner is not None:
        print(f"The winner is {players[winner].name}!")
    else:
        print("It's a tie!")


#
# Command-line interface
#

@click.command(name="connect4-gui")
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
        connectm = ConnectM(rows, cols, m)
    elif mode == "stub":
        connectm = ConnectMStub(rows, cols, m)
    elif mode == "mock":
        connectm = ConnectMMock(rows, cols, m)

    player1 = GUIPlayer(1, player1, connectm, PieceColor.YELLOW, PieceColor.RED)
    player2 = GUIPlayer(2, player2, connectm, PieceColor.RED, PieceColor.YELLOW)

    players = {PieceColor.YELLOW: player1, PieceColor.RED: player2}

    play_connect_4(connectm, players, bot_delay)

if __name__ == "__main__":
    cmd()
