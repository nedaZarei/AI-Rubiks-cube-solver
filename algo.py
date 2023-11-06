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
        ...
    
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