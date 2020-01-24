# Names: Ben Wiegand and Daniel Katz

import numpy as np
import matplotlib.pyplot as plt
import csv
import k_means as km
import random

def read_csv(file_name):
    reader = csv.reader(open(file_name))
    headers = next(reader)
    points = list()
    for row in reader:
        points.append([float(i) for i in row])
    return (headers, points)
    

def centroids_to_graph(centroids, headers, x_axis, y_axis):
    x = list()
    y = list()
    colors = list()

    centroids_x = list()
    centroids_y = list()
    centroids_colors = list()

    for centroid in centroids:
        color = [random.random(),random.random(),random.random()]
        centroids_x.append(centroid.dimensions[x_axis])
        centroids_y.append(centroid.dimensions[y_axis])
        centroids_colors.append(color.copy())
        for point in centroid.points_under_control:
            x.append(point[x_axis])
            y.append(point[y_axis])
            colors.append(color.copy())    
    
    plt.xlabel(headers[x_axis])
    plt.ylabel(headers[y_axis])
    plt.scatter(x,y,c=colors)
    plt.scatter(centroids_x, centroids_y, c=centroids_colors, marker="*", s=150)
    plt.show()


def main():
    file_name = 'transfusion.csv'
    headers, points = read_csv(file_name)
    #points = km.gen_points(4)
    centroids = km.k_means(5, points, point_labels=False)
    print("The headers are {}".format(headers))
    centroids_to_graph(centroids, headers, 0, 1)

if __name__=="__main__": main()
