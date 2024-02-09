import itertools
import random
from copy import deepcopy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        # if the number of cells equals the count of mines in the cells, then all the cells are mines
        if len(self.cells) == self.count:
            return self.cells
        
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        # if the count is 0, then all the cells are safe
        if self.count == 0:
            return self.cells
        
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        # if the cell is in the knowledge base we have, remove it and remove 1 from the count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        # if the cell is in the knowledge base we have, remove it from the sentence
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # add the cell to moves made and mark it safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # add cell neighbors to knowledge base
        neighbors = set()
        neighbors_count = count
        for row in range(cell[0]-1, cell[0]+2):
            if row >= self.height or row < 0:
                continue
            for col in range(cell[1]-1, cell[1]+2):
                if col >= self.width or col < 0:
                    continue
                if (row, col) == cell:
                    continue
                if (row, col) in self.safes:
                    continue
                if (row, col) in self.mines:
                    neighbors_count -= 1
                    continue
                neighbors.add((row, col))
        new_sentence = Sentence(neighbors, neighbors_count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)
                

        # deep copy of sentences, to allow looping through it and changing it's elements
        knowledge_ = deepcopy(self.knowledge)

        # loop through the sentences in knowledge base and add any new safe or mine cells to knowledge base
        for sentence in knowledge_:

            for safe in sentence.known_safes():
                if safe not in self.safes:
                    self.mark_safe(safe)

            for mine in sentence.known_mines():
                if mine not in self.mines:
                    self.mark_mine(mine)

        # updated copy of the knowledge base
        knowledge_ = deepcopy(self.knowledge)

        # inferring new sentences using subset formula: set2 - set1 = count2 - count 1
        for s1 in knowledge_:
            for s2 in knowledge_:
                # if on the same sentence, continue
                if s1.cells is s2.cells:
                    continue
                # if s1 is a subset of s2, we can infer a new sentence: set2 - set1 = count2 - count1    
                if s1.cells.issubset(s2.cells):
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count
                    if len(new_cells) > 0 and new_count > 0:
                        new_sentence = Sentence(s2.cells - s1.cells, s2.count - s1.count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
        
        # updated copy of knowledge base
        knowledge_ = deepcopy(self.knowledge)
        # loop through the sentences in knowledge base and add any new safe or mine cells to knowledge base
        for sentence in knowledge_:
            for safe in sentence.known_safes():
                if safe not in self.safes:
                    self.mark_safe(safe)
            for mine in sentence.known_mines():
                if mine not in self.mines:
                    self.mark_mine(mine)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        # loop throgh known safe cells, if it is not a move already made, return it
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # store possible moves in list
        possible_moves = list()
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.mines and (row, col) not in self.moves_made:
                    possible_moves.append((row, col))
        
        # if there are no possible moves return none
        if len(possible_moves) == 0:
            return None
        # return a random move
        return random.choice(possible_moves)