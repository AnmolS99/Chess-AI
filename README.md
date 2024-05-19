# Chess ♟️

A personal project for learning chess programming.

## Terminology

### Moves

There is a difference between possible moves: Attacked squares are all squares that are in the attacking view of a piece. These are both legal and illegal moves. For example a piece can threaten the opposite color king even if it is pinned (it can threaten the opponents king even if it could not legally have gone to that square, for example if that would have set its own king in check).

While a move here (and generally speaking) is referred to as a piece being moved to a square, in the code, a "move" also includes what piece is ends up on that square. In most cases it will be the same piece that was on the starting square, however in the case of pawn promotion, it will be another piece. Therefore, in the code, a "move" (where the starting position is given) is a tuple: (end_position, piece).

## Development Process

### Testing

Checking if a chess implementation is correct may seem difficult given the large number of different states a game can be in. Certain specific situations occur relatively rarely, such as en passant, castling, and pawn promotion.

A good way to test that the game logic is correct is to, given a game state (FEN string), calculate the number of different states you can end up at different depths. A depth here is defined as a move for one player, also known as a ply. One could look at this as a tree structure, where the nodes are game states and edges are moves made. This testing method is also known [perft](https://www.chessprogramming.org/Perft).

For example, at the initial state of a chess game, white player has the possibility to make one of 20 different moves. This means that at a depth of 1, there are 20 nodes. Since black player has the possibility of making the exact same moves regardless of white player's move, there are 20 x 20 = 400 possible states or nodes at 2 ply.

While this is a good starting point, it doesn't test the more intricate game states. These states usually occur in the middlegame and endgame, and to calculate the number of nodes more than a few depths can be computationally expensive, as the number of nodes rapidly grows.

A better approach would therefore be to set the game to a middlegame or endgame state, and then calculate nodes at different depths from here. The Chess Programming Wiki has a [list of different perft results](https://www.chessprogramming.org/Perft_Results) which have been proven to be useful for debugging chess implementation. These were used to debug my game logic. Once I found a discrepancy between the number of nodes calculated by my program, and the results on Chess Programming Wiki, I did the same calculations with [Stockfish](https://disservin.github.io/stockfish-docs/).

Using Stockfish was very helpful since it outputs the number of leaf nodes for all nodes at depth 1. The example below shows the number of possible nodes for each game state that is possible from the start position (position 5):

![Stockfish calculating nodes from Position 5](./README_images/stockfish_position5.png)

I could then output the same info from my program:

![My program calculating nodes from Position 5](./README_images/my_program_position5.png)

Given this info I could find out what node(s) at depth 1 lead to the discrepancies. I did this by copying the output of Stockfish into `output/stockfish_output.txt` and my program's output into `output/my_program_output.txt`. I then ran `python3 compare_moves.py`, which gave me the nodes that had different number of leaf nodes between the outputs. I could then set such a node to my initial position and perform the calculations again. This was done by entering my initial position into a [FEN viewer website](https://www.dailychess.com/chess/chess-fen-viewer.php), perform the move that lead to a node with discrepancy, and set the new FEN string as the initial position.

For my program, these tests revealed a couple of bugs I was unaware of, mostly regarding castling.

All perfts from the Chess Programming Wiki can be run on my program by running the following command:

`python3 perft.py`

### Optimization

Now that the game logic had been thoroughly tested, it was time to optimize the code to run faster. This is especially important if one wants to create an AI chess bot, as it directly affects evaluation/training time.

At this point my code wasn't particulary fast 😅 The image below shows the number of nodes calculated from the starting position of a chess game:

![Test times before optimization](./README_images/chess_engine_not_optimized.png)

To calculate the number of nodes at a depth of 5, it takes 7.5 minutes!

The most obvious way to speed up my chess program would be to change to a compiled language such as C or C#. This comes at the cost of development time. A reasonable solution would therefore be to use a JIT-compiler for my already developed code.

## Cool Resources

Some cool resources I found while developing:

-   Video that inspired me to do this project: https://www.youtube.com/watch?v=U4ogK0MIzqk
-   Website to analyse your chess games for free: https://chess.wintrcat.uk/
