from random import uniform
from math import e

# CLASSES

# Class that stores each image object read from file.
# Stores the actual image array as well as methods to represent it and flatten.
class Image:
    def __init__(self, image, number):
        self.image = image
        self.actual_number = number

    def flatten(self):
        output = list()
        for line in self.image:
            for number in line:
                output.append(number)
        return output

    def __repr__(self):
        out = ""
        for line in self.image: 
            for i in line:
                out += str(i)
            out += '\n'
        out += str(self.actual_number)
        return out

# Class that represents each node in network, stores pre-sigmoid value and
# list of input and/or output edges.
class Node:
    def __init__(self):
        self.value = 0.0
        self.input_edges = list()
        self.output_edges = list()

def __repr__(self):
        return str(self.value)

# Class for every edge between nodes. Stores output and input node 
# as well as edge weight.
class Edge:
    def __init__(self, i, o, w):
        self.input_node = i
        self.output_node = o
        self.weight = w

    def __repr__(self):
        return str(self.weight)


# HELPER FUNCTIONS

# Returns node with highest value from output layer.
# Larger pre-sigmoid value will correcspond with higher post-sigmoid value
# so it saves computation time to compare pre-sigmoid values.
def max_node(model):
    out = model[-1][0]
    for node in model[-1][1:]:
        if node.value > out.value: out = node
    return out

# Input image, model, and specific output node.
# Returns the error of the specific node by subtracting excepected value
# from actual post-sigmoid value.
def calculate_error(image, model, node):
    return (0.0 if model[-1].index(node) != image.actual_number else 1.0) - sigmoid_function(node.value)

def sigmoid_function(x): 
    return 1/(1+e**(-x))

def sigmoid_derivative(x):
    return sigmoid_function(x) * (1-sigmoid_function(x))


# FILE FUNCTIONS

# Return a list of image objects made from data in given file.
def read_data(filename):
    images = list()

    with open(filename, 'r') as file:
        uncompleted_image = list()
        for line in file:
            processed_line = [int(i) for i in list(line.strip())]

            # If the current line is a single digit, it means that the 
            # image is complete and the current line is what the image
            # represents.
            if len(processed_line) == 1:
                images.append(Image(uncompleted_image.copy(), processed_line[0]))
                uncompleted_image = list()
            else:
                uncompleted_image.append(processed_line.copy())

    return images

# Read weights from a file, convert them to a float, and set 
# them as the edge weight.
def weights_from_file(model):
    with open('runtime_files/edge_values.txt', 'r') as file:
        for node in model[0]:
            for edge in node.output_edges:
                edge.weight = float(file.readline().strip())

# Save the edge weights to a file, every 10 numbers all the edges from an
# input node to an output node.
def save_to_file(model):
    f = open('runtime_files/edge_values.txt', 'w')
    for input_node in model[0]:
        for edge in input_node.output_edges:
            f.write(str(edge.weight) + '\n')
    f.close()
