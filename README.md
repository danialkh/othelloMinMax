# Othello with Minimax AI

## Description

This is a simple implementation of the game Othello (also known as Reversi) in Python using the Pygame library. It features a Minimax AI opponent.

## Features

*   **Graphical User Interface:** Uses Pygame for a visually appealing game board.
*   **Human vs. AI:** Play against a Minimax AI opponent.
*   **Basic Game Logic:** Implements the core rules of Othello, including move validation and flipping pieces.
*   **Minimax AI:** A simple Minimax algorithm is used for the AI player.

## How to Run

1.  **Prerequisites:**
    *   Python 3.x
    *   Pygame library

    You can install Pygame using pip:

    ```
    pip install pygame
    ```

2.  **Run the Game:**

    Save the code as `MinMax.py` and run it from your terminal:

    ```
    python MinMax.py
    ```

## Controls

*   **Mouse Click:** Click on an empty square on the board to place a piece.
*   **Restart:** Click the "Restart" button to start a new game.
*   **Exit:** Click the "Exit" button to quit the game.

## AI Implementation

The AI uses a Minimax algorithm with a limited search depth (currently 2) to determine the best move. The `performMoveMinMax()` function calculates the optimal move for the AI player.

## Known Issues

*   **AI Difficulty:** The AI is relatively simple due to the limited search depth of the Minimax algorithm.
*   **Hint Button:** The "Hint" button is not functional.

## Future Improvements

*   **Improve AI:** Implement alpha-beta pruning to improve the Minimax algorithm's performance or explore other AI techniques.
*   **Implement Hint:** Make the "Hint" button functional, suggesting possible moves to the player.
*   **GUI Enhancements:** Add more visual feedback and improve the overall user interface.
*   **Difficulty Levels:** Implement different difficulty levels by adjusting the search depth of the Minimax algorithm.
