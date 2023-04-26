# Connect-M

This repository contains a design and implementation
for Connect-M (a general version of [Connect Four](https://en.wikipedia.org/wiki/Connect_Four)).
It is an example of what a completed CMSC 14200 course project
should look like.

# Setup

Running the code in this repository requires using a number of
Python libraries. We recommend creating a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
before installing these libraries. To do so, run the
following from the root of your local repository:

    python3 -m venv venv

To activate your virtual environment, run the following:

    source venv/bin/activate

You should now see `(venv)` in your terminal prompt, indicating
that the virtual environment is active, e.g.:

    (venv) student@linux1:~/repos/connectm$

Using a virtual environment has many benefits, but the main
one is that you can install Python libraries just for
a specific project you're working on (in this case, the
`connectm` repository) without interfering with the Python
libraries you may already have elsewhere on your computer.

To install the required Python libraries run the following:

    pip3 install -r requirements.txt

To deactivate the virtual environment (e.g., because you're done
working on the `connectm` code), just run the following:

    deactivate

# Running the TUI

To run the TUI, run the following from the root of the repository:

    python3 src/tui.py

The TUI displays the state of the board, and asks for a player's
next move. You must specify a column number (1 through 7) where
you would like to drop a piece. If the number is not valid for
any reason, you will be prompted again.

By default the TUI creates a Connect Four board (six rows, seven
column, and four contiguous pieces needed to win). You can specify 
an alternate number of rows, columns, or contiguous pieces to win
with the `--rows`, `--columns`, and `--m` parameters (respectively)

You can also play against a bot like this:

    python3 src/tui.py --player2 <bot>

Where ``<bot>`` is either ``random-bot`` or ``smart-bot`` (the
bots are described further below).

You can even have two bots play against each other:

    python3 src/tui.py --player1 <bot> --player2 <bot>

The TUI inserts an artificial delay of half a second between each bot's
move, so that you can more easily observe the progress of the game.
You can modify this delay using the ``--bot-delay <seconds>`` parameter.

# Running the GUI

To run the GUI, run the following from the root of the repository:

    python3 src/gui.py

The GUI displays the state of the board. To drop a piece, click
on the column you'd like to drop a piece in. If board with 10
or less columns, you can also press a key 1 and 9, or 0 for 10 
(depending on what column you want to drop a piece in).

By default the GUI creates a Connect Four board (six rows, seven
column, and four contiguous pieces needed to win). You can specify 
an alternate number of rows, columns, or contiguous pieces to win
with the `--rows`, `--columns`, and `--m` parameters (respectively)

Like the TUI, you can play against a bot, or have two bots play
against each other like this:

    python3 src/tui.py --player2 <bot>

    python3 src/tui.py --player1 <bot> --player2 <bot>

The ``--bot-delay <seconds>`` parameter is also supported.

# Bots

The ``bots.py`` file includes two classes:

- ``RandomBot``: A bot that will just choose a move at random
- ``SmartBot``: A bot that will try to make a winning move if possible.
  If no such move is possible, it checks whether the opposing player
  would win in the next move and, if so, it blocks that move. Otherwise,
  it just picks a move at random.

These two classes are used in the TUI and GUI, but you can also run
``bots.py`` to run 10,000 simulated games where two bots face each other,
and see the percentage of wins and ties. For example:

    $ python3 src/bot.py --player1 random --player2 random
    Bot 1 (random) wins: 55.59%
    Bot 2 (random) wins: 44.12%
    Ties: 0.29%
    
    $ python3 src/bot.py --player1 random --player2 smart
    Bot 1 (random) wins: 4.23%
    Bot 2 (smart) wins: 95.51%
    Ties: 0.26%

You can control the number of simulated games using the ``-n <number of games>`` parameter
to ``bots.py``.

# Running with stubs and mocks

Stub and mock implementations of the ``ConnectMBase`` class are
available in the ``mocks.py`` file. 

The TUI and GUI both accept a ``--mode <mode>`` parameter, where
``<mode>`` is one of:

- ``real``: Use the ``ConnectM`` class (default)
- ``stub``: Use the ``ConnectMStub`` class
- ``mock``: Use the ``ConnectMMock`` class

Additionally, we also include a simplified TUI that can be run
like this:

- `python3 src/mini-tui.py` to use the ``ConnectM`` class
- `python3 src/mini-tui.py stub` to use the ``ConnectMStub`` class
- `python3 src/mini-tui.py mock` to use the ``ConnectMMock`` class

The bots have their own mock class (``ConnectMBotMock``),
which is used in a series of automated tests that can be run
like this:

    pytest tests/test_bot.py
