
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, END
import numpy as np


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ringo\Documents\ERNESTO\work\magnitudes\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1177x629")
window.configure(bg = "#FFFFFF")

entryBorders = 5


def k(A, tau):
    return  0.5* A* (tau *998*0.4 + (1 - tau)* 1.29*0.4 )

def magnitudes():
    w = float(Weight.get())
    speed = float( Speed.get() ) #Input in km/h
    speed = 0.2777*speed

    Len = float(Length.get() )
    Rad = float(Radious.get())
    
    A = 0.6*(0.4*Len)*(0.4*Len)
    
    Force.delete(0, END)
    forc = k(A,0.3)*speed**2
    Force.insert(0, round(forc,1))
    
    MotorSpeed.delete(0, END)
    ms = (1.25/2*3.1416) *(speed/(0.75*Rad*np.tan(np.deg2rad(45))))
    MotorSpeed.insert(0,round(ms*60)) #in rev per minute
    



#This is the frame
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 629,
    width = 1177,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

#This is the image
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    235.0,
    61.0,
    image=image_image_1
)



#Title rectangle
canvas.create_rectangle(
    324.0,
    23.0,
    726.0,
    100.0,
    fill="#466695",
    outline="")

#title text
canvas.create_text(
    324.0,
    23.0,
    anchor="nw",
    text="Boat Dynamics",
    fill="#FFFFFF",
    font=("JacquesFrancois Regular", 48 * -1)
)


canvas.create_text(
    46.0,
    185.0,
    anchor="nw",
    text="Weight (kg) ",
    fill="#1E1E1E",
    font=("JacquesFrancois Regular", 32 * -1)
)

Weight = Entry(window,width=13, borderwidth=entryBorders , font=(14))
Weight.place(x=350, y=190)
#e1.pack()



canvas.create_text(
    38.0,
    275.0,
    anchor="nw",
    text="Boat’s Length (m) ",
    fill="#1E1E1E",
    font=("JacquesFrancois Regular", 32 * -1)
)


Length = Entry(window,width=13, borderwidth=entryBorders , font=(14))
Length.place(x=350, y=275+8)


canvas.create_text(
    52.0,
    376.0,
    anchor="nw",
    text="Speed(Km/h)",
    fill="#1E1E1E",
    font=("JacquesFrancois Regular", 32 * -1)
)

Speed = Entry(window,width=13, borderwidth=entryBorders , font=(14))
Speed.place(x=350, y=376+8)


canvas.create_text(
    13.0,
    487.0,
    anchor="nw",
    text="Propeler Radious (m)",
    fill="#1E1E1E",
    font=("JacquesFrancois Regular", 32 * -1)
)
Radious = Entry(window,width=13, borderwidth=entryBorders , font=(14))
Radious.place(x=350, y=487+8)


canvas.create_text(
    554.0,
    185.0,
    anchor="nw",
    text="Motor Speed (rpm) ",
    fill="#1E1E1E",
    font=("JacquesFrancois Regular", 32 * -1)
)

MotorSpeed = Entry(window,width=13, borderwidth=entryBorders , font=(14))
MotorSpeed.place(x=554+300, y=190)

canvas.create_text(
    600.0,
    275.0,
    anchor="nw",
    text="Force (N)",
    fill="#1E1E1E",
    font=("JacquesFrancois Regular", 32 * -1)
)
Force = Entry(window,width=13, borderwidth=entryBorders , font=(14))
Force.place(x=554+300, y=275+8)






ComputeMagnitudes = Button(window, text = "Compute Magnitudes", font= 14,
                           padx = 40, pady = 20, command=magnitudes)
ComputeMagnitudes.place(x=350+500, y=487+8)


window.resizable(False, False)
window.mainloop()
