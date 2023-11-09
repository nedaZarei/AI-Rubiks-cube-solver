import numpy as np
from location import next_location, solved_location
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
    if method == 'Random':
        return list(np.random.randint(1, 12+1, 10))
    
    elif method == 'IDS-DFS':
        return idfs(init_state)

    elif method == 'A*':
        return aStar(init_state,init_location)

    elif method == 'BiBFS':
        return bi_bfs(init_state)
    
    else:
        return []  
    
def idfs(startState):
       depth_limit = 1
       expanded_nodes = 0
       while True:
            explored = set()
            actions = []
            frontier = util.Stack()

            state_with_layer_num = (startState, 0)
            frontier.push((state_with_layer_num, actions))

            while not frontier.isEmpty():
                (curr_state, layer), actions = frontier.pop()
                expanded_nodes += 1
                
                if np.array_equiv(curr_state,solved_state()):
                    print_info(explored, actions, expanded_nodes)
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

def print_info(explored, actions, expanded_nodes):
    print("depth of answer:")
    print(len(actions))
    print("number of expanded:")
    print(expanded_nodes)
    print("number of explored nodes:")
    print(len(explored))   

def aStar(startState,startLocation):
    #search the node that has the lowest combined cost and heuristic first.
    explored = dict() # state -> cost
    actions = []
    frontier = util.PriorityQueue()
    expanded_nodes = 0
    #cost = heuristic + cost from init state to current state -> -priority
    frontier.push( (startState, startLocation, heuristic(startLocation)+len(actions), actions), heuristic(startLocation)+len(actions) )

    while not frontier.isEmpty():
        (curr_state, curr_location, curr_cost, actions) = frontier.pop()
        expanded_nodes += 1
        #pop in util.priorityQueue -> heappop : Pop the smallest item off the heap, maintaining the heap invariant.

        if np.array_equiv(curr_state,solved_state()):
            print_info(explored, actions, expanded_nodes)
            return actions
        elif to_tuple(curr_state) not in explored:
            explored[to_tuple(curr_state)] = curr_cost
        
            for i in range(12):
                nextState = next_state(curr_state, i+1)
                nextLocation = next_location(curr_location, i+1)
                nextCost = heuristic(nextLocation) + len(actions)+1

                if to_tuple(nextState) not in explored:
                  frontier.push( ((nextState,nextLocation,nextCost, actions+[i+1])), nextCost)
                else:
                #if this state was already explored, check the cost, if old one is more than new state, add new to frontier
                    old_cost = explored[to_tuple(nextState)]
                     # If item already in priority queue with higher priority, update its priority and rebuild the heap.
                    if(nextCost < old_cost):
                        #update in util.priorityQueue:
                        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
                        # If item already in priority queue with equal or lower priority, do nothing.
                        # If item not in priority queue, do the same thing as self.push.
                       frontier.update(((nextState,nextLocation,nextCost, actions+[i+1])), nextCost)   

    return []

def heuristic(location):
    total = 0
    solved_xyz = { 1:[0,0,0] , 2:[0,0,1], 3:[0,1,0], 4:[0,1,1]
                   ,5:[1,0,0] , 6:[1,0,1], 7:[1,1,0], 8:[1,1,1]}
    for i in range(2):
        for j in range(2):
            for k in range(2):
              curr_value = location[i,j,k] #the number assign to each little cube
              #getting little cube's number's (curr_value) location(x,y,z) in the solved cube
              xyz = solved_xyz.get(curr_value)          
              total += (abs(xyz[0]-i) + abs(xyz[1]-j) + abs(xyz[2]-k))

    return total/4

def bi_bfs(startState):
    frontier1 = util.Queue() #starts from scrambeled state
    frontier2 = util.Queue() #starts from goal state
    explored1 = dict()
    explored2 = dict()
    actions1 = []
    actions2 = []
    frontier1.push((startState, actions1))
    frontier2.push((solved_state(), actions2))
    expanded_nodes = 0

    while not frontier1.isEmpty() or not frontier2.isEmpty():
        curr_state1, actions1 = frontier1.pop()
        curr_state2, actions2 = frontier2.pop()
        expanded_nodes += 2

        if to_tuple(curr_state1) in explored2: #curr_state1 is the similar state in two bfs searches
                actions =  merge_actions(actions1, explored2[to_tuple(curr_state1)])
                print_info({**explored1, **explored2}, actions , expanded_nodes)
                return actions
        
        if to_tuple(curr_state2) in explored1: #curr_state2 is the similar state in two bfs searches
                actions =  merge_actions(explored1[to_tuple(curr_state2)], actions2)
                print_info({**explored1, **explored2}, actions , expanded_nodes)
                return actions

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
    # action_dict = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
    #                7: 'q', 8: 'w', 9: 'e', 10: 'r', 11: 't', 12: 'y'}
    #we have to change scrambling actions in actions2 array, to their corespondant solving actions
    for i in range(len(actions2)):
        if actions2[i] <= 6:
            actions2[i] += 6
        else:
            actions2[i] -= 6    

    return actions1 + actions2
