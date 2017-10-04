#this class is used by the search algorithm to define search nodes consisting
#of the state of the node, the action taken to reach the node, and its parent
#node
class SearchNode:
    def __init__(self, action, state, parent):
        self.state = state
        self.action = action
        self.parent = parent
        
    #this method determines the path taken to reach the particular node
    def path(self):
        if self.parent == None:
            return [(self.action, self.state)]
        else:
            return self.parent.path() + [(self.action, self.state)]

    #this method determines whether a node with state s is anywhere in the
    #path of the particular node
    def inPath(self, s):
        if s == self.state:
            return True
        elif self.parent == None:
            return False
        else:
            return self.parent.inPath(s)

#this class is used by a depth-first search algorithm to construct a stack
#(last in, first out)
class Stack:
    def __init__(self):
        self.data = []
    def push(self, item):
        self.data.append(item)
    def pop(self):
        return self.data.pop()
    def isEmpty(self):
        return self.data == []

#this class is used by a breadth-first search algorithm to construct a queue
#(first in, first out)
class Queue:
    def __init__(self):
        self.data = []
    def push(self, item):
        self.data.append(item)
    def pop(self):
        return self.data.pop(0)
    def isEmpty(self):
        return self.data == []

#this general search algorithm takes as input an initial state, a 
#goalTest function for determining if the goal state has been reached, a list
#of possible actions, a successor function for determining what node will be
#reached when performing a particular action, a variable for switching between
#breadth-first and depth-first search, a variable for switching dynamic
#programming on and off, and a variable for determining the maximum number of
#nodes that can be constructed
def search(initialState, goalTest, actions, successor, depthFirst = False, \
           DP = True, maxNodes = 10000):
    if depthFirst:
        agenda = Stack()
    else:
        agenda = Queue()

    #the starting node has no parent and wasn't reached via an action
    startNode = SearchNode(None, initialState, None)
    if goalTest(initialState):
        return startNode.path()
    agenda.push(startNode)
    #with dynamic programming turned on, we ignore paths to states that have
    #already been visited via another path
    if DP: visited = {initialState: True}
    #count is used to make sure the maximum number of nodes isn't breached
    count = 1
    while not agenda.isEmpty() and maxNodes > count:
        #parent is the next node on the agenda to be expanded via possible
        #actions
        parent = agenda.pop()
        newStates = []
        #here we loop through the available actions, determining the resulting
        #state and resulting node
        for a in actions:
            newS = successor(parent.state, a)
            newN = SearchNode(a, newS, parent)
            #if we've reached our goal via this action, the path to it is
            #returned
            if goalTest(newS):
                return newN.path()
            #if the new state is one we can already reach via another action,
            #we ignore this action
            elif newS in newStates:
                pass
            #if the new state is already in the current path or if DP is on
            #and the new state has already been visited on some path, we ignore
            #this action
            elif ((not DP) and parent.inPath(newS)) or (DP and newS in visited):
                pass
            #otherwise we add the resulting node to the agenda of nodes to be
            #expanded
            else:
                count += 1
                if DP: visited[newS] = True
                newStates.append(newS)
                agenda.push(newN)
    return None




#standard class definition for general state machine
class SM:
    #particular machines are initialized with a startState, which this method
    #sets the machine's state to
    def start(self):
        self.state = self.startState
        
    #uses machine's getNextValues method to update the state on input inp and 
    #return output
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o
    
    #some machines include a done method, which returns True when the machine 
    #is finished; here the default method always returns False
    def done(self, state):
        return False
    
    #this method runs the machine (from its start state) on a list of inputs, 
    #until the machine reaches its done state (if ever), returning the list of
    #outputs
    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs if not self.done(self.state)]
    
    #this method runs the machine on n inputs of None, returning the list of 
    #outputs
    def run(self, n = 10):
        return self.transduce([None] * n)
    
    #the default startState is None
    startState = None
    
    #the default getNextValues method uses the machine's getNextState method, 
    #which is useful for defining machines whose next state and output are 
    #identical
    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)



#here we convert the search algorithm into an algorithm that runs on state
#machines, searching for the shortest sequence of legal inputs from the initial
#state of the machine to its goal state (determined by the machine's done
#method)
def smSearch(smToSearch, initialState = None, goalTest = None, maxNodes \
             = 10000, depthFirst = False, DP = True):
    if initialState == None:
        initialState = smToSearch.startState
    if goalTest == None:
        goalTest = smToSearch.done
    return search(initialState, goalTest, smToSearch.legalInputs, \
                  lambda s, a: smToSearch.getNextValues(s, a)[0], \
                  maxNodes = maxNodes, depthFirst = depthFirst, DP = DP)


#here we use object names as indices to determine the positions of the four
#objects in the farmer-goat-wolf-cabbage problem
(farmer, goat, wolf, cabbage) = range(4)

#this function switches the positions of objects
def L_R(input):
    if input == 'L':
        return 'R'
    else:
        return 'L'

#this state machine takes farmer actions as input and outputs the resulting
#positions of the four objects, where the goal is to get all four objects to
#the right side of the river (see README for details)
class FarmerGoatWolfCabbageClass(SM):
    startState = ('L', 'L', 'L', 'L')
    legalInputs = ['takeNone', 'takeGoat', 'takeWolf', 'takeCabbage']
    def getNextValues(self, state, action):
        if action == 'takeNone' and state[goat] != state[cabbage] and \
           state[goat] != state[wolf]:
            nextState = list(state)
            nextState[farmer] = L_R(nextState[farmer])
            nextState = tuple(nextState)
            return (nextState, nextState)
        elif action == 'takeGoat' and state[goat] == state[farmer]:
            nextState = list(state)
            nextState[farmer] = L_R(nextState[farmer])
            nextState[goat] = L_R(nextState[goat])
            nextState = tuple(nextState)
            return (nextState, nextState)
        elif action == 'takeWolf' and state[wolf] == state[farmer] and \
            state[goat] != state[cabbage]:
            nextState = list(state)
            nextState[farmer] = L_R(nextState[farmer])
            nextState[wolf] = L_R(nextState[wolf])
            nextState = tuple(nextState)
            return (nextState, nextState)
        elif action == 'takeCabbage' and state[cabbage] == state[farmer] and \
            state[goat] != state[wolf]:
            nextState = list(state)
            nextState[farmer] = L_R(nextState[farmer])
            nextState[cabbage] = L_R(nextState[cabbage])
            nextState = tuple(nextState)
            return (nextState, nextState)
        else:
            return (state, state)
    def done(self, state):
        return state == ('R', 'R', 'R', 'R')

#here we define a state machine that takes a legal chess move for a knight as
#input and outputs the resulting position of the knight, where the goal is to
#reach the top-right position of the chessboard (see README for details)
class KnightMoves(SM):
    legalInputs = ['ul', 'ur', 'dl', 'dr', 'lu', 'ld', 'ru', 'rd']
    def __init__(self, s):
        self.startState = s
    def getNextValues(self, state, inp):
        if inp == 'ul' and state[0] > 0 and state[1] < 6:
            nextState = (state[0] - 1, state[1] + 2)
            return (nextState, nextState)
        elif inp == 'ur' and state[0] < 7 and state[1] < 6:
            nextState = (state[0] + 1, state[1] + 2)
            return (nextState, nextState)
        elif inp == 'dl' and state[0] > 0 and state[1] > 1:
            nextState = (state[0] - 1, state[1] - 2)
            return (nextState, nextState)
        elif inp == 'dr' and state[0] < 7 and state[1] > 1:
            nextState = (state[0] + 1, state[1] - 2)
            return (nextState, nextState)
        elif inp == 'lu' and state[0] > 1 and state[1] < 7:
            nextState = (state[0] - 2, state[1] + 1)
            return (nextState, nextState)
        elif inp == 'ld' and state[0] > 1 and state[1] > 0:
            nextState = (state[0] - 2, state[1] - 1)
            return (nextState, nextState)
        elif inp == 'ru' and state[0] < 6 and state[1] < 7:
            nextState = (state[0] + 2, state[1] + 1)
            return (nextState, nextState)
        elif inp == 'rd' and state[0] < 6 and state[1] > 0:
            nextState = (state[0] + 2, state[1] - 1)
            return (nextState, nextState)
        else:
            return (state, state)
    def done(self, state):
        return state == (7,7)

#here we store the results of applying the algorithm to the two problems
#in the variables farmer_goat and knight, respectively
farmer_goat = smSearch(FarmerGoatWolfCabbageClass())

knight = smSearch(KnightMoves((0,0)))
