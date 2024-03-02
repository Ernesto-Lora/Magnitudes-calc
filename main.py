import subprocess
import sys
import os

try:
    import numpy as pd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
finally:
    import numpy as pd

try:
    import matplotlib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'matplotlib'])
finally:
    import matplotlib


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from ast import main
from distutils.util import change_root
from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import Modules.boatDynamics as boatDynamics
import Modules.shockAbsorber as shockAbsorber
import Modules.springUTS as springUTS

class mainApp:
    def __init__(self, root):
        self.root = root
        self.springApp()

    #################################
    def change_option(self):
        def choice_options():
            text = clicked.get()
            if (text == "Boat Dynamics"):
                self.boatApp()
            elif(text == "Shock Absorber"):
                self.shockApp()
            elif(text == "Spring Ultimate Strength"):
                self.springApp()
        
        options = ["Boat Dynamics",
                "Shock Absorber",
                "Spring Ultimate Strength"]

        clicked = StringVar()
        clicked.set(options[0])

        drop = OptionMenu(self.root, clicked, *options)
        drop.place(x= 0.8*1170, y = 0.1*630)

        change_btn = Button(root, text="Go to App", font = 14, command=choice_options)
        change_btn.place(x= 0.8*1170, y = 0.15*630)
        
    
    #################################

    def boatApp(self):
        #initiate the App
        boatDynamics.boatDinamics(self.root)

        #Chage App options 
        self.change_option()
    
    def shockApp(self):
        shockAbsorber.shockAbs(self.root)

        self.change_option()

    def springApp(self):
        springUTS.springUTS(self.root)
        
        self.change_option()


root = Tk()

mainApp(root=root)

root.mainloop()