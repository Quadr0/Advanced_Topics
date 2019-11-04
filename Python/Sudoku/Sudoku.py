"""
Project 3 - Sudoku Solver
BB&N 2018-19 Advanced Topics in Computer Science
Sudoku.java - source file to solve sudoku puzzles.
See the Powerschool for guidelines and advice.

Name: Daniel Katz
Date: October 2019
"""

# The number parameter is the number that is to be checked that if placed in the specified 
# puzzle[row][column] it is valid given the rules of sudoku.
def is_valid(puzzle, row, column, number):
    # Boolean function that determines if it is allowed to place a number in
    # the given position [row, column]

    # Finds the start index for each third of the rows in the puzzle: 0, 3, or 6.
    # Then constructs an array values ranging from the start index to two more.
    # Then used in a list comprehension to build a 2d array that contains the section
    # of the puzzle that inputed number is in
    section_row_start = (row // 3) * 3
    row_section = range(section_row_start, section_row_start + 3)

    # Same process as above, but constructs a slice object instead of a list.
    section_column_start = (column // 3) * 3
    column_section = slice(section_column_start, section_column_start + 3)

    # Uses the two objects made above in a list comprehension to construct a 2d array
    # of the current ninth of the puzzle. Then uses the 'any' function, to see if any of the
    # rows contain the inputed number.
    section_of_puzzle = [puzzle[x][column_section] for x in row_section]
    section_contains = any(number in x for x in section_of_puzzle)

    # Gets the row in which the number is to be placed and checks if the row contains
    # the inputed number.
    entire_row = puzzle[row]
    row_contains = number in entire_row

    # Constucts a 2d array in which each row is a number for each number in the
    # column in which the inputed is contained in the larger puzzle.
    # Then uses another 'any' function to see if any of rows have the inputed number.
    entie_column = [puzzle[x][column:column+1] for x in range(9)]
    column_contains = any(number in x for x in entie_column)
    
    # If the column, row, or section contains the inputed number return False, because
    # the inputed number can not validly be places in the given spot. Otherwise, return True.
    if section_contains or row_contains or column_contains:
        return False
    else:
        return True


def solve(puzzle, row, column):
    # Function that should be recursively called to solve the sudoku puzzle.
    # This function should return a boolean that says whether the puzzle can be
    # solved using the current configuration

    # If the inputed column is bigger the length of the column, wrap the current index to
    # be the first value on the next row.
    if column > 8:
        row += 1
        column = 0

    # If the current row is bigger than the number of rows, it means that there is no 
    # more puzzle to check and the puzzle is correct.
    if row > 8:
        return True

    # Keeps incrementing the row and column while the given index is already filled by 
    # a given number. Wraps around the puzzle if need be.
    # Returns True if the end of the puzzle is reached.
    while puzzle[row][column] != 0:
        if column >= 8:
            row += 1
            column = 0
        else:
            column += 1

        if row > 8:
            return True

    # Loops through each possible input in a sudoku puzzle: 1-9. Then if the current input
    # is a valid input given the current set up of the puzzle, it sets the number
    # at the current index and recursively continues with the puzzle. 
    # If a recursive call returns False, it resets the set index to 0, and trys the next
    # number. If the is_valid function returns False, it continues trying the other numbers.
    # If none of the numbers work, it returns False. 
    for i in range(1,10):
        if is_valid(puzzle, row, column, i):
            puzzle[row][column] = i
            if solve(puzzle, row, column+1): 
                return True
            else: 
                puzzle[row][column] = 0

    return False

def main():
    # Open the file and read it into a 9x9 list
    filename = "s3.txt" # change this to read other puzzle files
    with open(filename, "r") as file:
        puzzle = []
        for line in file:
            line = [int(x) for x in line.strip().split(" ")]
            puzzle.append(line)

    print("Original puzzle ("+filename+")")
    print_puzzle(puzzle) # print unsolved puzzle

    solved = solve(puzzle, 0, 0) # solve

    if solved:
        print("Solved Puzzle")
        print_puzzle(puzzle) # print solved puzzle

        # Use helper method to see if your solution matches mine
        if check_answer(puzzle, filename):
            print("Correct solution!")
        elif check_answer(puzzle, filename) == False:
            print("Incorrect solution.")
        else:
            print("No associated solution file to check against")
    else:
        # puzzle was unsolvable. all the puzzles provided are solvable,
        # so you should never get here unless your code doesn't work correctly
        print("Unsolvable sudoku (or a broken algorithm)")


##############################
###### HELPER FUNCTIONS ######
##############################
def check_answer(puzzle, filename):
    filename = filename.split(".")
    filename = filename[0]+"_solution.txt"
    try:
        with open(filename, "r") as file:
            puzzle_sol = []
            for line in file:
                line = [int(x) for x in line.strip().split(" ")]
                puzzle_sol.append(line)
            for r in range(len(puzzle_sol)):
                for c in range(len(puzzle_sol[r])):
                    if puzzle[r][c] != puzzle_sol[r][c]:
                        return False
            return True
    except:
        return None

def print_puzzle(puzzle):
    # helper function to print puzzle cleanly
    for i in puzzle:
        for j in i:
            print(str(j) + " ",end="")
        print()

main()
