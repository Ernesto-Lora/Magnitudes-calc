
from tkinter import *

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from matplotlib.figure import Figure
import io

import os
script_directory = os.path.dirname(os.path.abspath(__file__))
images_dic = os.path.join(script_directory, "Images" )


class springUTS:
    def __init__(self, root):
        self.root = root
        
        self.root.geometry("1177x630")
        self.root.configure(bg = "#FFFFFF")
        self.width = 1177
        self.height = 650

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
        
        self.variablesImage = PhotoImage(
            file= os.path.join(images_dic, "variables.png" ) )

        #Define buttons
        entryBorders = 5
        self.stress, self.springDiameter, self.wireDiameter, self.activeCoils, self.length, self.UTS, self.factor = [ Entry(self.root,width=13,
                                                                         borderwidth=entryBorders,
                                                                           font=(14)) for i in range(7)]
        self.plot_button = Button(master = self.root,
                            width = 12,
                            height = 2,  
                            command = self.plot,
                            text = "Plot",
                            font=16)
        
        self.showVariables = Button(master = self.root,
                            width = 20,
                            height = 1,  
                            command = self.showVariablesImage,
                            text = "Spring Variables Diagram",
                            font=14)
         
        self.computeFactorButton = Button(master = self.root,
                            width = 12,
                            height = 1,  
                            command = self.calcFactor,
                            text = "Compute",
                            font=14)

        self.showScreen()
    
    def Stress(self):
        D = float(self.springDiameter.get())
        D = D*1e-3 # in m
        d = float(self.wireDiameter.get() )
        d = d*1e-3 #in m
        n = float(self.activeCoils.get() )
        l = float(self.length.get() )
        l = l*1e-2

        diffL = 0.8*(l- n*d)
        # spring rate
        G = 75e9 #Pa
        c = (G*d**4)/(8*n*D**3)
        force = c*diffL
        #stress 
        s = (8*D*force)/(np.pi*d**3)
        w = D/d
        correctionFactor = (4*w -1)/(4*w-4)+ 0.615/w

        return s*correctionFactor
    
    def calcFactor(self):
        uts = float(self.UTS.get() )
        uts = uts*1e6
        s = self.Stress()

        self.factor.delete(0, END)
        self.factor.insert(0,round( (uts + s)/uts, 3) )
        s = s*1e-6
        self.stress.delete(0, END)
        self.stress.insert(0, round(s,3)) 
    
    def plot(self):  
        uts = float(self.UTS.get() )
        newuts = uts*1e6 + self.Stress()

        newuts = newuts*1e-6

        y0 = np.array([0.9*uts,0.5*uts])
        y1 = np.array([0.9*uts+self.Stress()*1e-6, 0.5*uts + self.Stress()*1e-6])
        x = [1e4,1.0e5]

        fig, ax = plt.subplots()

        ax.plot(x, y0, label = "Material Fatigue", color = "blue")
        ax.hlines(y=y0[0], xmin=0, xmax=1e04, color='Blue')
        ax.hlines(y=y0[1], xmin=1e5, xmax=1.5e05, color='Blue')

        ax.plot(x, y1, label = "Material + Spring Fatigue", color = "green")
        ax.hlines(y=y1[0], xmin=0, xmax=1e04, color="green")
        ax.hlines(y=y1[1], xmin=1e5, xmax=1.5e05, color="green")

        #plt.xlabel("Cycles")
        ax.set_xticks([])
        ax.set_ylabel("Stress Amplitde (Mpa)")
        ax.set_xlabel("cycles")
        ax.set_title("SN Curve")
        ax.legend()
    
        new_window = Toplevel()
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def showVariablesImage(self):  
    
        new_window = Toplevel()
        new_window.geometry("700x400")

        canvas = Canvas(
            new_window,
            bg = "#FFFFFF",
            height = 400,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.pack(fill="both", expand=True)
        
        canvas.create_image(
            0.6*600,
            0.5*400,
            image= self.variablesImage
        )
        # Embed the plot in the Tkinter window

        #canvas_widget = canvas.get_tk_widget()
        #canvas_widget.pack()
    
    def close(self):
        self.root.withdraw()


    def showScreen(self):

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
            text="SPRING UTS",
            fill="#15bcf0",
            font=(font, 48 * -1)
        )

        xButtons = 450

        #Input
        self.canvas.create_text(47.0, 120.0, anchor="nw", text="Input Variables:",
                                fill="#1E1E1E", font=(font, 32 * -1) )
        #Show variables
        self.showVariables.place(x=300.0, y=120.0)


        #Spring diameter D 
        self.canvas.create_text(46.0, 185.0, anchor="nw", text="Spring Diameter D (mm) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.springDiameter.place(x=xButtons, y=190)
        self.springDiameter.insert(0, 11.20)

        #wire diameter d
        self.canvas.create_text(46.0, 185.0+80, anchor="nw", text="Wire Diameter d (mm) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.wireDiameter.place(x=xButtons, y=190+80)
        self.wireDiameter.insert(0, 0.80)
        
        #Active Coils
        self.canvas.create_text(46.0, 185.0+2*80, anchor="nw", text="Number of Active Coils n",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )

        self.activeCoils.place(x=xButtons, y=190+2*80)
        self.activeCoils.insert(0, 20)
        
        #length
        fig = Figure(figsize=(4, 1), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, r"Spring Length $L_0$", fontsize=22, ha='center')
        ax.axis('off')  # Turn off the axes

        # Convert the figure to an image
        buf = io.BytesIO()
        FigureCanvas(fig).print_png(buf)
        buf.seek(0)
        img = PhotoImage(data=buf.read())
        # Display the image on the canvas
        self.canvas.create_image(20, 170.0+3*80, anchor=NW, image=img)

        self.canvas.create_text(38.0, 225.0+3*80, anchor="nw", text= "(No compression) (cm) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.length.place(x=xButtons, y=190+3*80)
        self.length.insert(0, 5)

        #UTS
        self.canvas.create_text(38.0, 185.0+4.5*80, anchor="nw", text="Ultimate Tensile Strength \nUTS (Spring Material) (MPa) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.UTS.place(x=xButtons, y=190+4.5*80)
        self.UTS.insert(0, 980)

        ############## Output

        #Input
        self.canvas.create_text(700.0, 120.0, anchor="nw", text="Output:",
                                fill="#1E1E1E", font=(font, 32 * -1) )

        # Ultimate stress correction factor
        self.canvas.create_text(xButtons+150, 185.0, anchor="nw", text=" Ultimate Stress Correction Factor ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.factor.place(x=xButtons+300, y=250)
        self.computeFactorButton.place(x=xButtons+450, y=250)

        # Ultimate stress correction factor
        self.canvas.create_text(xButtons+150, 300, anchor="nw", text=" Stress Absorbed by the Spring (MPa)",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.stress.place(x=xButtons+300, y=350)


        #Plot
        self.canvas.create_text(
                0.6*1170,
                0.65*630,
            anchor="nw",
            text="Show SN Curve",
            fill="#1E1E1E",
            font=("JacquesFrancois Regular", 32 * -1)
        )
        
        # button that displays the plot 
        self.plot_button.place(x= 0.62*1170, y = 0.75*630)




        

