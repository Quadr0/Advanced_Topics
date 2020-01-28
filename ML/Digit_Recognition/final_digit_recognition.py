import random
import math

NUM_EPOCHS = 5
LEARNING_RATE = .1
MIN_INITIAL_WEIGHT = -1
MAX_INITIAL_WEIGHT = 1

NODES_IN_MODEL_LAYERS = [1024, 10]

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

class Node:
    def __init__(self):
        self.value = 0.0
        self.input_edges = list()
        self.output_edges = list()

    def __repr__(self):
        return str(self.value)

class Edge:
    def __init__(self, i, o):
        self.input_node = i
        self.output_node = o
        self.weight = random.uniform(MIN_INITIAL_WEIGHT, MAX_INITIAL_WEIGHT)

    def __repr__(self):
        return str(self.weight)

def read_data():
    training_files = ['optdigits-32x32.tra', 'optdigits-32x32.tes']
    data = [list(), list()]

    for i in range(len(training_files)):
        with open(training_files[i], 'r') as file:
            uncompleted_image = list()
            for line in file:
                processed_line = [int(i) for i in list(line.strip())]
                if len(processed_line) == 1:
                    data[i].append(Image(uncompleted_image.copy(), processed_line[0]))
                    uncompleted_image = list()
                else:
                    uncompleted_image.append(processed_line.copy())

    return (data[0], data[1])

def init_network():
    model = [list() for _ in range(len(NODES_IN_MODEL_LAYERS))]

    for i in range(len(NODES_IN_MODEL_LAYERS)):
        for _ in range(NODES_IN_MODEL_LAYERS[i]):
            model[i].append(Node())
        if i != len(NODES_IN_MODEL_LAYERS) - 1:
            bias_node = Node()
            bias_node.value = 1
            model[i].append(bias_node)

    for next_layer_i in reversed(range(1, len(model))):
        for next_node in model[next_layer_i]:
            for prev_node in model[next_layer_i-1]:
                edge = Edge(prev_node, next_node)
                prev_node.output_edges.append(edge)
                next_node.input_edges.append(edge)

    return model

def run_epoch(data, model):
    pass

def run_single_image(image, model):
    flattened_image = image.flatten()

    for i in range(len(flattened_image)):
        model[0][i].value = flattened_image[i]

    for output_node in model[-1]:
        cur_activation_sum = 0.0
        for edge in output_node.input_edges:
            cur_activation_sum += edge.weight * sigmoid_function(edge.input_node.value)
        output_node.value = cur_activation_sum


    backpropogate(image, model)
    
def max_node(model):
    pass
    
def backpropogate(image, model):
    pass
    
def sigmoid_function(x): 
    return 1/(1+math.e**(-x))

def sigmoid_derivative(x):
    return sigmoid_function(x) * (1-sigmoid_function(x))

def calculate_error(image, model, node):
    pass

def train_model():
    training_data, testing_data = read_data()
    model = init_network()
    for _ in range(NUM_EPOCHS):
        run_epoch(training_data, model)

def main():
   train_model()

if __name__=='__main__': main()
