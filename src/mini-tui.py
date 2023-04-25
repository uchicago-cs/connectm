from connectm import ConnectM, PieceColor

def play_connect_4():
    # Create the game
    connectm = ConnectM(nrows=6, ncols=7, m=4)

    # The starting player is yellow
    current = PieceColor.YELLOW

    # Keep playing until there is a winner:
    while True:
        # Print the board
        print(connectm)

        # Ask for a column (and re-ask if
        # a valid column is not provided)
        column = None
        while column is None:
            v = input("> ")
            if v in "1234567":
                v = int(v) - 1
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
    play_connect_4()
