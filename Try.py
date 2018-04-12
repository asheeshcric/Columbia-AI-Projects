import sys
import queue

class Operations:

    def __init__(self):
        up = 'Up'
        down = 'Down'
        right = 'Right'
        left = 'Left'

class State:

    def __init__(self, state, parent_state, operation, path_cost):
        self.state = state
        self.parent_state = parent_state
        self.operation_on_parent = operation
        self.path_cost = path_cost


class Solver:
    pass


def bfs(state):
    pass

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

