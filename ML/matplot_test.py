import matplotlib.pyplot as plt
from random import randint

x = [] # will hold random x values
y = [] # will hold random y values
colors = [] # will hold color values corresponding to each data point

# generate a random cluster of data
for _ in range(100):
    x.append(randint(0,10))
    y.append(randint(50,100))
    colors.append([0.2,0.6,0.2])
# generate a random cluster of data
for _ in range(100):
    x.append(randint(100,150))
    y.append(randint(50,100))
    colors.append([0.2,0.2,0.6])
# generate a random cluster of data
for _ in range(100):
    x.append(randint(40,60))
    y.append(randint(10,30))
    colors.append([0.6,0.2,0.2])

# scatter the data with corresponding colors
plt.scatter(x,y,c=colors) # c is an optional parameter for the color vector
plt.show() # need to call in order to show the plot
