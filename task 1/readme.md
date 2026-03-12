# RoboGambit Engine – Task 1

## Introduction

In this task, we built a chess engine capable of playing a 6×6 chess variant. The engine receives a board configuration and determines a strong move for the player whose turn it is.

The overall approach is to generate all possible moves, explore how the game might continue after those moves, and select the move that leads to the most favorable board position.

Since the number of possible game states grows extremely quickly, exploring every possibility would take too long. To make the engine practical, we used several techniques that allow it to focus only on promising branches of the search while ignoring clearly weaker options.

## Board Representation

The chess board is stored as a NumPy array of length 36, representing the 6×6 board. Each number represents a piece on the board:

| Piece  | White ID | Black ID |
|--------|----------|----------|
| Pawn   | 1        | 6        |
| Knight | 2        | 7        |
| Bishop | 3        | 8        |
| Queen  | 4        | 9        |
| King   | 5        | 10       |

Instead of using a 2‑D matrix, we store the board in a flattened format, which simplifies indexing and speeds up board updates.

Example initialization:

```python
import numpy as np

board = np.zeros(36, dtype=int)
board = 4   # white queen
board = 10 # black king
