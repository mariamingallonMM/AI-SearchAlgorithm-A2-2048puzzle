# AI-SearchAlgorithm-A2-2048puzzle
Create an agent to intelligently play the 2048-puzzle game.


The skeleton code includes the following files. Note that you will only be working in one of them, and the rest of them are read-only:

Read-only: GameManager.py. This is the driver program that loads your Computer AI and Player AI, and begins a game where they compete with each other. See below on how to execute this program.
Read-only: Grid.py. This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone(), which you may use in your code. These are available to get you started, but they are by no means the most efficient methods available. If you wish to strive for better performance, feel free to ignore these and write your own helper methods in a separate file.
Read-only: BaseAI.py. This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different "moves" for different AIs).
Read-only: ComputerAI.py. This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.
Writable: PlayerAI.py. You will create this file, and this is where you will be doing your work. This should inherit from BaseAI. The getMove() function, which you will need to implement, returns a number that indicates the player’s action. In particular, 0 stands for "Up", 1 stands for "Down", 2 stands for "Left", and 3 stands for "Right". You need to create this file and make it as intelligent as possible. You may include other files in your submission, but they will have to be included through this file.
Read-only: BaseDisplayer.py and Displayer.py. These print the grid.
.

To test your code, execute the game manager like so:

$ python3 GameManager.py

The progress of the game will be displayed on your terminal screen, with one snapshot printed after each move that the Computer AI or Player AI makes. The Player AI is allowed 0.2 seconds to come up with each move. The process continues until the game is over; that is, until no further legal moves can be made. At the end of the game, the maximum tile value on the board is printed.

IMPORTANT: Do not modify the files that are specified as read-only. When your submission is graded, the grader will first automatically over-write all read-only files in the directory before executing your code. This is to ensure that all students are using the same game-play mechanism and computer opponent, and that you cannot "work around" the skeleton program and manually output a high score.