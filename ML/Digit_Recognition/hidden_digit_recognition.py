import random
import math

NUM_EPOCHS = 5
LEARNING_RATE = .1
MIN_INITIAL_WEIGHT = -.4
MAX_INITIAL_WEIGHT = .4

NODES_IN_MODEL_LAYERS = [1024, 128, 10]

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

def weights_from_file(model):
    with open('edge_values.txt', 'r') as file:
        for node in model[0]:
            for edge in node.output_edges:
                edge.weight = float(file.readline().strip())
            file.readline()


def run_epoch(data, model, backprop=True):
    cur_sum = 0
    for image in data:
        cur_sum += run_single_image(image, model, backprop)


    random.shuffle(data)
    return str(round(cur_sum/len(data)*100, 3))


def run_single_image(image, model, backprop, acc_mode=True):
    flattened_image = image.flatten()

    for i in range(len(flattened_image)):
        model[0][i].value = flattened_image[i]

    for output_node in model[-1]:
        cur_value = 0.0
        for edge in output_node.input_edges:
            cur_value += edge.weight * sigmoid_function(edge.input_node.value)
        output_node.value = cur_value


    if(backprop): backpropogate(image, model)

    if model[-1].index(max_node(model)) == image.actual_number: return 1
    else: return 0
    
def max_node(model):
    out = model[-1][0]
    for node in model[-1][1:]:
        if node.value > out.value: out = node
    return out
    
def backpropogate(image, model):
    for output_node in model[-1]:
        der_value = sigmoid_derivative(output_node.value)
        error = calculate_error(image, model, output_node)
        pre_weight_change = LEARNING_RATE * error * der_value
        for edge in output_node.input_edges:
            edge.weight += sigmoid_function(edge.input_node.value) * pre_weight_change

def save_to_file(model):
    f = open('edge_values.txt', 'w')
    for input_node in model[0]:
        for edge in input_node.output_edges:
            f.write(str(edge.weight) + '\n')
        f.write('\n')
    f.close()
    
def sigmoid_function(x): 
    return 1/(1+math.e**(-x))

def sigmoid_derivative(x):
    return sigmoid_function(x) * (1-sigmoid_function(x))

def calculate_error(image, model, node):
    return (0.0 if model[-1].index(node) != image.actual_number else 1.0) - sigmoid_function(node.value)

def main():
    data_files = ['optdigits-32x32.tra', 'optdigits-32x32.tes']
    training_data, testing_data = read_data(data_files)
    model = init_network()
    #for _ in range(NUM_EPOCHS):
    #    accuracy = run_epoch(training_data, model)
    #    print('The accuracy of this training epoch is', accuracy)

    #save_to_file(model)
    weights_from_file(model)    

    accuracy = run_epoch(testing_data, model, backprop=False)
    print('The accuracy of this training epoch is', accuracy)

if __name__=='__main__': main()
