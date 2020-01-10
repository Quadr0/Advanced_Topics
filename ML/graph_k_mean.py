import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import k_means as km

def read_csv(file_name):
    reader = csv.reader(open(file_name))
    next(reader)
    

def main():
    file_name = './transfusion.csv'
    points = read_csv(file_name)
    print(points)
    km.k_means(5, points)

if __name__=="__main__": main()
