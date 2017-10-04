# Farmer-and-Knight-via-Search-Algorithms
Here we use a breadth-first search algorithm with dynamic programming to solve the infamous farmer-goat-wolf-cabbage problem and to determine the shortest path a knight can take from the bottom-left position on a chessboard to the top-right position. 

To compute the solutions, run the program and print (farmer) or print (knight). The solutions are represented as a list of ordered pairs containing the previous action and resulting state. 

In the case of the farmer, the state is a four-tuple containing the locations of the farmer, goat, wolf, and cabbage, respectively, where those locations can be 'L' or 'R' (for left side and right side of the river, respectively). So, the starting position is ('L', 'L', 'L', 'L'). The actions correspond to the object taken by the farmer from his current position to the opposite position (e.g. 'takeGoat'). 

In the case of the knight, chessboard positions are represented via an ordered tuple of (x,y) coordinates (more technically: the coordinates correspond to the bottom-left corner of each square with unit length being the side length of a single square and origin being the bottom-left corner of the board). So, (0,0) is the bottom-left position and (7,7) is the top-right position. Actions are represented as two-character strings with characters 'u', 'd', 'l', and 'r' (for "up", "down", "left", and "right", respectively), where the first character denotes what direction the knight moved two squares and the second character denotes what direction the knight moved one square. For example, 'ur' refers to the knight moving two squares up and one square to the right. 

See comments in the code for details on how this was accomplished via search algorithms and state machines. 
