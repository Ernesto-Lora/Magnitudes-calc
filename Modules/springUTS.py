
from tkinter import *
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from matplotlib.figure import Figure
import io


import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
        #base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def resize_image(image, factor):
    return image.subsample(round(image.width() * factor), round(image.height() * factor))




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
           file= resource_path( os.path.join("Modules", "Images", "logo.png" ) ) )
        
        self.variablesImage = PhotoImage(
            file= resource_path(os.path.join("Modules", "Images", "variables.png" )) )
        
        self.NoSpringWarnigImage = PhotoImage(
            file= resource_path(os.path.join("Modules", "Images", "warning.png" )) )
        

        #Define entries
        entryBorders = 5

        #Input entries
        self.springDiameter, self.wireDiameter, self.activeCoils, self.length, self.UTS = [ Entry(self.root,width=9,
                                                                         borderwidth=entryBorders,
                                                                         font=(14)) for i in range(5)]
        
        self.UTSerror = Entry(self.root, width=7, borderwidth=entryBorders, font=(14))
        
        #output entries
        self.stress, self.factor = [ Entry(self.root,width=13, borderwidth=entryBorders, font=(14)) for i in range(2)]

        #Define buttons 
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

    def NoSpringWarnig(self):
        self.stress.delete(0, END) 
        self.factor.delete(0, END)
        
        new_window = Toplevel()

        new_window.geometry("{}x{}".format(self.NoSpringWarnigImage.width(), self.NoSpringWarnigImage.height()))

        canvas = Canvas(
            new_window,
            bg = "#FFFFFF",
            width=self.NoSpringWarnigImage.width(), height=self.NoSpringWarnigImage.height(),
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.pack(fill="both", expand=True)
        
        canvas.create_image(
            0, 0, anchor= "nw",
            image= self.NoSpringWarnigImage
        )

    
    def Stress(self):

        D = float(self.springDiameter.get())
        D = D*1e-3 # in m
        d = float(self.wireDiameter.get() )
        d = d*1e-3 #in m
        n = float(self.activeCoils.get() )
        l = float(self.length.get() )
        l = l*1e-3 #in m

        diffL = (l- n*d)
        # spring rate
        G = 75e9 #Pa
        c = (G*d**4)/(8*n*D**3)
        force = c*diffL
        #stress 
        s = (8*D*force)/(np.pi*d**3)
        w = D/d
        correctionFactor = (4*w -1)/(4*w-4)+ 0.615/w

        return s*correctionFactor
    
    def StressBerg(self):

        D = float(self.springDiameter.get())
        D = D*1e-3 # in m
        d = float(self.wireDiameter.get() )
        d = d*1e-3 #in m
        n = float(self.activeCoils.get() )
        l = float(self.length.get() )
        l = l*1e-3 #in m

        diffL = (l- n*d)
        # spring rate
        G = 75e9 #Pa
        c = (G*d**4)/(8*n*D**3)
        force = c*diffL
        #stress 
        s = (8*D*force)/(np.pi*d**3)
        w = D/d
        correctionFactor = (w+0.5)/(w-0.75)

        return s*correctionFactor
    
    def calcFactor(self):
        D = float(self.springDiameter.get())
        D = D*1e-3 # in m
        d = float(self.wireDiameter.get() )
        d = d*1e-3 #in m
        l = float(self.length.get() )
        l = l*1e-3
        n = float(self.activeCoils.get() )

        if (l- n*d <= 0 ):
            self.NoSpringWarnig()
            return


        uts = float(self.UTS.get() )
        uts = uts*1e6


        s = self.Stress()

        self.factor.delete(0, END)
        self.factor.insert(0,round( (uts + s)/uts, 3) )
        s = s*1e-6
        self.stress.delete(0, END)
        self.stress.insert(0, round(0.8*s,3)) #at 80%

    def calcErrors(self):
        err1 = 100*float(self.UTSerror.get())/float(self.UTS.get())
        err2 = err1 + 6 #the 6 comes From (0.45 +/- 0.3)
        err3 = 0.01*err1*float(self.UTS.get()) + (np.absolute(self.Stress()-self.StressBerg()))*1e-6
        err3 = 100*err3/(float(self.UTS.get())+self.Stress()*1e-6)
        err4 = err3 + 6

        err1 = 0.01*err1*float(self.UTS.get())
        err2 = 0.01*err2*float(self.UTS.get())*0.45
        err3 = 0.01*err3*(float(self.UTS.get())+self.Stress()*1e-6)
        err4 = 0.01*err4*(float(self.UTS.get())+self.Stress()*1e-6)*0.45

        return round(err1,1), err2, round(err3,1) , round(err4,1)
    
    def plot(self):
        D = float(self.springDiameter.get())
        D = D*1e-3 # in m
        d = float(self.wireDiameter.get() )
        d = d*1e-3 #in m
        l = float(self.length.get() )
        l = l*1e-3
        n = float(self.activeCoils.get() )

        if (l- n*d <= 0 ):
            self.NoSpringWarnig()
            return
          
        uts = float(self.UTS.get() )
        newuts = uts*1e6 + self.Stress()

        newuts = newuts*1e-6

        y0 = np.array([0.9*uts,0.5*uts])
        y1 = np.array([0.9*uts+self.Stress()*1e-6, 0.5*uts + self.Stress()*1e-6])
        x = [1e4,1e5]

        fig, ax = plt.subplots()

        ax.plot(x, y0, label = "Material Fatigue", color = "blue")
        ax.hlines(y=y0[0], xmin=0, xmax=1e04, color='Blue')
        ax.hlines(y=y0[1], xmin=1e5, xmax=1.5e05, color='Blue')

        ax.plot(x, y1, label = "Material + Spring Fatigue", color = "green")
        ax.hlines(y=y1[0], xmin=0, xmax=1e04, color="green")
        ax.hlines(y=y1[1], xmin=1e5, xmax=1.5e05, color="green")

        #ax.set_xticks([])
        ax.set_xticks([0, 1e5], ['1,000', '1,000,000'])
        ax.set_ylabel("Stress Amplitde (Mpa)")
        ax.set_xlabel("cycles")
        ax.set_title("SN Curve")
        ax.legend()
    
        new_window = Toplevel(self.root)
        # Embed the plot in the Tkinter window
        height = 500
        width = 1200
        new_window.geometry("{}x{}".format(width, height))

        canvas = Canvas(
            new_window,
            bg = "#FFFFFF",
            height = height,
            width = width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.pack(fill="both", expand=True)



        canvas_widget  = FigureCanvasTkAgg(fig, master=new_window)
        canvas_widget.draw()
        plot_widget = canvas_widget.get_tk_widget()

        canvas.create_window(0, 0, anchor='nw', window=plot_widget)
        
        entryBorders = 5

        originalUTS, originalFatigueLimit, springUTS, springFatigueLimit = [ Entry(new_window, width=10, borderwidth=entryBorders, font=(14)) for i in range(4)]
        
        originalUTSerror, originalFatigueLimitError, springUTSerror, springFatigueLimitError = [ Entry(new_window, width=7, borderwidth=entryBorders, font=(14)) for i in range(4)]
        font = "bebas neue"

        #original UTS
        xPosVariables = 640
        yRelativePos = 60
        canvas.create_text(xPosVariables, yRelativePos, anchor="nw", text="Material UTS (Mpa)",
                                fill="#1E1E1E", font=(font, 28 * -1)
        )

        canvas.create_text(xPosVariables, yRelativePos+80, anchor="nw", text="Material Fatigue \n Limit (Mpa)",
                                fill="#1E1E1E", font=(font, 28 * -1)
        )

        canvas.create_text(xPosVariables, yRelativePos+2*80+20, anchor="nw", text="Material + Spring \n UTS (Mpa)",
                                fill="#1E1E1E", font=(font, 28 * -1)
        )
        canvas.create_text(xPosVariables, yRelativePos+3*80+30, anchor="nw", text="Material + Spring\n Fatigue Limit (Mpa)",
                                fill="#1E1E1E", font=(font, 28 * -1)
        )

        canvas.create_text(910, 20, anchor="nw", text="Result",
                                fill="#1E1E1E", font=(font, 26 * -1)
        )

        canvas.create_text(1040, 20, anchor="nw", text="Error",
                                fill="#1E1E1E", font=(font, 26 * -1)
        )

        #### Magnitudes

        error1, error2, error3, error4 = self.calcErrors()

        xAdd = 260
        xAddError = 120
        originalUTS.place(x=xPosVariables+xAdd, y=yRelativePos)
        originalUTSval = float(self.UTS.get())
        originalUTS.insert(0, originalUTSval)
        #Error
        originalUTSerror.place(x=xPosVariables+xAdd+xAddError, y=yRelativePos)
        originalUTSerror.insert(0, error1)


        originalFatigueLimit.place(x=xPosVariables+xAdd, y=yRelativePos+80)
        originalFatigueLimit.insert(0, round(0.45*originalUTSval)  )
        #Error
        originalFatigueLimitError.place(x=xPosVariables+xAdd+xAddError, y=yRelativePos+80)
        originalFatigueLimitError.insert(0, error2)

        springUTS.place(x=xPosVariables+xAdd, y=yRelativePos+2*80+35)
        newUTSval = float(self.UTS.get()) + self.Stress()*1e-6
        springUTS.insert(0, round(newUTSval))
        #Error
        springUTSerror.place(x=xPosVariables+xAdd+xAddError, y=yRelativePos+2*80+35)
        springUTSerror.insert(0, error3)

        springFatigueLimit.place(x=xPosVariables+xAdd, y=yRelativePos+3*80+40)
        springFatigueLimit.insert(0, round(0.45*newUTSval) )
        #Error
        springFatigueLimitError.place(x=xPosVariables+xAdd+xAddError, y=yRelativePos+3*80+40)
        springFatigueLimitError.insert(0, error4)


        def on_plot_close():
            fig.clf()  # Clear the figure
            plt.close(fig)  # Close the figure
            new_window.destroy()

        # Set the close event handler for the plot window
        new_window.protocol("WM_DELETE_WINDOW", on_plot_close)

    

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

        self.canvas.create_text(38.0, 225.0+3*80, anchor="nw", text= "(No compression) (mm) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.length.place(x=xButtons, y=190+3*80)
        self.length.insert(0, 40)

        #UTS
        self.canvas.create_text(38.0, 185.0+4.5*80, anchor="nw", text="Ultimate Tensile Strength \nUTS (Spring Material) (MPa) ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.canvas.create_text(580, 150+4.5*80, anchor="nw", text="Error",
                                fill="#1E1E1E", font=(font, 24 * -1)
        )
        self.UTS.place(x=xButtons, y=190+4.5*80)
        self.UTSerror.place(x=xButtons+ 120, y=190+4.5*80)

        self.UTS.insert(0, 980)
        self.UTSerror.insert(0, 30)

        ############## Output
        self.canvas.create_text(700.0, 120.0, anchor="nw", text="Output:",
                                fill="#1E1E1E", font=(font, 32 * -1) )

        # Ultimate stress correction factor
        self.canvas.create_text(xButtons+150, 185.0, anchor="nw", text=" Ultimate Stress Correction Factor ",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.factor.place(x=xButtons+300, y=250)
        self.computeFactorButton.place(x=xButtons+470, y=250)

        # Ultimate stress correction factor
        self.canvas.create_text(xButtons+150, 300, anchor="nw", text=" Stress Absorbed by the Spring (MPa)",
                                fill="#1E1E1E", font=(font, 32 * -1)
        )
        self.stress.place(x=xButtons+300, y=350)


        #Plot text
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


        

