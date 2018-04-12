import sys
import queue

class State:

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.frontier = queue.Queue(initial_state)


class Solver:
    pass

if __name__ == '__main__':
    input_arguments = sys.argv[1:]
    # print(type(input_arguments))
    search_type = input_arguments[0]
    input_state = input_arguments[1]
    input_state = input_state.split(',')
    initial_state = set()
    for number in input_state:
        initial_state.add(int(number))
    x = State(initial_state)

