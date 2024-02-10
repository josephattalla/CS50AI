import sys
from copy import deepcopy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)


    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        # iterate through the keys in the domain, each key is an instance of the Variable class
        for variable in self.domains:

            # iterate through the words in the variables domain
            for word in list(self.domains[variable]):

                # if the length of the word doesn't equal the length of the variable (given by the length attribute in the Variable class), remove it from the variables domain
                if len(word) != variable.length:
                    self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revision = False

        # loop through all overlap keys (2 variables represented as (v1, v2))
        for overlap in self.crossword.overlaps:

            # if the overlap is of the variables given in the parameter
            if overlap == (x, y):

                # if there is an overlap
                if self.crossword.overlaps[overlap]:
                    
                    # loop through the words in the domain of x and y, if there is a word in x that doesn't overlap with any word in y, remove it from the domain of x
                    for w1 in deepcopy(self.domains[x]):
                        valid = False
                        for w2 in self.domains[y]:
                            if w1[self.crossword.overlaps[x, y][0]] == w2[self.crossword.overlaps[x, y][1]]:
                                valid = True
                        if (not valid):
                            self.domains[x].remove(w1)
                            revision = True

        return revision


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # not given an initial list of arcs, begin with all arcs
        if arcs == None:
            arcs = list(self.crossword.overlaps)

        # continuously loop until all arcs are done
        while len(arcs) != 0:
            
            # dequeue variables
            x, y = arcs.pop()

            # make it arc consistent
            if self.revise(x, y):

                # if the domain left is 0, a solution is not possible, return False
                if len(self.domains[x]) == 0:
                    return False

                # because of the revision, there could now be other arcs that need to be done, enqueue them
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.insert(0, (z, x))
        
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        if len(assignment) != len(self.crossword.variables):
            return False

        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        # iterate through the variables in the assignment
        for v1 in assignment:

            # if the length of the assigned word is different from the length of the variable return False
            if len(assignment[v1]) != v1.length:
                return False
                
            # get another variable in assignment
            for v2 in assignment:   

                # if on the same variable, continue             
                if v1 == v2:
                    continue

                # if the length of the assignment is different from the variables length, return False
                if len(assignment[v2]) != v2.length:
                    return False

                # if the variable have the same assignment, return False
                if assignment[v1] == assignment[v2]:
                    return False

                # loop through the overlaps in the crossword
                for overlaps in self.crossword.overlaps:

                    # if the overlap is of the variables we are on
                    if overlaps == (v1, v2):

                        # if there is an overlap between these variables
                        if self.crossword.overlaps[overlaps]:

                            # if the the character where they overlap is not the same, return False
                            if assignment[v1][self.crossword.overlaps[overlaps][0]] != assignment[v2][self.crossword.overlaps[overlaps][1]]:
                                return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        counts = list()

        # loop through the values in the domain of the variable
        for value in self.domains[var]:

            # keep count of how many values the current domain value rules out for the neighbors of the variable
            count = 0

            # loop through the neighbors of the variable
            for neighbor in self.crossword.neighbors(var):

                # if neighbor is already assigned, continue
                if neighbor in assignment:
                    continue

                # loop through the overlaps in the crossword
                for overlaps in self.crossword.overlaps:

                    # if the overlap is var and neighbor
                    if overlaps == (var, neighbor):

                        # if there is an overlap between these variables
                        if self.crossword.overlaps[overlaps]:

                            # loop through the domain values of the neighbor
                            for value_2 in self.domains[neighbor]:

                                # if the the character where they overlap is not the same, add to the count
                                if value[self.crossword.overlaps[overlaps][0]] != value_2[self.crossword.overlaps[overlaps][1]]:
                                    count += 1
                
                counts.append(count)
            
        # return the sorted list of values
        combined = list(zip(self.domains[var], counts))
        sorted_combined = sorted(combined, key=lambda x: x[1])
        sorted_values = [pair[0] for pair in sorted_combined]
        return sorted_values


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        # dictionary of the remianing variables and their number of domain values
        remaining = {variable: len(self.domains[variable]) for variable in self.crossword.variables if variable not in assignment}

        # if the values of each variable is not the same
        if (not all(i == list(remaining.values())[0] for i in list(remaining.values()))):

            # setting arbritrary high number for the variable to find the variable with least remaining domain values
            min_num = 99999

            # looping through the variables remaining
            for variable in remaining:

                # if the variables value is less than the minimum found so far, set the minimum value to that value and store that variable
                if remaining[variable] < min_num:
                    min_num = remaining[variable]
                    min_var = variable
        
            return min_var
        
        # if they all have the same number of domain value remaining, use degree heuristic, which chooses the variable with the highest number of neighbors
        remaining = {variable: len(self.crossword.neighbors(variable)) for variable in self.crossword.variables if variable not in assignment}

        # setting arbritrary max number to compare
        max_num = -1

        # looping through the variables remaining
        for variable in remaining:

            # if the variables value is greater than the max found so far, set the max value to that value and store that variable
            if remaining[variable] > max_num:
                max_num = remaining[variable]
                max_var = variable
    
        return max_var
        



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        # if assignment complete, return it
        if self.assignment_complete(assignment):
            return assignment
        
        # select variable
        var = self.select_unassigned_variable(assignment)

        # loop through the possible values for this variable
        for value in self.domains[var]:

            # create a copy of assignment and see if the assignment will work
            assignment_ = deepcopy(assignment)
            assignment_[var] = value

            if self.consistent(assignment_):
                
                # recursively call backtrack with this new assignment
                result = self.backtrack(assignment_)

                # if the value works, return result
                if result != None:
                    return result

        return None                
                



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)


    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
