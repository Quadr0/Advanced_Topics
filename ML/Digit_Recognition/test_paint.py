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



        #test_data = dr.read_data('optdigits-32x32.tes')
        #model = dr.init_network()
        #dr.weights_from_file(model)
        #accuracy = dr.run_epoch(test_data, model, backprop=False)
        #print('the accuracy of this training epoch is', accuracy)

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 15.0
        self.color = 'black'
        #self.eraser_on = False
        #self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def clear_canvas(self):
        self.c.delete('all')

    def use_model(self):
        self.c.postscript(file='runtime_files/pre_scaled_img.eps')
        pre_scaled_img = Image.open_eps('runtime_files/pre_scaled_img.eps')
        pre_scaled_img.save('runtime_files/raster_canvas.jpg', 'JPEG')
        pre_scaled_arr = self.img_to_arr(pre_scaled_img)
        
    def img_to_arr(self, pre_scaled_img):
        
        out_arr = pre_scaled_img.getdata()
        print(len(out_arr))
        out_arr = np.array([1 if sum(i) == 0 else 0 for i in out_arr])
        #out_arr.reshape(320,320)

        return out_arr


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
