from classes_and_utils import *

from random import shuffle

# Set constants that will be used to change model parameters.
NUM_EPOCHS = 8
LEARNING_RATE = .1
MIN_INITIAL_WEIGHT = -.4
MAX_INITIAL_WEIGHT = .4

# Boolean options to read or save weights from file. Make sure file exists.
# If READ_FROM_FILE is true, no training epochs will occur.
READ_FROM_FILE = False
SAVE_TO_FILE = True

# List that describes the number of nodes in each layer of model
# DO NOT CHANGE!!!
NODES_IN_MODEL_LAYERS = [1024, 10]

# Function that initializes the model and all the nodes and edges between them.
# Sets the edge weight randomly between min and max parameters. 
def init_network():
    
    # Model is a 2d array where each row is a layer in the network. 
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

# Runs a single epoch of training or testing and returns accuracy of the epoch. 
# Shuffles data after each epoch to slowdown overfitting.

def run_epoch(data, model, backprop=True):
    cur_sum = 0

    for image in data:
        cur_sum += run_single_image(image, model, backprop)

    shuffle(data)
    return str(round(cur_sum/len(data)*100, 3))

# Takes in an image object, 2d model list, and 
# boolean option to backpropogate or not.
# Returns a 1 if the image was correctly identified or 0 if incorrect. 
# Backpropogation occurs, if it occurs, after every image.
def run_single_image(image, model, backprop):
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
    
    
def backpropogate(image, model):
    for output_node in model[-1]:
        der_value = sigmoid_derivative(output_node.value)
        error = calculate_error(image, model, output_node)
        pre_weight_change = LEARNING_RATE * error * der_value
        for edge in output_node.input_edges:
            edge.weight += sigmoid_function(edge.input_node.value) * pre_weight_change
    

def main():
    model = init_network()

    if READ_FROM_FILE: weights_from_file(model)
    else:
        training_data = read_data('runtime_files/optdigits-32x32.tra')
        for i in range(NUM_EPOCHS):
            accuracy = run_epoch(training_data, model)
            print('Training epoch {}: The accuracy is {}'.format(i+1, accuracy))
            #print('The accuracy of this training epoch is', accuracy)

    if SAVE_TO_FILE: save_to_file(model)
    
    testing_data = read_data('runtime_files/optdigits-32x32.tes')
    accuracy = run_epoch(testing_data, model, backprop=False)
    print('The accuracy of the testing epoch is', accuracy)

if __name__=='__main__': main()
