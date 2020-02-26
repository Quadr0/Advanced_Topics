# Matplotlib is a neccesary library
import matplotlib.pyplot as plt

import random, math

# Constants used to control variables in algorithm and equations.
# If they vary from the guidelines, that is because I have tested 
# theses to be better.
NUM_ITERATIONS = 20
NUM_ANTS = 20
PHER_EVAP = .2
ALPHA = 2
BETA = 5

# Toggle True or False to determine if elitist or plain ant colony runs.
RUN_ELITIST = True

# File for city locations.
TSP_FILE = 'a280.tsp'

# File for optimized ant tour.
OPT_FILE = 'a280_opt.tour'

# City class that contains where in the cities list it is, x and y coordinate,
# and a distance function to find distance form another city.
class City:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y

    # Returns the euclidean distance between two cities or a small number
    # if two cities are right on top of each other.
    def distance(self, c2):
        return max(math.sqrt((self.x - c2.x)**2 + (self.y - c2.y)**2), .001)

# Ant class that keeps track of where an ant has been.
class Ant:
    def __init__(self, start_city):
        self.tour = [start_city]

# Convert the .tsp file to a list of cities
def file_to_graph(filename):
    cities = list()

    with open(filename, 'r') as file:

        # Skip header information.
        [file.readline() for i in range(6)]

        curline = file.readline().strip()

        # Keep adding cities to list while end of file is not reached.
        while curline != 'EOF':
            line_list = [int(float(i)) for i in curline.split()]
            cities.append(City(*line_list))
            curline = file.readline().strip()

    return cities

# Reset the list of ants so that the ants all start at the first city.
def reset_ants(cities):
    return [Ant(cities[0]) for i in range(NUM_ANTS)]

# Run an iteration where each ant builds its tour.
def iteration(ants, cities, pheramones):

    for ant in ants:

        # While the ant's tour is not complete, add more cities.
        while len(ant.tour) < len(cities):
            ant.tour.append(city_selection(ant, cities, pheramones))

# Choose the next city for the ant to visit by 
# using the city choice equation.
def city_selection(ant, cities, pheramones):

    # Get a list of the ants unvisited cities.
    unvisited = unvisited_cities(ant, cities)

    cur_city = ant.tour[-1]

    # Find the denominator by finding the distance and pheramone levels
    # between the unvisited cities and current city and do the neccesary math.
    denom = 0
    for c in unvisited:

        # Do a bit of processing to make sure that two cities always refer to 
        # the same pheramone number.
        small_label = min(cur_city.label, c.label)-1
        large_label = max(cur_city.label, c.label)-1

        denom += pheramones[small_label][large_label] ** ALPHA * (1/cur_city.distance(c)) ** BETA

    # r is the value that has to be smaller than the probability to add
    # the current random unvisited city to the ant's tour
    r = 1

    # probability is the current numerator divided by the denominator.
    probability = 0

    # Try a new city and probability while r is bigger than the probability.
    # Simulates a java do-while loop.
    while r > probability:

        # Randomly picked city.
        r_city = random.choice(unvisited)

        # Do a bit of processing to make sure that two cities always refer to 
        # the same pheramone number.
        small_label = min(cur_city.label, r_city.label)-1
        large_label = max(cur_city.label, r_city.label)-1

        # Calculate the numerator with the given formula.
        numer = pheramones[small_label][large_label] ** ALPHA * (1/cur_city.distance(r_city)) ** BETA

        probability = numer/denom
        r = random.random()
        
    return r_city

# Use a list comprehension to get all the cities a given ant has not been to.
def unvisited_cities(ant, cities):
    return [city for city in cities if city not in ant.tour]

# Function to deposit pheramones as well as return the ant with the smallest
# tour in a given iteration.
# If return_min_ant = True: a minimum ant will be returned and the lengths
#   of all the ants in the interation will be printed.
# If return_min_ant = False: a minimum ant will not be returned and nothing 
#   will be printed. Only False for elitist ant pheramone deposit.
def deposit_pheremones_min_ant(ants, pheramones, return_min_ant=True):
    if return_min_ant: min_ant = ants[-1]

    if return_min_ant: print('The ant tour lengths for this iteration are: ')

    for ant in ants:
        ant_distance = tour_length(ant)

        if return_min_ant and ant_distance < tour_length(min_ant): 
            min_ant = ant

        if return_min_ant: print(' ',round(ant_distance, 2))

        # Go through every edge between cities ant visits and update the
        # pheramones using the given equation.
        for i in range(len(ant.tour)-1):

            # Do a bit of processing to ensure both cities referce same
            # pheramone value.
            small_label = min(ant.tour[i].label, ant.tour[i+1].label)-1
            large_label = max(ant.tour[i].label, ant.tour[i+1].label)-1

            pheramones[small_label][large_label] += 1/ant_distance

    if return_min_ant: return min_ant


# Iterate through every city in an ant's tour and 
# sum the distance between cities.
def tour_length(ant):
    out = 0
    for i in range(len(ant.tour)-1):
        out += ant.tour[i].distance(ant.tour[i+1])
    return out

# Go through every pheramone spot and remove the amount 
# specified by the PHER_EVAP constant.
def evaporate_pheremones(pheramones):
    for i in range(len(pheramones)):
        for j in range(len(pheramones[i])):
            pheramones[i][j] *= 1 - PHER_EVAP

# Find the optimal tour by using the .tour file and return 
# the distance and ant with the optimal tour.
def optimal_length(filename, cities):
    distance = 0
    o_ant = Ant(cities[0])

    with open(filename, 'r') as file:
        
        prev_city = o_ant.tour[-1]

        # Skip header information.
        [file.readline() for i in range(4)]

        curline = file.readline().strip()
        
        # Keep adding to the distance and building the ant's tour until the 
        # end of the file is reached.
        while curline != '-1':
            cur_city = cities[int(float(curline))-1]
            distance += prev_city.distance(cur_city)
            o_ant.tour.append(cur_city)
            prev_city = cur_city

            curline = file.readline().strip()

    return distance, o_ant


# Build the nearest neighbor ant's tour and return it as well as its distance.
def nn_ant_dist(cities):
    nn_ant = Ant(cities[0])
    distance = 0

    # Keep adding cities until the ant's tour is complete. 
    while len(nn_ant.tour) < len(cities):

        # Get all unvisited cities.
        unvisited = unvisited_cities(nn_ant, cities)

        cur_city = nn_ant.tour[-1]
        next_city = unvisited[0]

        # Find the closest city from the current city.
        for i in unvisited[1:]:
            if cur_city.distance(next_city) > cur_city.distance(i): next_city = i

        distance += cur_city.distance(next_city)
        nn_ant.tour.append(next_city)

    return (1 / distance, nn_ant)


# Plot an ant's path along the cities using matplotlib.
# This function takes a list of ants, the list of cities, 
# and a list of window titles.
def plot_solutions(ants, cities, titles):
    for a in range(len(ants)):

        ant = ants[a]

        # Make a new figure so that all the different ant tours have
        # their own window.
        cur_figure = plt.figure(a+1)

        # Title the figure's window.
        cur_figure.canvas.set_window_title(titles[a])

        for i in range(len(ant.tour)-1):
            cur_city = ant.tour[i]
            next_city = ant.tour[i+1]

            xs = [cur_city.x, next_city.x]
            ys = [cur_city.y, next_city.y]
    
            # Draw lines to signify an ant's travel between cities.
            plt.plot(xs, ys, 'y-')

        # Overlay dots over lines to signify where the cities are.
        plt.plot([c.x for c in ant.tour], [[c.y] for c in ant.tour], 'bo', linewidth=10)

        # Show the ant's distance in the popup.
        plt.title("The distance of this ant is: {}".format(round(tour_length(ant), 2)))

    plt.show()

def main():
    cities = file_to_graph(TSP_FILE)

    # Get the initial pheramone level from the nearest neighbor algorithm
    # as well as the nearest neighbor ant so it can be displayed later.
    init_pher, nn_ant = nn_ant_dist(cities)

    # Make a pheramone 2d array with the initial pheramone level.
    # Only half of this array will ever be used.
    pheramones = [[init_pher for i in cities] for j in cities]

    print('The initial pheramone is:', init_pher, '\n')

    ants = None

    # Variable that will be used to keep track of the global best ant.
    # Will be used for elitist ant colony algorithm as well as what will
    # be displayed in the graph popup.
    min_ant = None
    
    for _ in range(NUM_ITERATIONS):

        ants = reset_ants(cities)
        iteration(ants, cities, pheramones)
        evaporate_pheremones(pheramones)

        # In the first iteration, after the tours have been built, make sure
        # the min_ant variable is initialized to an ant with a full tour.
        if min_ant == None: min_ant = ants[0]

        # Get the ant with the minimum tour from the current iteration.
        iter_min_ant = deposit_pheremones_min_ant(ants, pheramones)

        # Update the global best ant if neccesary.
        if tour_length(iter_min_ant) < tour_length(min_ant): min_ant = iter_min_ant

        # If the elitist option is toggled, the global best ant will update the
        # pheramones based on it's tour. This is the only diffrence between
        # ant colony and elitist ant colony.
        if RUN_ELITIST: deposit_pheremones_min_ant([min_ant], pheramones, return_min_ant=False)

        print('The current global minimum tour length is:', round(tour_length(min_ant), 2))
        print('\n')


    o_distance, o_ant = optimal_length(OPT_FILE, cities)

    print('\n')
    print('The optimal length is :', o_distance, '\n')

    ants_to_plot = [o_ant, min_ant, nn_ant]
    plot_titles = ['Optimal Tour Ant', 'Minumum Ant Colony Tour', 'Nearest Neighbor Ant']
    
    plot_solutions(ants_to_plot, cities, plot_titles)

if __name__=="__main__": main()
