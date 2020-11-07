# AI-SearchAlgorithm-A2-2048puzzle
## Week 4 Project: Adversarial Search and Games
In this assignment we were asked to create an agent to intelligently play the **2048-puzzle game**, using more advanced techniques to probe the search space than the simple methods used in the previous assignment. 

Try playing the game here: [gabrielecirulli.github.io/2048](https://gabrielecirulli.github.io/2048) to get a sense of how the game works. 
The assignmen includes implementing an adversarial search algorithm that plays the game intelligently, perhaps much more so than playing by hand.

[spinner_2048.gif](img/spinner.gif)

## Code structure
The skeleton code includes the following files. Note that from the '.py' files, only PlayerAI.py file has been written by author; the rest of the files were provided as part of the assignment and could not be modified. The exception was the time.clock() vs time.process_time() as the former had been deprecated in current version of Python. 

### Read-only: GameManager.py. 
This is the driver program that loads your Computer AI and Player AI, and begins a game where they compete with each other. See below on how to execute this program.

### Read-only: Grid.py. 
This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone(), which you may use in your code. These are available to get you started, but they are by no means the most efficient methods available. If you wish to strive for better performance, feel free to ignore these and write your own helper methods in a separate file.

### Read-only: BaseAI.py. 
This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different "moves" for different AIs).


### Read-only: ComputerAI.py. 
This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.


### Writable: PlayerAI.py. 
This is where the coding work for this assignment has taken place. This file inherits from BaseAI. The getMove() function returns a number that indicates the player’s action. In particular: 
- 0 stands for "Up", 
- 1 stands for "Down", 
- 2 stands for "Left", and 
- 3 stands for "Right". 


### Read-only: BaseDisplayer.py and Displayer.py. 
These print the grid.

### Execute the GameManager as follows:

$ python3 GameManager.py

The progress of the game will be displayed on your terminal screen, with one snapshot printed after each move that the Computer AI or Player AI makes. Note that the Player AI is allowed 0.2 seconds to come up with each move. The process continues until the game is over; that is, until no further legal moves can be made. At the end of the game, the maximum tile value on the board is printed.

## References
The following references have been instrumental in understanding alpha-beta pruning and minimax algorithm techniques. Recommend reading:
- [Understanding the Minimax Algorithm](https://towardsdatascience.com/understanding-the-minimax-algorithm-726582e4f2c6) by [Dorian Lazar](https://medium.com/@dorianlazar)
- Series of 3 articles to implement minimax algorithm to 2048 game, [How to apply Minimax to 2048](https://towardsdatascience.com/playing-2048-with-minimax-algorithm-1-d214b136bffb) by [Dorian Lazar](https://medium.com/@dorianlazar)
- [Visualise alpha-beta pruning and minimax](http://homepage.ufp.pt/jtorres/ensino/ia/alfabeta.html) by José Manuel Torres.
- [Beginner’s guide to AI and writing your own bot for the 2048 game](https://medium.com/@bartoszzadrony/beginners-guide-to-ai-and-writing-your-own-bot-for-the-2048-game-4b8083faaf53) by 
- [AI Plays 2048](http://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf) by Yun Nie (yunn), Wenqi Hou (wenqihou), Yicheng An (yicheng) from CS229, Stanford University.

## Future development

- Started trying to implement an index.html to show the PlayerAI on:
https://mariamingallonmm.github.io/AI-SearchAlgorithm-A2-2048puzzle/
- It could be similar to how it is done in this article using Selenium: https://towardsdatascience.com/how-to-control-the-game-board-of-2048-ec2793db3fa9 & github: https://github.com/lazuxd/playing-2048-with-minimax.
- Reference for Selenium: [Selenium WebDriver: Browse the Web with Code](https://medium.com/towards-artificial-intelligence/selenium-webdriver-browse-the-web-with-code-f064d3556a8)
- An alternative could be using Flask.
