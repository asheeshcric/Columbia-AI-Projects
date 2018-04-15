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
        # print('allowed_operations - ', allowed_operations)
        for operation in allowed_operations:
            new_state = list(self.state)
            zero_position = tuple(self.state).index(0)
            if operation == Operations.up:
                new_zero_postion = zero_position - 3
            elif operation == Operations.down:
                new_zero_postion = zero_position + 3
            elif operation == Operations.left:
                new_zero_postion = zero_position - 1
            elif operation == Operations.right:
                new_zero_postion = zero_position + 1

            new_state[zero_position] = new_state[new_zero_postion]
            new_state[new_zero_postion] = 0
            available_neighbors.append(State(tuple(new_state), self, operation, self.cost_of_path + 1))

        return available_neighbors


def write_to_file(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage):
    output = open('output.txt', 'w')
    output.write('path_to_goal: {}\n\n'.format(path_to_goal))
    output.write('cost_of_path: {}\n\n'.format(cost_of_path))
    output.write('nodes_expanded: {}\n\n'.format(nodes_expanded))
    output.write('search_depth: {}\n\n'.format(search_depth))
    output.write('max_search_depth: {}\n\n'.format(max_search_depth))
    output.write('running_time: {} seconds\n\n'.format(running_time))
    output.write('max_ram_usage: {}'.format(max_ram_usage))
    output.close()



def bfs(initial_state):
    start_time = time.clock()

    frontier = deque([initial_state])
    explored = set()

    nodes_expanded = 0
    max_search_depth = -1

    while frontier:
        state = frontier.popleft()
        state_being_checked = state.state
        explored.add(state.state)

        if state.check_goal_state():
            path_to_goal = []
            current_state = state

            while current_state.parent_state:
                path_to_goal.append(current_state.operation_on_parent)
                current_state = current_state.parent_state

            path_to_goal = path_to_goal[::-1]   # Reversing the order of path list
            cost_of_path = len(path_to_goal)
            search_depth = state.cost_of_path
            running_time = time.clock() - start_time
            import resource
            max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            write_to_file(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage)
            return
            # Calculate ram usage and write output to file

        # The output cannot be derived from the current node. So, it should be expanded
        nodes_expanded += 1

        for neighbor in state.neighbors():
            neighbor_being_checked = neighbor.state
            if neighbor.state not in explored:
                frontier.append(neighbor)
                explored.add(neighbor.state)
                max_search_depth = max(max_search_depth, neighbor.cost_of_path)

    print("The problem did not result to a solution!")




def dfs(initial_state):
    start_time = time.clock()

    frontier = deque([initial_state])
    explored = set()

    nodes_expanded = 0
    max_search_depth = -1

    while frontier:
        state = frontier.pop()
        state_being_checked = state.state
        explored.add(state.state)

        if state.check_goal_state():
            path_to_goal = []
            current_state = state

            while current_state.parent_state:
                path_to_goal.append(current_state.operation_on_parent)
                current_state = current_state.parent_state

            path_to_goal = path_to_goal[::-1]  # Reversing the order of path list
            cost_of_path = len(path_to_goal)
            search_depth = state.cost_of_path
            running_time = time.clock() - start_time
            import resource
            max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            write_to_file(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time,
                          max_ram_usage)
            return
            # Calculate ram usage and write output to file

        # The output cannot be derived from the current node. So, it should be expanded
        nodes_expanded += 1

        for neighbor in state.neighbors()[::-1]:        # Reversing the list of neighbors so that popping results in UDLR
            neighbor_being_checked = neighbor.state
            if neighbor.state not in explored:
                frontier.append(neighbor)
                explored.add(neighbor.state)
                max_search_depth = max(max_search_depth, neighbor.cost_of_path)

    print("The given problem has no solution!!!")

def ast(initial_state):
    pass

if __name__ == '__main__':
    input_arguments = sys.argv[1:]
    # print((input_arguments))
    search_type = input_arguments[0]
    input_state = input_arguments[1]
    initial_state = tuple((int(x) for x in input_state.split(',')))    # Using tuple to represent a state
    goal_state = (0,1,2,3,4,5,6,7,8)
    state = State(state=initial_state, parent_state=None, operation=None, cost_of_path=0)
    if search_type == 'bfs':
        bfs(state)
    elif search_type == 'dfs':
        dfs(state)
    elif search_type == 'ast':
        ast(state)

