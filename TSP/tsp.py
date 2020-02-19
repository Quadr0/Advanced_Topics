import random
import math

INIT_PHER = .05
NUM_ITERATIONS = 10
NUM_ANTS = 20
PHER_EVAP = .1
ALPHA = 1
BETA = 3

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

        while(curline != 'EOF'):
            line_list = [int(i) for i in curline.split()]
            cities.append(City(*line_list))
            curline = file.readline().strip()

    return cities


def reset_ants(cities):
    ants = list()
    for _ in range(NUM_ANTS):
        ants.append(Ant(cities[0]))
    return ants

def iteration(ants, cities, pheramones):
    for ant in ants:
        while len(ants.tour) < len(cities):
            pass
                

def city_selection(ant, cities, pheramones):
    unvisited = unvisited_cities(ant, cities)
    cur_city = ant.tour[-1]

    denom = 0
    for c in unvisited:
        small_label = min(cur_city.label, c.label)-1
        large_label = max(cur_city.label, c.label)-1
        denom += pheramones[small_label][large_label] ** ALPHA * cur_city.distance(c) ** BETA

    r = random.random()
    numer = -1

    while(r > numer):
        r_city = random.choice(unvisited)
        small_label = min(cur_city.label, r_city.label)-1
        large_label = max(cur_city.label, r_city.label)-1
        numer += pheramones[small_label][large_label] ** ALPHA * cur_city.distance(r_city) ** BETA

def unvisited_cities(ant, cities):
    out = list()
    
    for city in cities:
        if city not in ant.tour: out.append(city)

    return out

def main():
    cities = file_to_graph('a280.tsp')
    pheramones = [[INIT_PHER for i in cities] for j in cities]
    ants = reset_ants(cities)

if __name__=="__main__": main()
