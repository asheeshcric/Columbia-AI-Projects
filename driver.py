import sys
from collections import deque
import time

class Operations:
    up = 'Up'
    down = 'Down'
    right = 'Right'
    left = 'Left'

class State:

    def __init__(self, state, parent_state, operation, cost_of_path):
        self.state = state
        self.parent_state = parent_state
        self.operation_on_parent = operation
        self.cost_of_path = cost_of_path

    def check_goal_state(self):
        return self.state == goal_state

    def get_allowed_operations(self):
        allowed_operations = []
        zero_position = tuple(self.state).index(0)
        if zero_position > 2:
            allowed_operations.append(Operations.up)
        if zero_position < 6:
            allowed_operations.append(Operations.down)
        if zero_position not in (0,3,6):
            allowed_operations.append(Operations.left)
        if zero_position not in (2,5,8):
            allowed_operations.append(Operations.right)

        return allowed_operations

    def neighbors(self):
        available_neighbors = []
        allowed_operations = self.get_allowed_operations()
        print(allowed_operations)

        for operation in allowed_operations:
            pass



class Solver:
    pass



def bfs(initial_state):
    start_time = time.clock()

    frontier = deque([initial_state])
    explored = set()

    nodes_expanded = 0
    # Will come back to this later
    max_fringe_size = -1
    max_search_depth = -1

    while frontier:
        state = frontier.popleft()
        explored.add(state)

        if state.check_goal_state():
            path_to_goal = []
            current_state = state

            while current_state.parent_state:
                path_to_goal.append(current_state.operation_on_parent)
                current_state = current_state.parent_state

            path_to_goal = path_to_goal[::-1]   # Reversing the order of path list
            cost_of_path = len(path_to_goal)
            fringe_size = len(frontier)
            search_depth = state.cost_of_path
            running_time = time.clock() - start_time

            # Calculate ram usage and write output to file

        # The output cannot be derived from the current node. So, it should be expanded
        nodes_expanded += 1

        for neighbor in state.neighbors():
            if not neighbor in explored:
                frontier.append(neighbor)
                explored.add(neighbor)
                max_fringe_size = max(max_fringe_size, len(frontier))
                max_search_depth = max(max_search_depth, neighbor.cost_of_path)

    print("The given problem has no solution!!!")




def dfs(state):
    pass

def ast(state):
    pass

if __name__ == '__main__':
    input_arguments = sys.argv[1:]
    # print(type(input_arguments))
    search_type = input_arguments[0]
    input_state = input_arguments[1]
    initial_state = (int(x) for x in input_state.split(','))    # Using tuple to represent a state
    goal_state = (0,1,2,3,4,5,6,7,8)
    state = State(initial_state, None, None, 0)

    if search_type == 'bfs':
        bfs(state)
    elif search_type == 'dfs':
        dfs(state)
    elif search_type == 'ast':
        ast(state)

