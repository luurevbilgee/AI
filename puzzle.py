from collections import deque
import time

class PuzzleGame:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def actions(self, state):
        # Determine the possible actions based on the current state
        actions = []
        empty_index = state.index(0)  # Find the index of the empty space
        
        # Move left if possible
        if empty_index % 3 > 0:
            actions.append('left')
        
        # Move right if possible
        if empty_index % 3 < 2:
            actions.append('right')
        
        # Move up if possible
        if empty_index >= 3:
            actions.append('up')
        
        # Move down if possible
        if empty_index < 6:
            actions.append('down')
        
        return actions
    
    def result(self, state, action):
        # Generate the new state by performing the given action on the current state
        new_state = list(state)
        empty_index = new_state.index(0)  # Find the index of the empty space
        
        if action == 'left':
            new_state[empty_index], new_state[empty_index - 1] = new_state[empty_index - 1], new_state[empty_index]
        elif action == 'right':
            new_state[empty_index], new_state[empty_index + 1] = new_state[empty_index + 1], new_state[empty_index]
        elif action == 'up':
            new_state[empty_index], new_state[empty_index - 3] = new_state[empty_index - 3], new_state[empty_index]
        elif action == 'down':
            new_state[empty_index], new_state[empty_index + 3] = new_state[empty_index + 3], new_state[empty_index]
        
        return tuple(new_state)
    
    def goal_test(self, state):
        # Check if the current state matches the goal state
        return state == self.goal_state
    
    def path_cost(self, c, state1, action, state2):
        # Return the cumulative path cost
        return c + 1
    
    def value(self, state):
        # Heuristic function (optional)
        # Return a value that represents the desirability of a state
        # The lower the value, the closer it is to the goal state
        # This can be used to guide the search algorithm
        return sum([1 for i in range(8) if state[i] != i + 1])  # Counts the number of misplaced tiles

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
    
    def __repr__(self):
        return f"<Node {self.state}>"
    
    def __lt__(self, node):
        return self.state < node.state
    
    def expand(self, problem):
        return [self.child_node(problem, action) for action in problem.actions(self.state)]
    
    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node
    
    def solution(self):
        return [node.action for node in self.path()[1:]]
    
    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state
        return False

    def __hash__(self):
        return hash(self.state)

def depth_first_search(problem, depth_limit=100):
    frontier = [Node(problem.initial_state)]  # Stack
    explored = set()
    
    while frontier:
        node = frontier.pop()
        
        if problem.goal_test(node.state):
            return node
        
        explored.add(node.state)
        
        if node.depth < depth_limit:
            for child_node in node.expand(problem):
                if child_node.state not in explored and child_node not in frontier:
                    frontier.append(child_node)
    
    return None
def print_puzzle_state(state):
    for i in range(3):
        row = state[i * 3: (i + 1) * 3]
        print("|".join(map(str, row)))

# Define the initial state and goal state
initial_state = (1, 2, 3, 0, 4, 6, 7, 5, 8)
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Create an instance of PuzzleGame
game = PuzzleGame(initial_state, goal_state)

# Execute DFS to find the solution
start_time = time.time()

solution_node = depth_first_search(game)
end_time = time.time()
# Print the solution path
if solution_node:
    print("Solution found!")
    print("Path to the solution:", [node.action for node in solution_node.path()[1:]])
    # print("Time taken:", end_time - start_time, "seconds")
    for step, node in enumerate(solution_node.path()):
        print(f"Step {step + 1}:")
        print_puzzle_state(node.state)
        print()
    print("Number of nodes expanded:", len(solution_node.path()) - 1)
    print("Time taken:", end_time - start_time, "seconds")
else:
    print("No solution found.")
