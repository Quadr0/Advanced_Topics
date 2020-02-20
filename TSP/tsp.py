import random, math

INIT_PHER = .05
NUM_ITERATIONS = 5
NUM_ANTS = 20
PHER_EVAP = .1
ALPHA = 1
BETA = 3

TSP_FILE = 'berlin52.tsp'
OPT_FILE = 'berlin52_opt.tour'

class City:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y
        self.connections = list()

    def distance(self, c2):
        return math.sqrt((self.x - c2.x)**2 + (self.y - c2.y)**2)


class Ant:
    def __init__(self, start_city):
        self.tour = [start_city]

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
    return [Ant(cities[0]) for i in range(NUM_ANTS)]

def iteration(ants, cities, pheramones):
    for ant in ants:
        while len(ant.tour) < len(cities):
            ant.tour.append(city_selection(ant, cities, pheramones))
                

def city_selection(ant, cities, pheramones):
    unvisited = unvisited_cities(ant, cities)
    cur_city = ant.tour[-1]

    denom = 0
    for c in unvisited:
        small_label = min(cur_city.label, c.label)-1
        large_label = max(cur_city.label, c.label)-1
        denom += pheramones[small_label][large_label] ** ALPHA * cur_city.distance(c) ** BETA

    r = 1
    probability = 0

    while r > probability:
        r_city = random.choice(unvisited)
        small_label = min(cur_city.label, r_city.label)-1
        large_label = max(cur_city.label, r_city.label)-1
        numer = pheramones[small_label][large_label] ** ALPHA * cur_city.distance(r_city) ** BETA

        probability = numer/denom
        #print('The probability is:', probability)
        r = random.random()
        
    return r_city


def unvisited_cities(ant, cities):
    return [city for city in cities if city not in ant.tour]

def deposit_pheremones(ants, pheramones):
    for ant in ants:
        ant_distance = tour_length(ant)
        #print(ant_distance)
        for i in range(len(ant.tour)-1):
            small_label = min(ant.tour[i].label, ant.tour[i+1].label)-1
            large_label = max(ant.tour[i].label, ant.tour[i+1].label)-1

            pheramones[small_label][large_label] += 1/ant_distance

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
        
        while curline != 'EOF':
            cur_city = int(float(curline))
            distance += cities[prev_city-1].distance(cities[cur_city-1])
            prev_city = cur_city

            curline = file.readline().strip()

    return distance


def main():
    cities = file_to_graph(TSP_FILE)
    pheramones = [[INIT_PHER for i in cities] for j in cities]
    

    for _ in range(NUM_ITERATIONS):
        ants = reset_ants(cities)
        iteration(ants, cities, pheramones)
        deposit_pheremones(ants, pheramones)
        evaporate_pheremones(pheramones)
        print('\n')

    for i in ants[0].tour:
        #print(i.label)

    print('The optimal length is :', optimal_length(OPT_FILE, cities), '\n')

    #for i in range(len(pheramones)):
    #    for j in range(len(pheramones[i])):
    #        print(pheramones[i][j])

if __name__=="__main__": main()
