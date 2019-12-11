from graphics import *
from math import sqrt

class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.con_list = list()
        self.pred = None
        self.dist = -1

    def __repr__(self):
        return str(self.dist)

board = list()
start_point = [0,0]
end_point = [99,99]

def get_obstacles(obstacles):
    while(True):
        print('\nIf you are done entering obstacles, enter "stop" for the first prompt')
        point1 = input('Enter the top right corner of the obstacle in the format "y,x": ')
        point1 = point1.strip().lower()
        if point1 == 'stop' : break
        point1 = [int(i) for i in point1.split(',')]

        point2 = input('Enter the left corner of the obstacle in the format "y,x": ')
        point2 = point2.strip()
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

def change_start():
    global start_point

    start_point = input('enter the starting coordinates in the format "y,x": ').strip()
    start_point = [int(i) for i in start_point.split(',')]
    while(board[start_point[1]][start_point[0]] == None or sum([1 for i in start_point if i in range(100)]) < 2):
        start_point = input('The start point you entered is invalid, enter a valid start point: ')
        start_point = [int(i) for i in start_point.split(',')]
    print('\n')

def change_end():
    global end_point

    end_point = input('enter the ending coordinates in the format "y,x": ').strip()
    end_point = [int(i) for i in end_point.split(',')]
    while(board[end_point[1]][end_point[0]] is None):
        end_point = input('your point is in an obstace, enter a valid end point: ')
        end_point = [int(i) for i in end_point.split(',')]
    print('\n')


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


def connect_node(i, j, i_change, j_change, value):
    cur_node = board[i][j]
    rows = len(board)
    columns = len(board[0])

    if i_change >= rows or i_change < 0 or j_change >= columns or j_change < 0 or board[i_change][j_change] == None:
        return

    cur_node.con_list.append([board[i_change][j_change],value])

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

            if neighbor.dist == -1:
                neighbor.dist = cur_node.dist + value
                neighbor.pred = cur_node

            elif cur_node.dist + value < neighbor.dist:
                neighbor.dist = cur_node.dist + value
                neighbor.pred = cur_node



    return None

def draw_graph(end_node):
    node_list = start_to_end(end_node)

    win = GraphWin('Graph', 1200, 1000, autoflush=False)
    win.setBackground('white')

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == None:
                cur_color = 'black'
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

    win.getMouse()
    win.close()

def start_to_end(end_node):
    li = [end_node]
    while end_node.pred is not None:
        li.append(end_node.pred)
        end_node = end_node.pred
    return li[::-1]

def main():
    global board

    option = '0'
    obstacles = list()
    board = [[Node(i,j) for j in range(100)] for i in range(100)]
    init_board()

    print('\nThe default value for the start is (0,0) and (99,99) for the end.')
    print('There are no obstacles as a default.')
    print('You can select options from the menu to change the board or display the result.\n')

    while option != '6':
        print('The current start point is at ({}, {})'.format(start_point[1],start_point[0]))
        print('The current end point is at ({}, {})'.format(end_point[1],end_point[0]))

        print('Enter "1" to add obstacles.')
        print('Enter "2" to change the start point.')
        print('Enter "3" to change the end point.')
        print('Enter "4" to run the algorithim and display the results.')
        print('Enter "5" to clear the obstacles.')
        print('Enter "6" to exit the program.')
        option = input('Enter your option here: ').strip()
        
        if option not in [str(i) for i in range(1,7)]:
            option = '0'
            print('Enter a correct option.')
            continue

        if option == '1':
            board = [[Node(i,j) for j in range(100)] for i in range(100)]
            get_obstacles(obstacles)
            change_obstacles(obstacles)
            init_board() 

        if option == '2':
            change_start()

        if option == '3':
            change_end()

        if option == '4':
            end_node = find_path()
            if end_node is None:
                print("The end point could not be reached from the start given the obstacles.")
            else:
                draw_graph(end_node)
            board = [[Node(i,j) for j in range(100)] for i in range(100)]
            change_obstacles(obstacles)
            init_board()

        if option == '5':
            print('The obstacles have been reset.')
            obstacles = list()
            board = [[Node(i,j) for j in range(100)] for i in range(100)]
            init_board()

        if option == '6':
            exit(0)

        print('\n')

main()
