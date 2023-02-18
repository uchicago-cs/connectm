"""
GUI for Connect Four
"""

import os
import sys
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import click

from connectm import ConnectMBoard, PieceColor, BoardType
from mocks import ConnectMBoardStub, ConnectMBoardMock
from bot import RandomBot, SmartBot

WIDTH = 600
HEIGHT = 400


class GUIPlayer:
    """
    Simple class to store information about a GUI player

    A TUI player can either a human player using the keyboard,
    or a bot.
    """

    name: str
    bot: Union[None, RandomBot, SmartBot]
    board: BoardType
    color: PieceColor

    def __init__(self, n: int, player_type: str, board: BoardType,
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
            self.bot = RandomBot(board, color, opponent_color)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(board, color, opponent_color)
        self.board = board
        self.color = color


def draw_board(surface: pygame.surface.Surface, board: BoardType) -> None:
    """ Draws the current state of the board in the window

    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw

    Returns: None

    """
    grid = board.to_piece_grid()
    nrows = len(grid)
    ncols = len(grid[0])

    surface.fill((64, 128, 255))

    # Compute the row height and column width
    rh = HEIGHT // nrows + 1
    cw = WIDTH // ncols + 1

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


def play_connect_4(board: BoardType, players: Dict[PieceColor, GUIPlayer],
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

    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Connect Four")
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # The starting player is yellow
    current = players[PieceColor.YELLOW]

    while not board.is_done():
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

            # Check for key events, but only if the
            # current player is a human
            if current.bot is None and event.type == pygame.KEYUP:
                key = event.unicode
                if key in "1234567":
                    v = int(key) - 1
                    if board.can_drop(v):
                        column = v

        # If the current player is a bot, have it suggest
        # a move
        if current.bot is not None:
            pygame.time.wait(int(bot_delay * 1000))
            column = current.bot.suggest_move()

        # If there is a column to drop a piece in
        # (either because a human user pressed a key,
        # or a bot suggested one), make a move
        if column is not None:
            board.drop(column, current.color)

            # Update the player
            if current.color == PieceColor.YELLOW:
                current = players[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = players[PieceColor.YELLOW]

        # Update the display
        draw_board(surface, board)
        pygame.display.update()
        clock.tick(24)

    # Print the winner (on the terminal)
    winner = board.get_winner()
    if winner is not None:
        print(f"The winner is {players[winner].name}!")
    else:
        print("It's a tie!")


#
# Command-line interface
#

@click.command(name="connect4-gui")
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
def cmd(mode, player1, player2, bot_delay):
    if mode == "real":
        board = ConnectMBoard(nrows=6, ncols=7, m=4)
    elif mode == "stub":
        board = ConnectMBoardStub(nrows=6, ncols=7, m=4)
    elif mode == "mock":
        board = ConnectMBoardMock(nrows=6, ncols=7, m=4)

    player1 = GUIPlayer(1, player1, board, PieceColor.YELLOW, PieceColor.RED)
    player2 = GUIPlayer(2, player2, board, PieceColor.RED, PieceColor.YELLOW)

    players = {PieceColor.YELLOW: player1, PieceColor.RED: player2}

    play_connect_4(board, players, bot_delay)

if __name__ == "__main__":
    cmd()
