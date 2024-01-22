
from mimetypes import init
from tkinter import *

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import os
script_directory = os.path.dirname(os.path.abspath(__file__))
images_dic = os.path.join(script_directory, "Images" )


def kmhToMs(velocity):
    """
    Converts km/h to m/s (velocity magnitude)
    """
    return 0.277778*velocity


class shockAbs:
    def __init__(self, root):
        self.root = root
        
        self.root.geometry("1177x630")
        self.root.configure(bg = "#FFFFFF")
        self.width = 1177
        self.height = 630

        self.canvas = Canvas(
            self.root,
            bg = "#FFFFFF",
            height = 629,
            width = 1177,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.image_image_1 = PhotoImage(
            file= os.path.join(images_dic, "logo.png" ) )

        #Define buttons
        entryBorders = 5
        self.Weight, self.Velocity, self.Distance, self.Slope = [ Entry(self.root,width=13,
                                                                         borderwidth=entryBorders , font=(14)) for i in range(4)]
        self.plot_button = Button(master = self.root,
                            width = 12,
                            height = 2,  
                            command = self.plot,
                            text = "Plot",
                            font=16)
        self.screen()

    def SpringEner(self, kf, xf, kr, xr):
        return( kf *xf**2 + kr*xr**2)
    
    def Force(self, m, ang, v):
        crr = 0.07 #Rolling resistance coeficient
        airDragCoef  = 0.01 #Air drag coefficient
        airDensity = 1.293 #Air density [kg/m^3]
        g =9.8 #gravity constant [m/s^2]
        return m*g*crr*np.cos(ang) + m*g*np.sin(ang)+ 0.5*airDragCoef*airDensity*kmhToMs(v)**2
    
    def plot(self):  
        distance = float(self.Distance.get() )
        slope = float(self.Slope.get())
        weight = float(self.Weight.get())
        velocity = float(self.Velocity.get())

        #Work done by the car
        carWork = self.Force(weight, np.radians(slope), velocity)*distance

        krange = np.linspace(78000, 148000, 100)
        Xrange = np.linspace(0.000, 0.025*7, 100)
        X, Y = np.meshgrid(krange, Xrange)

        Z = (self.SpringEner(87000, Y, X, Y) /carWork)*100

        # Create a figure and axis
        fig, ax = plt.subplots()
    
        # Create a contour plot
        contour_plot = ax.contourf(X, Y, Z, cmap='viridis')

        # Add a colorbar to the plot
        cbar = fig.colorbar(contour_plot, ax=ax)
        cbar.set_label('Energy Harvesting Ratio (%)')

        # Add labels and a title
        ax.set_xlabel('k[N/m]')
        ax.set_ylabel('Shocks stretch[m]')
        ax.set_title('Energy Harvesting Ratio (%) for a car of weight of {} kg,\n that covers a mean distance of {} m with slope of {} Degrees \n going in a velocity of {} km/h'.format(weight,distance,slope, velocity))

    
        new_window = Toplevel()
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
    
    def close(self):
        self.root.withdraw()


    def screen(self):

        self.canvas.place(x = 0, y = 0)

        image= self.canvas.create_image(
            235.0,
            61.0,
            image=self.image_image_1
        )
        
        font = "bebas neue"
        #title text
        self.canvas.create_text(
            400.0,
            50.0,
            anchor="nw",
            text="SHOCK ABSORBER",
            fill="#15bcf0",
            font=(font, 48 * -1)
        )

        #weight
        self.canvas.create_text(46.0, 185.0, anchor="nw", text="Weight (kg) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Weight.place(x=350, y=190)
        self.Weight.insert(0, 1550)

        #velocity
        self.canvas.create_text(46.0, 185.0+80, anchor="nw", text="Velocity (Km/h) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Velocity.place(x=350, y=190+80)
        
        #Distance
        self.canvas.create_text(46.0, 185.0+2*80, anchor="nw", text="Mean Distance (m) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Distance.place(x=350, y=190+2*80)
        
        #Slope
        self.canvas.create_text(38.0, 185.0+3*80, anchor="nw", text="Slope (Degree) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Slope.place(x=350, y=190+3*80)

        #Heatmap Text
        self.canvas.create_text(
                0.5*1170,
                0.35*630,
            anchor="nw",
            text="Show heatmap of \n Energy Harverting Ratio:",
            fill="#1E1E1E",
            font=("JacquesFrancois Regular", 32 * -1)
        )
        
        # button that displays the plot 
        self.plot_button.place(x= 0.55*1170, y = 0.5*630)





        

