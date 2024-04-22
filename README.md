# Chess ♟️

A personal project for learning chess programming.

## Terminology

### Moves

There is a difference between possible moves: Attacked squares are all squares that are in the attacking view of a piece. These are both legal and illegal moves. For example a piece can threaten the opposite color king even if it is pinned (it can threaten the opponents king even if it could not legally have gone to that square, for example if that would have set its own king in check).

While a move here (and generally speaking) is referred to as a piece being moved to a square, in the code, a "move" also includes what piece is ends up on that square. In most cases it will be the same piece that was on the starting square, however in the case of pawn promotion, it will be another piece. Therefore, in the code, a "move" (where the starting position is given) is a tuple: (end_position, piece).

## Resources

-   Cool website to analyse your chess games for free: https://chess.wintrcat.uk/
