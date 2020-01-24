# Names: Ben Wiegand and Daniel Katz

import math, random, sys

class centroid():
    def __init__(self, label, dimensions):
        self.label = label
        self.dimensions = dimensions
        self.prev_dimensions = [sys.maxsize for i in range(len(dimensions))]
        self.points_under_control = dimensions.copy()


def k_means(num_clusters, points, point_labels=False):
    starting_dims = random.choices(points, k=num_clusters)
    centroids = [centroid(i, val) for i, val in enumerate(starting_dims)]

    while(check_to_stop(centroids)):
        single_iteration(points, centroids)

    if point_labels == True:
        for i in centroids:
            for j in i.points_under_control:
                print(j, i.label)

    return centroids

def single_iteration(points, centroids):
    for centroid in centroids: centroid.points_under_control = [centroid.dimensions.copy()]

    for point in points:
        centroid_dists = [distance(point, centroid) for centroid in centroids]
        min_dist = min(centroid_dists)
        min_index = centroid_dists.index(min_dist)
        centroids[min_index].points_under_control.append(point.copy())

    for centroid in centroids:
        len_points = len(centroid.points_under_control)
        new_dims = [int(sum(x)/len_points) for x in zip(*centroid.points_under_control)]

        centroid.prev_dimensions = centroid.dimensions.copy()
        centroid.dimensions = new_dims
                

def distance(point, centroid):
    out = 0
    for i in range(len(point)):
        out += (point[i] - centroid.dimensions[i]) ** 2
    return math.sqrt(out)


def check_to_stop(centroids):
    for i in centroids: 
        if i.dimensions != i.prev_dimensions: return True
    return False

def gen_points(num_clusters):
    out = list()
    for i in range(num_clusters*10):
        i = i // 10
        out.append([random.randint(i*100, i*100 + 60), random.randint(i*100, i*100 + 60)])

    return out

def main():
    num_clusters = 3
    points = gen_points(num_clusters)
    k_means(num_clusters, points)


if __name__=="__main__": main()
