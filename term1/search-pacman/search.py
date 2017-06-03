# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    start = problem.getStartState()
    stack = util.Stack()
    stack.push((start, []))
    visited = set()
    actions = dfs_helper(problem, stack, visited)
    return actions


def dfs_helper(problem, stack, visited):
    while stack:
        (vertex, path) = stack.pop()

        if vertex not in visited:
            if problem.isGoalState(vertex):
                return path
            visited.add(vertex)
            for neighbor in problem.getSuccessors(vertex):
                stack.push((neighbor[0], path + [neighbor[1]]))


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    queue = util.Queue()
    queue.push((start, []))
    visited = set()
    actions = bfs_helper(problem, queue, visited)
    # print('actions:{}'.format(actions))


    # actions = []
    return actions


def bfs_helper(problem, queue, visited):
    while queue:
        (vertex, path) = queue.pop()
        # print('vertex:{}.In:{}'.format(vertex,vertex in visited))

        # print('visited:{}'.format(visited))
        if vertex not in visited:
            if problem.isGoalState(vertex):
                return path
            visited.add(vertex)
            # print('neighbors:{}'.format(problem.getSuccessors(vertex)))
            for neighbor in problem.getSuccessors(vertex):
                queue.push((neighbor[0], path + [neighbor[1]]))


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    priorityQueue = util.PriorityQueue()
    start = problem.getStartState()
    priorityQueue.push((start, []), 0)
    explored = set()
    actions = uniform_helper(problem, priorityQueue, explored)
    return actions


def uniform_helper(problem, priorityQueue, explored):
    while priorityQueue:
        (priority, vertex) = priorityQueue.pop()
        item = vertex[0]
        path = vertex[1]
        if item not in explored:
            if problem.isGoalState(item):
                return path
            explored.add(item)
            for neighbor in problem.getSuccessors(item):
                priorityQueue.push((neighbor[0], path + [neighbor[1]]), priority + neighbor[2])


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    priorityQueue = util.PriorityQueueWithFunction(heuristic)
    start = problem.getStartState()
    priorityQueue.push((start, []), problem)
    explored = set()
    actions = aStarSearch_helper(problem, priorityQueue, explored)
    return actions


def aStarSearch_helper(problem, priorityQueue, explored):
    while priorityQueue:
        (priority, vertex) = priorityQueue.pop()
        item = vertex[0]
        path = vertex[1]
        if item not in explored:
            if problem.isGoalState(item):
                return path
            explored.add(item)
            for neighbor in problem.getSuccessors(item):
                priorityQueue.push((neighbor[0], path + [neighbor[1]]), problem)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
