import numpy as np
from state import next_state, solved_state
from textures import util


def solve(init_state, init_location, method):
    """
    Solves the given Rubik's cube using the selected search algorithm.
 
    Args:
        init_state (numpy.array): Initial curr_state of the Rubik's cube.
        init_location (numpy.array): Initial location of the little cubes.
        method (str): Name of the search algorithm.
 
    Returns:
        list: The sequence of actions needed to solve the Rubik's cube.
    """

    # instructions and hints:
    # 1. use 'solved_state()' to obtain the goal curr_state.
    # 2. use 'next_state()' to obtain the next curr_state when taking an action .
    # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
    # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.
  
    if method == 'Random':
        return list(np.random.randint(1, 12+1, 10))
    
    elif method == 'IDS-DFS':
        return idfs(init_state)

    elif method == 'A*':
         ...

    elif method == 'BiBFS':
        return bi_bfs(init_state)
    
    else:
        return []
    
    
def idfs(startState):
       depth_limit = 1
       while True:
            explored = set()
            actions = []
            frontier = util.Stack()

            state_with_layer_num = (startState, 0)
            frontier.push((state_with_layer_num, actions))

            while not frontier.isEmpty():
                (curr_state, layer), actions = frontier.pop()
                
                if np.array_equiv(curr_state,solved_state()):
                    return actions
                elif layer == depth_limit:
                    continue
                elif to_tuple(curr_state) not in explored:
                    explored.add(to_tuple(curr_state))

                    for i in range(12):
                         nextState = next_state(curr_state,i+1)
                         if to_tuple(nextState) not in explored:
                            frontier.push(((nextState, layer + 1), actions+[i+1]))

            depth_limit += 1

def to_tuple(array):
    return tuple(map(tuple, array))      

def bi_bfs(startState):
    frontier1 = util.Queue() #starts from scrambeled state
    frontier2 = util.Queue() #starts from goal state
    explored1 = dict()
    explored2 = dict()
    actions1 = []
    actions2= []
    frontier1.push((startState, actions1))
    frontier2.push((solved_state(), actions2))

    while not frontier1.isEmpty() or not frontier2.isEmpty():
        curr_state1, actions1 = frontier1.pop()
        curr_state2, actions2 = frontier2.pop()

        if np.array_equiv(curr_state1,solved_state) and np.array_equiv(curr_state2,solved_state):
            return []
        if to_tuple(curr_state1) in explored2: #curr_state1 is the similar state in two bfs searches
                return merge_actions(actions1, explored2[to_tuple(curr_state1)])
        
        if to_tuple(curr_state2) in explored1: #curr_state2 is the similar state in two bfs searches
                return merge_actions(explored1[to_tuple(curr_state2)], actions2)

        if  to_tuple(curr_state1) not in explored1:
            explored1[to_tuple(curr_state1)] = actions1
            for i in range(12):
                nextState1 = next_state(curr_state1,i+1)
                if to_tuple(nextState1) not in explored1:
                    frontier1.push((nextState1, actions1+[i+1]))
            
        if to_tuple(curr_state2) not in explored2:
            explored2[to_tuple(curr_state2)] = actions2
            for i in range(12):
                nextState2 = next_state(curr_state2,i+1)
                if to_tuple(nextState2) not in explored2:
                    frontier2.push((nextState2, actions2+[i+1]))
                      
    return []  

def merge_actions(actions1, actions2):
    actions2 = actions2[::-1] #reversing actions form goal state to the similar state we found
    for i in range(len(actions2)):
        if actions2[i] <= 6:
            actions2[i] += 6
        else:
            actions2[i] -= 6    

    return actions1 + actions2
