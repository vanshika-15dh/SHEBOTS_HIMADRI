# Task 1 – Autonomous Game Engine

## Introduction

In this task, we built a chess engine that can play a **6 × 6 chess variant**. The engine takes a board configuration as input and determines a strong move for the player whose turn it is.

Our main idea was simple: first generate all possible legal moves, then explore how the game might continue after each move, and finally choose the move that leads to the most promising board position.

One challenge in chess engines is that the number of possible game states grows extremely quickly. Exploring every possible continuation would take far too long. To handle this, we designed the engine to focus on the most promising branches while skipping clearly weaker options.

This makes the engine much more practical and allows it to analyze deeper positions within limited time.

---

## Board Representation

The chess board is stored as a **NumPy array of length 36**, which corresponds to the **6 × 6 board**.

Each number in the array represents a specific piece on the board. White and black pieces use different identifiers so that the engine can easily distinguish between them.

| Piece | White ID | Black ID |
|------|------|------|
| Pawn | 1 | 6 |
| Knight | 2 | 7 |
| Bishop | 3 | 8 |
| Queen | 4 | 9 |
| King | 5 | 10 |

Instead of storing the board as a two-dimensional grid, we used a **flattened structure**. This means the board is stored as a single list of 36 values.

For example:

- Index **0–5** represent the first row  
- Index **6–11** represent the second row  

This representation makes indexing easier and speeds up board updates during the search.

Example of how a board state might look conceptually:

[2, 3, 4, 5, 3, 2,
1, 1, 1, 1, 1, 1,
0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0,
6, 6, 6, 6, 6, 6,
7, 8, 9,10, 8, 7]


Here, `0` represents an empty square.

---

## Move Representation

To keep the engine efficient, every move is represented in a **compact format**.

Instead of storing large objects, the source and destination squares are packed together into a single value. This reduces memory usage and speeds up comparisons during the search.

For example, a move such as:
A2 → A3


internally stores the starting square and destination square in a compact encoded form. Whenever needed, the engine can decode this value to determine where the move starts and where it ends.

This approach becomes especially useful when the engine explores thousands of moves while searching deeper positions.

---

## Exploring Possible Moves

To decide the best move, the engine first generates **all legal moves** for the current player.

For each possible move:

1. The move is temporarily applied to the board  
2. The engine checks how the opponent might respond  
3. This process continues several steps into the future  

While exploring these possibilities, the engine keeps track of the strongest position it has found so far. If it becomes clear that a particular path cannot produce a better outcome than an already discovered move, that path is ignored and the engine moves on to the next one.

This helps reduce unnecessary computation and improves overall performance.

---

## Gradual Deepening of Search

Instead of immediately analyzing very deep positions, the engine searches **in stages**.

It first explores a small number of moves ahead and then gradually increases the depth of the search. This way the engine always has a reasonable move ready, even if the deeper search has not finished yet.

This method also helps the engine identify promising moves earlier and focus more attention on them.

---

## Position Evaluation

When the engine reaches the end of a search branch, it estimates how favorable the board position is.

The evaluation mainly considers:

- **Material balance** (which side has stronger pieces)
- **Piece mobility** (how many moves pieces can make)
- **Pawn structure**
- **Piece placement**

Each piece is assigned a value based on its importance in the game. For example, queens are more valuable than pawns, and kings are extremely important since losing the king ends the game.

Using these values, the engine calculates a score that indicates which player has the advantage.

---

## Avoiding Repeated Calculations

During the search, the same board position can sometimes appear through different move sequences.

Instead of recalculating the same position again, the engine stores results of positions that were already analyzed. If the same position appears later, the stored result can be reused.

This significantly improves efficiency, especially when the search goes deeper.

---

## Pawn Promotion Rule

The promotion rule in this variant is slightly different from standard chess.

A pawn can only promote to a piece that has already been **captured earlier in the game**.

For example:

- If a queen has been captured earlier, a pawn reaching the last rank may promote to a queen.
- If only bishops or knights were captured, those become the available promotion options.

This makes promotion depend on how the game has progressed.

---

## Testing the Engine

To make sure the engine behaves correctly, we tested it using different types of board setups.

### Fixed Starting Position

A fixed board configuration was used for debugging and consistent testing. This helped verify that move generation and board updates were working properly.

### Randomized Starting Position

We also experimented with randomized back-rank configurations where pieces were shuffled while still following valid placement rules.

Testing different starting setups ensured that the engine works reliably across a wide variety of board states.

---

## Final Move Output

Once the engine finishes its analysis, it returns the selected move in a readable format such as:

1:A2 -> A3

This indicates that a white pawn moves from square **A2** to **A3**.

---

## Conclusion

In this project, we developed a chess engine capable of playing a **6 × 6 chess variant**.

The engine generates legal moves, explores possible game continuations, evaluates board positions, and selects a move that appears most promising.

By using efficient board representation and focusing on promising search paths, the engine can analyze deeper positions within a reasonable time.

Working on this task helped us understand how strategic decision-making in board games can be translated into computational techniques and optimized for performance.
