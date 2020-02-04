import random
import math

NUM_EPOCHS = 25
LEARNING_RATE = .2
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
    model = [list() for _ in range(len(NODES_IN_MODEL_LAYERS)*2-1)]

    for i in range(len(NODES_IN_MODEL_LAYERS)):
        for _ in range(NODES_IN_MODEL_LAYERS[i]):
            model[i*2].append(0.0)
        if i != len(NODES_IN_MODEL_LAYERS)-1: model[i*2].append(1.0)

    for i in reversed(range(1, len(NODES_IN_MODEL_LAYERS))):
        for j in range(len(model[i*2]) - (1 if i*2+1 != len(model) else 0)):
            model[i*2-1].append(list())
            for k in range(len(model[i*2-2])):
                model[i*2-1][j].append(random.uniform(MIN_INITIAL_WEIGHT, MAX_INITIAL_WEIGHT))
                

    return model

def run_epoch(data, model):
    accuracy_sum = 0
    for image in data:
        accuracy_sum += run_single_image(image, model)

    print(round(accuracy_sum/len(data)*100,3))

    random.shuffle(data)

def run_single_image(image, model):
    flat_image = image.flatten()
    for i in range(len(flat_image)):
        model[0][i] = flat_image[i]
        #print(flat_image[i])

    for i in range(1, len(NODES_IN_MODEL_LAYERS)):
        for j in range(len(model[i*2])):
            #print(len(model[i*2-1][j]))
            cur_activation_sum = 0.0
            for k in range(len(model[i*2-1][j])):
                #print(model[i*2-1][j][k])
                #print(model[i*2-2][k])
                cur_activation_sum += model[i*2-1][j][k] * model[i*2-2][k]
            #print(cur_activation_sum)
            model[i*2][j] = cur_activation_sum

    #print([sigmoid_function(i) for i in model[-1]])

    backpropogate(image, model)

    if image.actual_number == model[-1].index(max_node(model, -1)): return 1
    return 0
    
    
def backpropogate(image, model):
    for i in range(len(model[-1])):
        der_value = sigmoid_derivative(model[-1][i])
        output_error = calculate_error(image, model,  model[-1][i])
        weight_change = LEARNING_RATE * output_error * der_value
        for j in range(len(model[1][i])):
            model[1][i][j] += (weight_change * sigmoid_function(model[0][j]))
            

    
def sigmoid_function(x): 
    return 1/(1+math.e**(-x))

def sigmoid_derivative(x):
    return sigmoid_function(x) * (1-sigmoid_function(x))

def calculate_error(image, model, node):
    return (0.0 if model[-1].index(node) != image.actual_number else 1.0) - sigmoid_function(node)

def max_node(model, layer):
    cur_out = model[layer][0]
    for i in model[layer][1:]:
        if i > cur_out: cur_out = i
    return cur_out

def train_model():
    training_data, testing_data = read_data()
    model = init_network()
    for _ in range(NUM_EPOCHS):
        run_epoch(training_data, model)
    #run_single_image(training_data[0], model)
    #print(training_data[-1])

def main():
   train_model()

if __name__=='__main__': main()
