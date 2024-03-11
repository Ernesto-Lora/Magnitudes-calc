
from tkinter import *
import numpy as np

import sys
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

script_directory = os.path.dirname(os.path.abspath(__file__))
images_dic = os.path.join(script_directory, "Images" )

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        #base_path = os.path.abspath(".")
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)



def kmhToMs(velocity):
    """
    Converts km/h to m/s (velocity magnitude)
    """
    return 0.277778*velocity

class boatDinamics:
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
            file= resource_path( os.path.join("Images", "logo.png" ) ) )
        
        #define all the Entries
        entryBorders = 5
        self.Weight = Entry(self.root,width=13, borderwidth=entryBorders , font=(14))
        self.Speed = Entry(self.root,width=13, borderwidth=entryBorders , font=(14))
        self.Length = Entry(self.root,width=13, borderwidth=entryBorders , font=(14))
        self.Radious = Entry(self.root,width=13, borderwidth=entryBorders , font=(14))

        self.Force = Entry(self.root,width=13, borderwidth=entryBorders , font=(14))
        self.MotorSpeed = Entry(self.root,width=13, borderwidth=entryBorders , font=(14))

        #Buttons
        self.ComputeMagnitudes = Button(self.root, text = "Compute Magnitudes", font= 14,
                                padx = 40, pady = 20, command=self.magnitudes)
        self.show_screen()



    def k(self, A, tau):
            return  0.5* A* (tau *998*0.4 + (1 - tau)* 1.29*0.4 )
    
    def magnitudes(self):
        w = float(self.Weight.get())
        speed = float( self.Speed.get() ) #Input in km/h
        speed = kmhToMs(speed)

        Len = float(self.Length.get() )
        Rad = float(self.Radious.get())
        
        A = 0.6*(0.4*Len)*(0.4*Len)
        
        force = self.k(A,0.3)*speed**2
        ms = (1.25/2*3.1416) *(speed/(0.75*Rad*np.tan(np.deg2rad(45))))


        self.Force.delete(0, END)
        self.Force.insert(0, round(force,1))
        
        self.MotorSpeed.delete(0, END)
        self.MotorSpeed.insert(0,round(ms*60)) #in rev per minute

    def close(self):
        self.root.withdraw()
            
    def show_screen(self):

        #font = "JacquesFrancois Regular"
        font= "bebas neue" 

        self.canvas.place(x = 0, y = 0)
        #This is the image
        
        image= self.canvas.create_image(
            235.0,
            61.0,
            image=self.image_image_1
        )
        self.canvas.update()

        #Title
        self.canvas.create_text(
            400.0,
            50.0,
            anchor="nw",
            text="BOAT DYNAMICS",
            fill="#15bcf0",
            font=(font, 48 * -1)
        )

        #Weigth
        self.canvas.create_text(46.0, 185.0, anchor="nw", text="Weight (kg)",
                           fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Weight.place(x=350, y=190)
        self.Weight.insert(0, 1500)

        # Boat’s Length
        self.canvas.create_text(
            38.0, 275.0, anchor="nw", text="Boat’s Length (m) ",
            fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Length.place(x=350, y=275+8)
        self.Length.insert(0, 3)

        #Speed
        self.canvas.create_text(52.0, 376.0, anchor="nw", text="Speed(Km/h)",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Speed.place(x=350, y=376+8)
        self.Speed.insert(0, 30)

        #Propeller radious

        self.canvas.create_text(
            13.0, 487.0, anchor="nw", text="Propeler Radious (m)",
            fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Radious.place(x=350, y=487+8)
        self.Radious.insert(0, 1.5)

        #Output
        #Motor Speed
        self.canvas.create_text(554.0, 185.0, anchor="nw", text="Motor Speed (rpm) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.MotorSpeed.place(x=554+300, y=190)

        
        self.canvas.create_text(600.0, 275.0, anchor="nw", text="Force (N)",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.Force.place(x=554+300, y=275+8)

        self.ComputeMagnitudes.place(x=350+500, y=487+8)




        

