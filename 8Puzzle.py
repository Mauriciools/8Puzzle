# Import needed libraries
import math
import time

# Class for handling node operations
class Node:
    """ 
    Instantiate a node object with the passed arguments.
    Args:
        data (list): The data/state of the node.
        parent (Node): Node that instantiates the current one.
        cost (int): Cost of iteration.
        heuristic (int): THe value of the heuristic.

        self.g is used to sum up the cost and the heuristics together.
    """
    def __init__(self, data: list, parent = None, cost: int = 0, heuristic: float = 0):
        self.data = data
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.g = self.cost + self.heuristic

    """ 
    Find the position (row, column) in the Node of the given element.
    Args:
        number (int): The element to search within the Node.
    """
    def findPosition(self, number: int):
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):

                # Find and return the row and column of a given number
                if (self.data[row][column] == number):
                    return row, column

    """
    Copy the data from an original node to another one.
    """
    def copyNode(self):
        copiedNode = []

        for row in range(len(self.data)):
            tempRow = []

            # Copies each number of the columns to the tempRow
            for column in range(len(self.data[row])):
                tempRow.append(self.data[row][column])

            # Appends each tempRow to the copied node
            copiedNode.append(tempRow)

        return copiedNode

    """
    Find the available moves for the node.
    The moves are defined only in vertical and horizontal positions and of a single element at a time.
    """
    def findAvailableMoves(self):
        availableMoves = []

        # Find the position (row, column) of the blank tile in the current node
        row, column = self.findPosition(0)

        # Verifies based on the blank position the available moving positions, and append it to a list
        if (row > 0 and row <= 2):
            availableMoves.append([row - 1, column])
        if (column > 0 and column <= 2):
            availableMoves.append([row, column - 1])
        if (row >= 0 and row < 2):
            availableMoves.append([row + 1, column])
        if (column >= 0 and column < 2):
            availableMoves.append([row, column + 1])

        return availableMoves

    """
    Generate child nodes from the current one.
    """
    def generateChildren(self):
        children = []

        # Find the available moves for the current node
        availableMoves = self.findAvailableMoves()

        # For each move
        for move in availableMoves:
            # Find the blank position
            row, column = self.findPosition(0)
            
            # Copies the current node and applies the movement by switching the positions of the blank tile and 
            # the one placed in the position of an available movement  
            copiedNode = self.copyNode()
            copiedNode[move[0]][move[1]], copiedNode[row][column] = self.data[row][column], self.data[move[0]][move[1]]

            # Create a child node from the copied node and append it to the children list
            child = Node(copiedNode, self, self.cost + 1)
            children.append(child)

        return children

# Class to handle 8Puzzle operations, such as the solver for a given game and the calculus for different heuristics
class Puzzle:
    """ 
    Instantiate a 8Puzzle object with the passed arguments.
    Args:
        data (list): The data/state of the initial node.
        
        open (list): list of open/child nodes that will be evaluated in further iterations.
        visited (list): list of already visited nodes. 
        finalNode (Node): node representing the goal state of the game.
    """
    def __init__(self, data):
        self.initialNode = Node(data)
        self.open = []
        self.visited = []

        self.expectedResult = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.finalNode = Node(self.expectedResult)

    """
    Apply a "simple" heuristic.
    This heuristic adds up one to the heuristic value for every tile misplaced in the current node in comparison to the goal state.
    Args:
        childNode (Node): The child node.
    """
    def simpleHeuristic(self, childNode: Node):
        # For every number (0-9) in the matrix, find the corresponding position in the child node and in the final one
        for i in range(9):
            position1 = childNode.findPosition(i)
            position2 = self.finalNode.findPosition(i)

            # If they are not in the same position in both nodes, add 1 to the heuristic of the child node
            if (position1 != position2):
                childNode.heuristic += 1

        childNode.g = childNode.cost + childNode.heuristic
        return childNode.g

    """
    Apply the Manhattan distance heuristic.
    This heuristic adds the distance (vertical + horizontal) to the heuristic value for each misplaced 
    tile at the child node, compared to the corresponding tile in the goal state.
    Args:
        childNode (Node): The child node.
    """
    def manhattanHeuristic(self, childNode: Node):
        # For every number (0-9) in the matrix, find the corresponding position in the child node and in the final one
        for i in range(9):
            position1 = childNode.findPosition(i)
            position2 = self.finalNode.findPosition(i)

            # Find the Manhattan distance (vertical + horizontal) of a tile in the child node to its corresponding goal in the final one
            # And add this value to the child node heuristic
            manhattanDistance = abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])
            childNode.heuristic += manhattanDistance

        childNode.g = childNode.cost + childNode.heuristic
        return childNode.g

    """
    Apply the Euclidian distance heuristic.
    This heuristic adds the distance (as a straight line) to the heuristic value for each misplaced 
    tile at the child node, compared to the corresponding tile in the goal state.
    Args:
        childNode (Node): The child node.
    """
    def euclidianHeuristic(self, childNode: Node):
        # For every number (0-9) in the matrix, find the corresponding position in the child node and in the final one
        for i in range(9):
            position1 = childNode.findPosition(i)
            position2 = self.finalNode.findPosition(i)

            # Find the Euclidian distance (stright line) of a tile in the child node to its corresponding goal in the final one
            # And add this value to the child node heuristic
            euclidianDistance = math.sqrt(math.pow((position1[0] - position2[0]), 2) + math.pow((position1[1] - position2[1]), 2))
            childNode.heuristic += euclidianDistance

        childNode.g = childNode.cost + childNode.heuristic
        return childNode.g

    """
    Solve the 8Puzzle game for a node using a specified method.
    Args:
        method (str): The method for solving the 8Puzzle game.
            (Current available methods: "UC", "A*", "A*+", and "A*++".
            Respectively, they mean: Uniform cost, simple heuristic, Manhattan heuristic, and Euclidian heuristic).
    
        maxIterations (int): Define the number of maximum iterations to reach the solution.
    """
    def solve(self, method: str, maxIterations: int):
        # Add the initial node to the open nodes list
        self.open.append(self.initialNode)

        # If the initial node is the solution, return the initial node
        if (self.initialNode.data == self.expectedResult):
            return self.initialNode

        # Iterate until find the solution or reach the maxIterations defined
        for i in range(maxIterations):
            # Get the current node as the first one of the open list and append it to the visited one
            currentNode = self.open.pop(0)
            self.visited.append(currentNode)

            # If the current node is the expected solution, return it
            if (currentNode.data == self.expectedResult):
                return currentNode

            # For each child generated by the current node
            for child in currentNode.generateChildren():
                # Add the child node to the open list if they are not already in either
                if (child.data not in [n.data for n in self.open] and child.data not in [n.data for n in self.visited]):
                    self.open.append(child)
                    
                    # Apply the selected method by calling the corresponding function
                    match(method):
                        case "UC":
                            child.g = child.cost
                        case "A*":
                            child.g = self.simpleHeuristic(child)
                        case "A*+":
                            child.g = self.manhattanHeuristic(child)
                        case "A*++":
                            child.g = self.euclidianHeuristic(child)
                        case _:
                            print("There is no algorithm available for the specified method or the method doesn't exist.")
                            return None

                    # Sort the open list based on the node.g attribute
                    self.open.sort(key=lambda n: n.g)
# ---------------------------------------------------------------------------------------

# Random data for testing
testData = [[5, 8, 1], [2, 3, 7], [4, 6, 0]]

# Print basic info on the screen about the input data
print("----------8Puzzle solver----------")
print("""Hello, user! :D
You'll be asked to put your input data soon...
Please provide 9 int different numbers from 0 to 8 with spaces between.\n""")

# Ask the input data to the user
inputData = input("Input your data here as requested: ").strip().split(" ")
intInputData = []

# Transform the input data to an integer 3x3 matrix
tempData = []
for i in range(1, 10):
    tempData.append(int(inputData[i - 1]))
    if (i % 3 == 0):
        intInputData.append(tempData)
        tempData = []

# Print the initial node passed by the user
print("Initial node:")
for i in range(len(intInputData)):
    print(intInputData[i])
print('----------------------------------------------------------')

# Ask the user for selecting the desired solving method and the maximum number of iterations
print("""There are four available methods for solving the 8-Puzzle.
UC - Uniform Cost
A* - Simple Heuristic
A*+ - Manhattan Heuristic
A*++ - Euclidian Heuristic 
all - Run all methods one after another
To learn more about each of these methods, please read our report document sent along with this code. :) \n""")
method = input("Select the wanted method for solving the 8-Puzzle (UC, A*, A*+, A*++, all): ").strip()
maxIterations = int(input("Now, please select the maximum number of iterations: "))
print('----------------------------------------------------------')



"""
Function for handling the solving steps and the final printing on the screen to the user.
This function is usefull when we use "all" as the desired method to solve the 8-Puzzle.
In this way, we can just execute this function four times in sequence, as we have four different methods to execute in the "all" option.

Args:
    method (str): The method for solving the 8Puzzle game.
        (Current available methods: "UC", "A*", "A*+", and "A*++".
        Respectively, they mean: Uniform cost, simple heuristic, Manhattan heuristic, and Euclidian heuristic).
"""
def solveAndPrint(method: str):
    # Instantiate the puzzle with the input data passed by the user
    puzzle = Puzzle(intInputData)

    # Calculate elapsed time of the solving step
    start = time.time()
    finalNode = puzzle.solve(method, maxIterations)
    end = time.time()

    # If the code found a proper solution, present the information to the user
    if (finalNode is not None):
        print("Visited nodes:", len(puzzle.visited))
        print("Path taken (cost):", finalNode.cost)
        print("Execution time (s):", end - start)
    # Otherwise throw the failure message
    else:
        print(f"A solution could not be reached within the maximum number of iterations ({maxIterations}).")
        print("Execution time (s):", end - start)

    print('----------------------------------------------------------')
    return

# If all methods were selected at once, we execute them one after another and print the results on the screen also one after another
if (method == "all"):
    print("Solving for UC: ")
    solveAndPrint("UC")

    print("Solving for A*: ")
    solveAndPrint("A*")

    print("Solving for A*+: ")
    solveAndPrint("A*+")

    print("Solving for A*++: ")
    solveAndPrint("A*++")
# Otherwise, just solve and print for the desired method
else:
    solveAndPrint(method)
