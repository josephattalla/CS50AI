class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0


    # Made by CS50, modified by Joseph Attalla to remove uneccesary else statement
    # after the if: raise Exception
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node

# Made by CS50, modified by Joseph Attalla to remove uneccesary else statement
# after the if: raise Exception
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")

        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node
