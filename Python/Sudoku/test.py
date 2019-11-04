"""
Project 3 - Sudoku Solver
BB&N 2018-19 Advanced Topics in Computer Science
Sudoku.java - source file to solve sudoku puzzles.
See the Powerschool for guidelines and advice.

Name:
Date: October 2018
"""

def is_valid(puzzle, row, column, number):
    # Boolean function that determines if it is allowed to place a number in
    # the given position [row, column]
    if(row <= 2):
        row_section = [0,1,2]
    elif(row >= 6):
        row_section = [6,7,8]
    else:
        row_section = [3,4,5]

    if(column <= 2):
        column_section = slice(0,3,1)
    elif(column >= 6):
        column_section = slice(6,9,1)
    else:
        column_section = slice(3,6,1)

    section_of_puzzle = [puzzle[x][column_section] for x in row_section]
    section_contains = any(number in x for x in section_of_puzzle)

    entire_row = puzzle[row:row+1]
    row_contains = number in entire_row

    entie_column = [puzzle[x:x+1][column:column+1] for x in range(8)]
    column_contains = any(number in x for x in entie_column)

    
    if(section_contains or row_contains or column_contains):
        return False
    else:
        return True


def solve(puzzle, row, column):
    # Function that should be recursively called to solve the sudoku puzzle.
    # This function should return a boolean that says whether the puzzle can be
    # solved using the current configuration

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

    print(str(is_valid(puzzle,2,0,3 ) ) )


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
