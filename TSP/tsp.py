import random, math

INIT_PHER = .05
NUM_ITERATIONS = 100
NUM_ANTS = 20 
PHER_EVAP = .2
ALPHA = 1
BETA = 4

TSP_FILE = 'a280.tsp'
OPT_FILE = 'a280_opt.tour'

class City:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y
        self.connections = list()

    def distance(self, c2):
        return max(math.sqrt((self.x - c2.x)**2 + (self.y - c2.y)**2), .001)


class Ant:
    def __init__(self, start_city):
        self.tour = start_city

def file_to_graph(filename):
    cities = list()

    with open(filename, 'r') as file:

        [file.readline() for i in range(6)]
        curline = file.readline().strip()

        while curline != 'EOF':
            line_list = [int(float(i)) for i in curline.split()]
            cities.append(City(*line_list))
            curline = file.readline().strip()

    return cities


def reset_ants(cities):
    return [Ant([cities[0]].copy()) for i in range(NUM_ANTS)]

def iteration(ants, cities, pheramones):
    for ant in ants:
        while len(ant.tour) < len(cities):
            next_city = city_selection(ant, cities, pheramones)

            ant.tour.append(next_city)


def city_selection(ant, cities, pheramones):
    unvisited = unvisited_cities(ant, cities)
    cur_city = ant.tour[-1]

    denom = 0

    for c in unvisited:
        small_label = min(cur_city.label, c.label)-1
        large_label = max(cur_city.label, c.label)-1
        denom += pheramones[small_label][large_label] ** ALPHA * (1/cur_city.distance(c)) ** BETA

    r = 1
    probability = 0

    while r > probability:
        r_city = random.choice(unvisited)
        small_label = min(cur_city.label, r_city.label)-1
        large_label = max(cur_city.label, r_city.label)-1
        numer = pheramones[small_label][large_label] ** ALPHA * (1/cur_city.distance(r_city)) ** BETA

        probability = numer/denom
        r = random.random()
        
    return r_city


def unvisited_cities(ant, cities):
    return [city for city in cities if city not in ant.tour]

def deposit_pheremones_min_ant(ants, pheramones):

    min_ant = ants[-1]

    for ant in ants:
        ant_distance = tour_length(ant)

        if ant_distance < tour_length(min_ant): 
            min_ant = ant

        print(ant_distance)

        for i in range(len(ant.tour)-1):
            small_label = min(ant.tour[i].label, ant.tour[i+1].label)-1
            large_label = max(ant.tour[i].label, ant.tour[i+1].label)-1

            pheramones[small_label][large_label] += 1/ant_distance

    return min_ant

def tour_length(ant):
    out = 0
    for i in range(len(ant.tour)-1):
        out += ant.tour[i].distance(ant.tour[i+1])
    return out

def evaporate_pheremones(pheramones):
    for i in range(len(pheramones)):
        for j in range(len(pheramones[i])):
            pheramones[i][j] *= 1 - PHER_EVAP

def optimal_length(filename, cities):
    distance = 0
    with open(filename, 'r') as file:
        
        prev_city = 1

        [file.readline() for i in range(4)]
        curline = file.readline().strip()
        
        while curline != '-1':
            cur_city = int(float(curline))
            distance += cities[prev_city-1].distance(cities[cur_city-1])
            prev_city = cur_city

            curline = file.readline().strip()

    return distance


def set_pher(cities):
    global INIT_PHER

    nn_ant = Ant(cities[0])
    distance = 0

    while len(nn_ant.tour) < len(cities):
        unvisited = unvisited_cities(nn_ant, cities)

        cur_city = nn_ant.tour[-1]
        next_city = unvisited[0]

        for i in unvisited[1:]:
            if cur_city.distance(next_city) > cur_city.distance(i): next_city = i

        distance += cur_city.distance(next_city)
        nn_ant.tour.append(next_city)

    INIT_PHER = 1 / distance



def main():
    cities = file_to_graph(TSP_FILE)
    pheramones = [[INIT_PHER for i in cities] for j in cities]
    set_pher(cities)
    ants = reset_ants(cities)
    
    min_ant = None
    
    for _ in range(NUM_ITERATIONS):

        ants = reset_ants(cities)
        iteration(ants, cities, pheramones)
        evaporate_pheremones(pheramones)

        if min_ant == None: min_ant = ants[0]

        temp_ant = deposit_pheremones_min_ant(ants, pheramones)
        if tour_length(temp_ant) < tour_length(min_ant): min_ant = temp_ant

        #for ant in ants: 
        #    print(tour_length(ant))
        print('The current minimum tour length is: ', tour_length(min_ant))
        print('\n')


    print('The optimal length is :', str(optimal_length(OPT_FILE, cities)), '\n')

if __name__=="__main__": main()
