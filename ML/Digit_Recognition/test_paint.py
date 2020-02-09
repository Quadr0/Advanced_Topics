from tkinter import *
from PIL import Image
import numpy as np
import digit_recogniton as dr


class Paint(object):

    def __init__(self):
        self.root = Tk()

        #self.choose_size_button = Scale(self.root, from_=1, to=20, orient=HORIZONTAL)
        #self.choose_size_button.grid(row=0, column=4)

        self.run_model_button = Button(self.root, text='run model', command=self.use_model)
        self.run_model_button.grid(row=0, column=0)

        self.clear_canvas_button = Button(self.root, text='clear canvas', command=self.clear_canvas)
        self.clear_canvas_button.grid(row=0,column=1)

        self.c = Canvas(self.root, bg='white', width=320, height=320)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()




    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 18.0
        self.color = 'black'
        #self.eraser_on = False
        #self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        self.model = dr.init_network()
        dr.weights_from_file(self.model)

        #self.test_data = dr.read_data(['optdigits-32x32.tes'])[0]
        #accuracy = dr.run_epoch(self.test_data, self.model, backprop=False)
        #print('the accuracy of this training epoch is', accuracy)
        

    def clear_canvas(self):
        self.c.delete('all')

    def use_model(self):
        self.c.postscript(file='runtime_files/pre_scaled_img.eps', pagewidth=319, pageheight=319)
        pre_scaled_img = Image.open('runtime_files/pre_scaled_img.eps')

        #pre_scaled_img.save('runtime_files/raster_canvas.png', 'png')

        pre_scaled_arr = self.img_to_arr(pre_scaled_img)
        scaled_arr = self.down_scale_arr(pre_scaled_arr)

        scaled_2d_flat_list = list(scaled_arr.flatten().tolist())
        print(self.guess_number(scaled_2d_flat_list))
        

    def guess_number(self, list_2d):
        for i in range(len(list_2d)):
            self.model[0][i].value = list_2d[i]

        for output_node in self.model[-1]:
            cur_value = 0.0
            for edge in output_node.input_edges:
                cur_value += edge.weight * dr.sigmoid_function(edge.input_node.value)
            output_node.value = cur_value

        return self.model[-1].index(dr.max_node(self.model))
    
    def img_to_arr(self, pre_scaled_img):
        out_arr = pre_scaled_img.getdata()

        #print(len(out_arr))

        out_arr = np.array([1 if sum(i) == 0 else 0 for i in out_arr])
        out_arr = np.reshape(out_arr, (320,320))

        #print(out_arr.shape)
        #print([i for i in out_arr[:10]])

        return out_arr

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

    def average_ten_pixels(self, arr, i, j):
        cur_avg = 0
        big_i = i*10
        big_j = j*10

        for x in range(big_i, big_i + 10):
            for y in range(big_j, big_j + 10):
                cur_avg += arr[x][y]

        if cur_avg > 1: return 1
        else: return 0
        


    #def use_eraser(self):
    #    self.activate_button(self.eraser_button, eraser_mode=True)

    #def activate_button(self, some_button, eraser_mode=False):
    #    self.active_button.config(relief=RAISED)
    #    some_button.config(relief=SUNKEN)
    #    self.active_button = some_button
    #    self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.line_width
        paint_color = self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()
