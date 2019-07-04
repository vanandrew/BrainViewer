#!/usr/bin/env python
"""
    A simple brain viewing tool with matplotlib

    Just something simple to quickly load and view 3D volumes with python
"""
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,Button

# eliminate toolbar when rendering window
mpl.rcParams['toolbar'] = 'None'

"""
    Defines an updater class so that we can multi-purpose our
    update method for several controls
"""
class Updater:
    # save the control/method to call
    # the method should accept (control,val,dim) as input
    # optional dim argument for dimension limits
    def __init__(self,control,method,dim=None):
        self.control = control
        self.method = method
        self.dim = dim
    # pass the control and value to the method
    def __call__(self,val):
        self.method(self.control,val,self.dim)

"""
    Define methods for control elements
"""
# delete old image and plot new image in axe
def change_image(control,val,dim):
    del control[0].images[0]
    control[0].imshow(control[1](int(val)),origin='lower',cmap='gray')

# decrement sliders
def decrement(control,val,dim):
    new_val = control.val - 1
    if new_val >= 0:
        control.set_val(new_val)

# increment slider (Add dim arg for limit)
def increment(control,val,dim):
    new_val = control.val + 1
    if new_val < dim:
        control.set_val(new_val)

"""
    Brain viewer
"""
class BrainViewer:
    def __init__(self,data,w=12,h=6):
        # Create figure and axes
        self.f = plt.figure(figsize=(w,h))
        self.f.canvas.set_window_title('Brain Viewer')
        self.f.patch.set_facecolor('#BBBBBB')
        self.ax1 = self.f.add_axes([0.06,0.20,0.28,0.75]); self.ax1.axis('off')
        self.ax2 = self.f.add_axes([0.36,0.20,0.28,0.75]); self.ax2.axis('off')
        self.ax3 = self.f.add_axes([0.66,0.20,0.28,0.75]); self.ax3.axis('off')
        plt.subplots_adjust(bottom=0.25)

        # set initial slices
        dim = data.shape
        Sinit = int(dim[0]/2)
        Cinit = int(dim[1]/2)
        Tinit = int(dim[2]/2)

        # Create sliders and buttons
        self.slider1 = Slider(self.f.add_axes([0.1,0.15,0.2,0.03],xticks=[],yticks=[]),
            'S',0,dim[0]-1,valinit=Sinit,valstep=1,valfmt='%1.0f')
        self.slider2 = Slider(self.f.add_axes([0.4,0.15,0.2,0.03],xticks=[],yticks=[]),
            'C',0,dim[1]-1,valinit=Cinit,valstep=1,valfmt='%1.0f')
        self.slider3 = Slider(self.f.add_axes([0.7,0.15,0.2,0.03],xticks=[],yticks=[]),
            'T',0,dim[2]-1,valinit=Tinit,valstep=1,valfmt='%1.0f')
        self.button1down = Button(self.f.add_axes([0.1,0.1,0.1,0.05]),'-', hovercolor='0.9')
        self.button1up = Button(self.f.add_axes([0.2,0.1,0.1,0.05]),'+', hovercolor='0.9')
        self.button2down = Button(self.f.add_axes([0.4,0.1,0.1,0.05]),'-', hovercolor='0.9')
        self.button2up = Button(self.f.add_axes([0.5,0.1,0.1,0.05]),'+', hovercolor='0.9')
        self.button3down = Button(self.f.add_axes([0.7,0.1,0.1,0.05]),'-', hovercolor='0.9')
        self.button3up = Button(self.f.add_axes([0.8,0.1,0.1,0.05]),'+', hovercolor='0.9')

        # add event listeners for each control
        self.slider1.on_changed(Updater((self.ax1,lambda x: data[x,:,:].T),change_image))
        self.slider2.on_changed(Updater((self.ax2,lambda x: data[:,x,:].T),change_image))
        self.slider3.on_changed(Updater((self.ax3,lambda x: data[:,:,x].T),change_image))
        self.button1down.on_clicked(Updater(self.slider1,decrement))
        self.button2down.on_clicked(Updater(self.slider2,decrement))
        self.button3down.on_clicked(Updater(self.slider3,decrement))
        self.button1up.on_clicked(Updater(self.slider1,increment,dim[0]))
        self.button2up.on_clicked(Updater(self.slider2,increment,dim[1]))
        self.button3up.on_clicked(Updater(self.slider3,increment,dim[2]))

        # plot initial slices
        self.ax1.imshow(data[Sinit,:,:].T,origin='lower',cmap='gray')
        self.ax2.imshow(data[:,Cinit,:].T,origin='lower',cmap='gray')
        self.ax3.imshow(data[:,:,Tinit].T,origin='lower',cmap='gray')

"""
    Create BrainViewer object and plot the figure
"""
def plot_brain(data):
    brainviewer = BrainViewer(data)
    plt.show(block=True)

"""
    Command line tool for BrainViewer
"""
if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='View a brain volume (Only does 3D, no 4D yet!)')
    parser.add_argument('volume', help='brain volume to view')
    args = parser.parse_args()

    # load data with nibabel
    import nibabel as nib
    data = nib.load(args.volume).get_fdata()
    plot_brain(data)
