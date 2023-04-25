import sys

from connectm import ConnectMBase, ConnectM, PieceColor
from mocks import ConnectMStub, ConnectMMock

def play_connect_4(connectm: ConnectMBase) -> None:
    # The starting player is yellow
    current = PieceColor.YELLOW

    # Keep playing until there is a winner:
    while True:
        # Print the board
        print()
        print(connectm)
        print()

        # Ask for a column (and re-ask if
        # a valid column is not provided)
        column = None
        while column is None:
            user_input = input("> ")
            if user_input in "1234567":
                v = int(user_input) - 1
                if connectm.can_drop(v):
                    column = v

        # Drop the piece
        connectm.drop(column, current)

        # If there is a winner, break out of the loop
        if connectm.winner is not None:
            break

        # Update the player
        if current == PieceColor.YELLOW:
            current = PieceColor.RED
        elif current == PieceColor.RED:
            current = PieceColor.YELLOW

    print(connectm)
    print(f"The winner is {current.name}!")

if __name__ == "__main__":
    game: ConnectMBase
    
    if len(sys.argv) == 2 and sys.argv[1] == "stub":
        game = ConnectMStub(nrows=6, ncols=7, m=4)
    elif len(sys.argv) == 2 and sys.argv[1] == "mock":
        game = ConnectMMock(nrows=6, ncols=7, m=4)
    else:
        game = ConnectM(nrows=6, ncols=7, m=4)

    play_connect_4(game)
