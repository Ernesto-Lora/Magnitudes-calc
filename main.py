
from ast import main
from distutils.util import change_root
from tkinter import *
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import Modules.boatDynamics as boatDynamics
import Modules.shockAbsorber as shockAbsorber

class mainApp:
    def __init__(self, root):
        self.root = root
        self.boatApp()

    def boatApp(self):
        boatDynamics.boatDinamics(self.root)
        change_btn = Button(root, text="Shock Absorber", font = 14, command=self.shockApp)
        change_btn.place(x= 0.8*1170, y = 0.1*630)
    
    def shockApp(self):
        shockAbsorber.shockAbs(self.root)
        change_btn = Button(root, text="Boat", font = 14, command=self.boatApp)
        change_btn.place(x= 0.8*1170, y = 0.1*630)



root = Tk()

mainApp(root=root)

root.mainloop()