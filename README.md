# Chess ♟️

A comprehensive chess implementation from scratch that includes all functionalities, such as en passant, castling, and pawn promotion. An AI based on the minimax algorithm was also created. Additionally, a PyGame GUI provides a user-friendly interface for playing the game.

## Motivation 💪

I have played chess casually on and off for a couple of years, and wanted to learn chess programming. Also, since I am not very good at chess, I thought it would be interesting to see if I could create an AI that could play better than me.

## Installation 📦

To install the required packages, use the following command: `pip install -r requirements.txt`

## Playing Chess

To play a game of chess simply run:

`python3 main.py`

This will run the game with user input for both white and black player.

For both white and black player you can choose different player types:

-   User - User input
-   Random - Random legal moves
-   MiniMax - AI Bot
-   AlphaBeta - Minimax, but faster

If you, as the white player, want to play against the AlphaBeta bot you would run:

`python3 main.py User AlphaBeta`

## Development Process 👨‍💻

I wanted to document my development process as it might be useful for anyone who might want to try a similar project themselves 😄

### Testing

Checking if a chess implementation is correct may seem difficult given the large number of different states a game can be in. Certain specific situations occur relatively rarely, such as en passant, castling, and pawn promotion.

A good way to test that the game logic is correct is to take a game state (FEN string) and calculate the number of different states you can end up at different depths. A depth here is defined as a move for one player, also known as a ply. One could look at this as a tree structure, where the nodes are game states and edges are the moves leading to those nodes. This testing method is known [perft](https://www.chessprogramming.org/Perft).

For example, at the initial state of a chess game, white player has the possibility to make one of 20 different moves. This means that at a depth of 1, there are 20 nodes. Black player has the possibility of making the exactly the same number of moves regardless of white player's move, meaning that there are 20 x 20 = 400 possible states or nodes at 2 ply.

While this is a good starting point, it doesn't test the more intricate game states. These states usually occur in the middlegame and endgame, and to calculate the number of nodes more than a few depths can be computationally infeasible, as the number of nodes grows rapidly.

A better approach would therefore be to set the game to a middlegame or endgame state, and then calculate nodes at different depths from there. The Chess Programming Wiki has a [list of different perft results](https://www.chessprogramming.org/Perft_Results) which have been proven to be useful for debugging chess programs. These were used to debug my game logic. Below is a GIF of my program running through all possible states, with initial state perft position 5, and a depth of 2:

<img alt="My program displaying all nodes from Position 5 with depth 2" src="./README_images/chess_node_calculation.gif" width="400">

Once I found a discrepancy between the number of nodes calculated by my program, and the results on Chess Programming Wiki, I did the same calculations with [Stockfish](https://disservin.github.io/stockfish-docs/). Using Stockfish was very helpful since it outputs the number of leaf nodes for all nodes at depth 1. The example below shows the number of possible nodes for each game state that is possible from the start position (position 5):

<img alt="Stockfish calculating nodes from Position 5" src="./README_images/stockfish_position5.png" width="900">

I could then output the same info from my program:

<img alt="My program calculating nodes from Position 5" src="./README_images/my_program_position5.png" width="500" >

Given this info I could find out what node(s) at depth 1 lead to the discrepancies. I did this by copying the output of Stockfish into `output/stockfish_output.txt` and my program's output into `output/my_program_output.txt`. I then ran `python3 compare_moves.py`, which gave me the nodes that had different number of leaf nodes between the outputs. I could then set such a node to my initial position and perform the calculations again. This was done by entering my initial position into a [FEN viewer website](https://www.dailychess.com/chess/chess-fen-viewer.php), perform the move that lead to a node with discrepancy, and set the new FEN string as the initial position.

For my program, these tests revealed a couple of bugs I was unaware of, mostly regarding castling.

All perfts from the Chess Programming Wiki can be run on my program by running the following command:

`python3 perft.py`

### Optimization

Now that the game logic had been thoroughly tested, it was time to optimize the code to run faster. This is especially important if one wants to create an AI chess bot, as it directly affects evaluation/training time.

At this point my code wasn't particulary fast 😅. The image below shows the number of nodes calculated from the starting position of a chess game:

<img alt="Test times before optimization" src="./README_images/chess_engine_not_optimized.png" width="500" >

To calculate the number of nodes at a depth of 5, it takes 7.5 minutes!

The most obvious way to speed up my chess program would be to change to a compiled language such as C or C#. This comes at the cost of development time. A reasonable solution would therefore be to use a JIT-compiler for my already developed code. However this proved to be challenging as Numba (the JIT library) lacks support a lot of Python functionality. Numba might be an option I revisit in the future.

I ended up optimizing the speed of my code by limiting the number of calculations and array accesses, and rather store more results in memory. There is almost always a space-time tradeoff in software programs, and I chose to optimize on time.

Running the perft tests was a good way to measure the speed of my code. Before optimization it took my code ~26 seconds to run the tests. I managed to reduce this to ~16 seconds, purely by rewriting my code.

### Chess AI (Minimax algorithm)

The standard minimax algorithm with a search tree depth of 3 took approximately 20 seconds to calculate one move, which is way too long. After implementing alpha-beta pruning one move on average took 5.6 seconds, meaning that the bot became nearly 4x faster!

## Cool Resources

Some cool resources I found while developing:

-   The book I have used to learn about minimax, alpha-beta, and AI in general: _Russell, S. J., & Norvig, P. (2016). Artificial intelligence : a modern approach (3rd ed.; Global ed.). Pearson._
-   Video that inspired me to do this project: https://www.youtube.com/watch?v=U4ogK0MIzqk
-   Website to analyse your chess games for free: https://chess.wintrcat.uk/
