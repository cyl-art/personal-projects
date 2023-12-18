import sys

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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        for variable in self.domains.keys():
            for each in self.domains[variable].copy():
                if variable.length != len(each):
                    self.domains[variable].remove(each)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlaps = self.crossword.overlaps[x, y]
        flag = False
        if overlaps:
            for x_value in self.domains[x].copy():
                match = False
                for y_value in self.domains[y]:
                    if x_value[overlaps[0]] == y_value[overlaps[1]]:
                        match = True
                        break
                #if match:
                    #continue
                if not match:
                    flag = True
                    self.domains[x].remove(x_value)
        return flag

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = []
            for variable in self.crossword.variables:
                #for var in self.crossword.neighbors(variable):
                for var in self.crossword.variables:
                    if variable != var:
                        if self.crossword.overlaps[variable, var] is not None:
                            queue.append((variable, var))

        while len(queue) > 0:
            val = queue.pop(0)
            #x, y = queue[0][0], queue[0][1]
            x, y = val[0], val[1]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == 0:
            return False
        for var in assignment:
            if len(assignment[var]) == 0 or assignment[var] is None:
                return False
        if len(assignment) != len(self.crossword.variables):
            return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check length
        for variable in assignment:
            if variable.length != len(assignment[variable]):
                return False
        # check if distinct
        for index, variable in enumerate(assignment):
            for ind, var in enumerate(assignment):
                if assignment[variable] == assignment[var] and index != ind:
                    return False
        # check constraints
        for variable in assignment:
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    overlaps = self.crossword.overlaps[variable, neighbor]
                    if overlaps:
                        if assignment[variable][overlaps[0]] != assignment[neighbor][overlaps[1]]:
                            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        result = {}
        for var_value in self.domains[var]:
            var_count = 0
            for variable in self.crossword.variables:
                if variable != var and variable not in assignment:
                    overlaps = self.crossword.overlaps[var, variable]
                    if overlaps:
                        for variable_value in self.domains[variable]:
                            if var_value[overlaps[0]] != variable_value[overlaps[1]]:
                                var_count += 1
            result[var_value] = var_count
        res = list(dict(sorted(result.items(), key=lambda x: x[1])).keys())
        return res

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        count = 0
        to_check = []
        for variable in self.crossword.variables:
            if variable not in assignment:
                to_check.append(variable)
        domain_count = {}
        for each in to_check:
            domain_count[each] = len(self.domains[each])
        for i, check in enumerate(domain_count):
            for j, check_1 in enumerate(domain_count):
                if domain_count[check] == domain_count[check_1] and i != j:
                    count += 1
        if count > 0:
            degree_count = {}
            for variable in to_check:
                degree_count[variable] = len(self.crossword.neighbors(variable))
            res = list(dict(sorted(degree_count.items(), key=lambda x: x[1], reverse=True)).keys())
            to_return = res[0]
            return to_return
        else:
            res = list(dict(sorted(domain_count.items(), key=lambda x: x[1])).keys())
            to_return = res[0]
            return to_return

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            #assignment_copy = assignment.copy()
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
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

