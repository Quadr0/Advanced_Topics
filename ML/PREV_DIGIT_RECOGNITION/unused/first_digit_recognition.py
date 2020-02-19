import random
import math

NUM_EPOCHS = 1
LEARNING_RATE= 1
MIN_INITIAL_WEIGHT = -1
MAX_INITIAL_WEIGHT = 1

# Number of nodes in input as well as hidden layers.
NODES_IN_INPUT_HIDDEN_LAYERS = [1024]

class Image:
    def __init__(self, image, number):
        self.image = image
        self.number = number

    def flatten(self):
        return [i for sub in self.image for i in sub]

    def __repr__(self):
        out = ""
        for line in self.image:
            for i in line:
                out += str(i)
            out += '\n'
        out += str(self.number)
        return out

class Input_Node:
    def __init__(self):
        self.pre_value = 0.0
        self.post_value = 0.0
        self.input_edges = list()
        self.output_edges = list()

class Output_Node:
    def __init__(self, number):
        self.output_number = number
        self.pre_value = 0.0
        self.post_value = 0.0
        self.input_edges = list()

class Edge:
    def __init__(self, i, o):
        self.input_node = i
        self.output_node = o
        self.weight = random.uniform(MIN_INITIAL_WEIGHT, MAX_INITIAL_WEIGHT)

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
    input_hidden_nodes = list()
    output_nodes = list()

    for i in range(len(NODES_IN_INPUT_HIDDEN_LAYERS)):
        input_hidden_nodes.append(list())
        for _ in range(NODES_IN_INPUT_HIDDEN_LAYERS[i]):
            input_hidden_nodes[i].append(Input_Node())
        bias_node = Input_Node()
        bias_node.pre_value = 1
        bias_node.post_value = 1
        input_hidden_nodes[i].append(bias_node)
    
    for i in range(10):
        output_nodes.append(Output_Node(i))

    for i in range(len(input_hidden_nodes[:-2])):
       for cur_node in input_hidden_nodes[i]:
           for next_node in input_hidden_nodes[i+1][:-1]:
               cur_edge = Edge(cur_node, next_node)
               cur_node.output_edges.append(cur_edge)
               next_node.input_edges.append(cur_edge)

    for output_node in output_nodes:
        for pre_node in input_hidden_nodes[-1]:
            cur_edge = Edge(pre_node, output_node)
            pre_node.output_edges.append(cur_edge)
            output_node.input_edges.append(cur_edge)

    return (input_hidden_nodes, output_nodes)


def run_epoch(data, input_hidden_nodes, output_nodes):
    accuracy_sum = 0
    for image in data:
        accuracy_sum += run_single_image(image, input_hidden_nodes, output_nodes)

    print(round(accuracy_sum/len(data)*100,3))

    #random.shuffle(data)

def run_single_image(image, input_hidden_nodes, output_nodes):
    flattened_image = image.flatten()

    for i in range(len(flattened_image)):
        input_hidden_nodes[0][i].pre_value = flattened_image[i]
        input_hidden_nodes[0][i].post_value = flattened_image[i]

    for cur_nodes in input_hidden_nodes[1:]:
        for cur_node in cur_nodes:
            cur_activation_sum = 0
            for cur_edge in cur_node.input_edges:
                cur_activation_sum += cur_edge.weight * cur_edge.input_node.post_value
            cur_node.post_value = activation_function(cur_activation_sum)
            cur_node.pre_value = cur_activation_sum

    for end_node in output_nodes:
        cur_activation_sum = 0
        for end_edge in end_node.input_edges:
            cur_activation_sum += end_edge.weight * end_edge.input_node.post_value
        end_node.post_value = activation_function(cur_activation_sum)
        end_node.pre_value = cur_activation_sum

    back_propogate(image, input_hidden_nodes, output_nodes)

    m_node = max_node(output_nodes)

    #print([node.pre_value for node in output_nodes])
    #print([node.post_value for node in output_nodes])
    #print(m_node.output_number, '\n')

    if m_node.output_number == image.number: return 1
    else: return 0

    
def max_node(output_nodes):
    cur_out = output_nodes[0]
    
    for node in output_nodes[1:]:
        if node.post_value > cur_out.post_value : cur_out = node
    
    return cur_out

    
def back_propogate(image, input_hidden_nodes, output_nodes):
    for node in output_nodes:
        der_value = der_activation_function(node.pre_value)
        output_error = calculate_error(node, image)
        weight_change = LEARNING_RATE * output_error * der_value
        for edge in node.input_edges:
            edge.weight += weight_change * edge.input_node.post_value

    #for hidden_layer in input_hidden_nodes[1::-1]:
    #    for node in hidden_layer[:-1]:
    #        der_value = der_activation_function(node.value)
    #        for edge in node.input_edges:
    #            weight_change = LEARNING_RATE * der_value * edge.input_node.value
    #            edge.weight = edge.weight + weight_change

    
def activation_function(x): 
    return 1/(1+math.exp(-x))

def der_activation_function(x):
    return activation_function(x) * (1-activation_function(x))

def calculate_error(output_node, actual_number):
    output = output_node.post_value
    if output_node.output_number == actual_number:
        output -= 1
    return output

def train_model():
    training_data, testing_data = read_data()
    input_hidden_nodes, output_nodes = init_network()
    for _ in range(NUM_EPOCHS):
        run_epoch(training_data, input_hidden_nodes, output_nodes)
    #run_single_image(training_data[0], input_hidden_nodes, output_nodes)
    print(training_data[-1])

def main():
   train_model()

if __name__=='__main__': main()
