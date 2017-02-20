# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: 
When:We applied the naked twins elimination when we try to reduce time complexitaty of the Sudoku problems along with eliminate and only_choice techniques. 
What:So the naked twins algorithms will: 
    1. look for the combinations of naked twins. 
    2. for each combination of naked twins, reduce the Sudoku problems by removing digits vertically, horizontally as well as inside the 9*9 box.
Note:There are more heruistics we can use to reduce time complexitaty of Sudoku problems. I think most of the algorithms are powered by constraint propagation & satisfaction.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We basically use diagonal_unitlist, diagonal_list and diagonal_peers instead of original ones when we try to apply eliminate,reduce as well as search algorithms. Constraint propagation and satisfyication are the underlying AI building blocks that support eliminate,reduce and search algorithms.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
