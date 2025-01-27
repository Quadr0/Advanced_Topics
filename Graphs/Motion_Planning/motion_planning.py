# Graphics library that allows to easily draw layout of all nodes and obstacles.
from graphics import *

from math import sqrt
from random import randint

# Node class that stores values about its x position(j), y position(i),
# neighboring nodes(con_list), predecessor node(pred), 
# and distance from the start node(dist).
class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.con_list = list()
        self.pred = None
        self.dist = -1

# Global variables that keep info about the start point, end point, and board.
board = list()
start_point = [0,0]
end_point = [99,99]

# Function that prompts user enter user to the top right, and bottom left corner
# of an obstacle. The points should be entered in a y,x format. Error
# checking to make sure the obstacle follows the instructions and does not
# take the place of the start or end point.
def get_obstacles(obstacles):
    while(True):
        print('\nIf you are done entering obstacles, enter "stop" for the first prompt.')
        point1 = input('Enter the top right corner of the obstacle in the format "y,x": ')
        point1 = point1.strip().lower().replace(" ", "")
        if point1 == 'stop' : break
        point1 = [int(i) for i in point1.split(',')]

        point2 = input('Enter the bottom left corner of the obstacle in the format "y,x": ')
        point2 = point2.strip().replace(" ", "")
        point2 = [int(i) for i in point2.split(',')]

        print('\n')

        if point1[0] > point2[0] or point1[1] > point2[1]:
            print('The obstacle you entered does not follow the given instruction.')
            continue

        if point1[0] <= start_point[0] and point2[0] >= start_point[0] and point1[1] <= start_point[1] and point2[1] >= start_point[1]:
            print('The obstacle would have blocked the start point. Enter a different obstacle or change the start point.')
            continue

        if point1[0] <= end_point[0] and point2[0] >= end_point[0] and point1[1] <= end_point[1] and point2[1] >= end_point[1]:
            print('The obstacle would have blocked the end point. Enter a different obstacle or change the end point.')
            continue

        obstacles.append([point1, point2])

# Function that randomly generates obstacles based on a few restrictions.
def random_obstacles(obstacles):
    num_obs = int(input('Enter the number of obstacle(s) you want to randomly generate, between 1 and 20: '))
    while num_obs not in range(1,21):
        num_obs = int(input('Enter the number of obstacle(s) you want to randomly generate, between 1 and 20: '))

    max_hor = int(input('Enter the max horizontal distance of an obstacle, between 1 and 30: '))
    while max_hor not in range(1,31):
        max_hor = int(input('Enter the max horizontal distance of an obstacle, between 1 and 30: '))

    max_vert = int(input('Enter the max vertical distance of an obstacle, between 1 and 30: '))
    while max_vert not in range(1,31):
        max_vert = int(input('Enter the max vertical distance of an obstacle, between 1 and 30: '))

    for _ in range(num_obs):
        while True:
            # Top right point
            point1 = list()
            # Bottom left point
            point2 = list()

            # Generate the actual vertical and horizontal lengths of the obstacles.
            hor_len = randint(0, max_hor-1)
            vert_len = randint(0, max_vert-1)

            # Make the top right point.
            point1.append(randint(0, 99 - vert_len))
            point1.append(randint(0, 99 - hor_len))

            # Make the bottom left point.
            point2.append(point1[0] + vert_len)
            point2.append(point1[1] + hor_len)

            # Check if the obstacle would block the start or end point, and if
            # it does, generate a different obstacle.
            if point1[0] <= start_point[0] and point2[0] >= start_point[0] and point1[1] <= start_point[1] and point2[1] >= start_point[1]:
                continue

            if point1[0] <= end_point[0] and point2[0] >= end_point[0] and point1[1] <= end_point[1] and point2[1] >= end_point[1]:
                continue

            # If the obstacle is fine, append it to obstacles list, and 
            # generate the next one.
            obstacles.append([point1,point2]) 
            break

# Go through the obstacles in the obstacles list, and put None in the place in
# the board where they would be.
def change_obstacles(obstacles):
    global board

    for obs in obstacles:
        point1 = obs[0]
        point2 = obs[1]
        startx, starty = point1
        endx, endy = point2

        for i in range(startx, endx+1):
            for j in range(starty, endy+1):
                board[i][j] = None

# Change the start point using user input, while also error checking.
def change_start():
    global start_point

    start_point = input('enter the starting coordinates in the format "y,x": ').strip().replace(" ", "")
    start_point = [int(i) for i in start_point.split(',')]
    while(board[start_point[1]][start_point[0]] == None or sum([1 for i in start_point if i in range(100)]) < 2):
        start_point = input('The start point you entered is invalid or in an obstacle, enter a valid start point: ')
        start_point = [int(i) for i in start_point.split(',')]
    print('\n')

# Change the end point using user input, while also error checking.
def change_end():
    global end_point

    end_point = input('enter the ending coordinates in the format "y,x": ').strip().replace(" ", "")
    end_point = [int(i) for i in end_point.split(',')]
    while(board[end_point[1]][end_point[0]] is None):
        end_point = input('your point is in an obstace, enter a valid end point: ')
        end_point = [int(i) for i in end_point.split(',')]
    print('\n')

# Go through every point on the board, and if it is a Node, link it to all of
# its neighbors. Set the edge value to one it it is a "straight" connection
# or the root of 2 if it is a diagnal connection.
def init_board():
    for row in range(len(board)):
        for col in range(len(board[row])):
            if isinstance(board[row][col], Node):
                connect_node(row, col, row+1, col, 1)
                connect_node(row, col, row-1, col, 1)
                connect_node(row, col, row, col+1, 1)
                connect_node(row, col, row, col-1, 1)

                connect_node(row, col, row+1, col+1, sqrt(2))
                connect_node(row, col, row-1, col-1, sqrt(2))
                connect_node(row, col, row-1, col+1, sqrt(2))
                connect_node(row, col, row+1, col-1, sqrt(2))


# Check if a connection between nodes is possibe, and if it is, make it
# with the specified value for the edge.
def connect_node(i, j, i_change, j_change, value):
    cur_node = board[i][j]
    rows = len(board)
    columns = len(board[0])

    if i_change >= rows or i_change < 0 or j_change >= columns or j_change < 0 or board[i_change][j_change] == None:
        return

    cur_node.con_list.append([board[i_change][j_change],value])

# Function that finds the shortest path between two points using a modified
# dijkstra's algorithm. Return None if there is no connecting path, or the 
# end node if there is one. Also updates each node dist to reflect the distance
# from the starting node, and upates the predecessor to reflect the predecessor
# node that it came from. Uses a "fake" priority queue to achieve this by
# having the diagnol connections come before the "straight" one.
def find_path():
    cur_node = board[start_point[0]][start_point[1]]
    cur_node.dist = 0
    qu = [cur_node]
    
    while len(qu) > 0:
        cur_node = qu.pop(0)
        if cur_node.i == end_point[0] and cur_node.j == end_point[1]:
            return cur_node

        for neighbor, value in cur_node.con_list:
            if neighbor.pred == None:
                qu.append(neighbor)

            if neighbor.dist == -1 or cur_node.dist + value < neighbor.dist:
                neighbor.dist = cur_node.dist + value
                neighbor.pred = cur_node

    return None

# Function that uses the graphics library to display a graphical representation
# of the board. Each node or part of obstacle is represented as a circle with
# a different color filling. The key to each color is printed in the console
# when the graphic pops up.
def draw_graph(end_node):
    print('\nThe pink circle is the starting node.')
    print('The purple circle is the ending node.')
    print('If there is a red circle, it means the start and end nodes are on the same point.')
    print('The green circles are the connecting nodes.')
    print('The black circles are the obstacles.')
    print('The yellow circles are unused nodes.')
    print('Click on the popup to exit it!!!')

    # Gets a list from the start node to the end node.
    node_list = start_to_end(end_node)

    # Makes a 1000 x 1000 window, and sets the background to white.
    win = GraphWin('Graph', 1000, 1000, autoflush=False)
    win.setBackground('white')

    # Goes through every point in the board and constructs a circle with
    # the approriate color filling.
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == None:
                cur_color = 'black'
            elif board[i][j] == node_list[0] and board[i][j] == node_list[-1]:
                cur_color = 'red'
            elif board[i][j] == node_list[0]:
                cur_color = 'pink'
            elif board[i][j] == node_list[-1]:
                cur_color = 'purple'
            elif board[i][j] in node_list:
                cur_color = 'green2'
            else:
                cur_color = 'yellow'
                
            circ_diam = 1000 / len(board) 
            center = Point(circ_diam/2+(circ_diam*j), circ_diam/2+(circ_diam*i))
            circle = Circle(center,circ_diam/2)
            circle.setFill(cur_color)
            circle.draw(win)

    # Waits for the mouse to be pressed and then closes the window.
    win.getMouse()
    win.close()

# Uses the pred field of the Node class to construct a list from the
# starting node to the end node.
def start_to_end(end_node):
    li = [end_node]
    while end_node.pred is not None:
        li.append(end_node.pred)
        end_node = end_node.pred
    return li[::-1]

def main():
    global board

    # Makes the option variable, which is then used to determine what action
    # to make, depending on user input.
    option = '0'

    # Does the inital initilization of the board and obstacle list.
    obstacles = list()
    board = [[Node(i,j) for j in range(100)] for i in range(100)]
    init_board()

    print('\nThe default value for the start is (0,0) and (99,99) for the end.')
    print('There are no obstacles as a default.')
    print('You can select options from the menu to change the board or display the result.\n')

    # Endlesly loops the option menu, until the user decides to quit the 
    # program. Keeps prompting the user for what action they want to take from
    # the option menu. Makes sure the user enters a correct option. Each option
    # that modifies the board also has to reset it and re-initilize it with the
    # stored obstacles.
    while True:
        print('\nThe current start point is at ({}, {})'.format(start_point[1],start_point[0]))
        print('The current end point is at ({}, {})'.format(end_point[1],end_point[0]))

        print('Enter "1" to add obstacles.')
        print('Enter "2" to randomly generate obstacles.')
        print('Enter "3" to change the start point.')
        print('Enter "4" to change the end point.')
        print('Enter "5" to run the algorithim and display the results.')
        print('Enter "6" to clear obstacles.')
        print('Enter "7" to exit the program.')

        option = input('Enter your option here: ').strip()
        
        if option not in [str(i) for i in range(1,8)]:
            option = '0'
            print('Enter a correct option.')
            continue

        if option == '1':
            board = [[Node(i,j) for j in range(100)] for i in range(100)]
            get_obstacles(obstacles)
            change_obstacles(obstacles)
            init_board() 

        if option == '2':
            board = [[Node(i,j) for j in range(100)] for i in range(100)]
            random_obstacles(obstacles)
            change_obstacles(obstacles)
            init_board() 

        if option == '3':
            change_start()

        if option == '4':
            change_end()

        if option == '5':
            end_node = find_path()
            if end_node == None:
                print("The end point could not be reached from the start given the obstacles.")
            else:
                draw_graph(end_node)
            board = [[Node(i,j) for j in range(100)] for i in range(100)]
            change_obstacles(obstacles)
            init_board()

        if option == '6':
            print('The obstacles have been reset.')
            obstacles = list()
            board = [[Node(i,j) for j in range(100)] for i in range(100)]
            init_board()

        if option == '7':
            exit()


main()
