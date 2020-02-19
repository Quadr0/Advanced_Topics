from tkinter import *
import numpy as np
from digit_recogniton import init_network
from classes_and_utils import *
from PIL import Image

class Paint(object):
    
    # Setup all buttons as well as canvas of TK application.
    # Start loop that runs until application is exited.
    def __init__(self):
        self.root = Tk()

        # Initializes the button that will run the current image 
        # through the model.
        self.run_model_button = Button(self.root, text='run model', command=self.use_model)
        self.run_model_button.grid(row=0, column=0)

        # Initializes the button that will clear the canvas.
        self.clear_canvas_button = Button(self.root, text='clear canvas', command=self.clear_canvas)
        self.clear_canvas_button.grid(row=0,column=1)

        # Initialize the canvas with a white background and 320*320 size.
        self.c = Canvas(self.root, bg='white', width=320, height=320)
        self.c.grid(row=1, columnspan=2)

        self.setup()
        self.root.mainloop()

    # Initialize the class variables.
    def setup(self):
        # Previous mouse coordinates.
        self.old_x = None
        self.old_y = None

        # Pen color, width, and mouse controls.
        self.line_width = 25.0
        self.color = 'black'
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        # Initialize the model and read the weights from a 
        # prevously trained model.
        self.model = init_network()
        weights_from_file(self.model)

        # Code to make sure the data is read in properly and model works by
        # testing accuracy of testing set.
        #self.test_data = dr.read_data(['optdigits-32x32.tes'])[0]
        #accuracy = dr.run_epoch(self.test_data, self.model, backprop=False)
        #print('the accuracy of this training epoch is', accuracy)
        
    # Function to clear the canvas when corresponding button is pressed.
    def clear_canvas(self):
        self.c.delete('all')

    # Function to run image through model and 
    # display the network's guessed number.
    def use_model(self):

        # Save the canvas image with the correct scaling as a postscript file
        # and then open the saved file in a PIL.Image object.
        self.c.postscript(file='runtime_files/pre_scaled_img.eps', pagewidth=319, pageheight=319)
        pre_scaled_img = Image.open('runtime_files/pre_scaled_img.eps')

        # Convert the image to a 2d numpy array.
        pre_scaled_arr = self.img_to_arr(pre_scaled_img)

        # Scale down the array from 320*320 to 32*32.
        scaled_arr = self.down_scale_arr(pre_scaled_arr)

        # Convert from 2d numpy array to flattened python list.
        scaled_2d_flat_list = list(scaled_arr.flatten().tolist())

        # Print the networks guess.
        print('The model guessed the digit is', self.guess_number(scaled_2d_flat_list), '\n')
        
    # Similar to run_single_image function, but no backpropogation and returns
    # the number which network guessed, not 1 or 0 to calculate accuracy.
    def guess_number(self, list_2d):
        for i in range(len(list_2d)):
            self.model[0][i].value = list_2d[i]

        for output_node in self.model[-1]:
            cur_value = 0.0
            for edge in output_node.input_edges:
                cur_value += edge.weight * sigmoid_function(edge.input_node.value)
            output_node.value = cur_value

        return self.model[-1].index(max_node(self.model))
    
    # Convert the PIL.Image to a 2d, 320*320 numpy array and 
    # conver RGB black and white to just 1 or 0.
    def img_to_arr(self, pre_scaled_img):
        out_arr = pre_scaled_img.getdata()

        out_arr = np.array([1 if sum(i) == 0 else 0 for i in out_arr])
        out_arr = np.reshape(out_arr, (320,320))

        return out_arr

    # Take the 320*320 array and convert it into 32*32 array.
    # Print out the 32*32 array to show what the inputted image looks like
    # to the model. 
    def down_scale_arr(self, pre_scaled_arr):
        out_arr = np.reshape(np.zeros(32**2), (32,32)).astype(int)
        
        for i in range(32):
            for j in range(32):
                out_arr[i][j] = self.average_ten_pixels(pre_scaled_arr, i, j)
                

        out = ""
        for line in out_arr: 
            for i in line:
                out += str(i)
            out += '\n'
        print(out)

        return out_arr

    # Sum the 10 pixels in the large arra which represent 1 pixel in the small array.
    # If the sum is bigger than 1 make the small pixel 1, else make the small pixel 0.
    def average_ten_pixels(self, arr, i, j):
        cur_avg = 0
        big_i = i*10
        big_j = j*10

        for x in range(big_i, big_i + 10):
            for y in range(big_j, big_j + 10):
                cur_avg += arr[x][y]

        if cur_avg >= 1: return 1
        else: return 0

    # Function which allows for drawing on the anvas by creating lines
    # every time the canvas refreshes by placing a line between current and
    # old mouse coordinates.
    # Does not draw if the model is just pressed.
    def paint(self, event):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=self.color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    # Reset the previous x and y mouse coordinates everytime the mouse is lifted.
    def reset(self, event):
        self.old_x, self.old_y = None, None

if __name__ == '__main__': Paint()
