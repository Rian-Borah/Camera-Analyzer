import datetime as dt
import tkinter as tk
import tkinter.font as tkFont

from ArdSerial import best_fit_slope_and_intercept, checkCicleRot

import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


###############################################################################
# Parameters and global variables

# Parameters
update_interval = 10 # Time (ms) between polling/animation updates

# Declare global variables
root = None
dfont = None
frame = None
canvas = None
ax1 = None
ax2 = None
RealTimeVisible = None


# Global variable to remember various states
fullscreen = False

###############################################################################
# Functions

# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)

# Return to windowed mode
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)

# Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 15)))
    dfont.configure(size=new_size)


def plotRegress(xs,ys):
    slope , intercept = best_fit_slope_and_intercept(xs,ys)     #returns two floats
    regression_line = (slope*xs + intercept)        #forms Y-Values of regression line
    ax2.clear()
    ax2.scatter(np.arange(len(xs)), ys, c='red', label = 'Data Scatter')
    ax2.plot(xs,regression_line, c='blue', label='Regression Line')


def shape(xs,ys):
    slope , intercept = best_fit_slope_and_intercept(xs,ys)
    if slope >= -0.70 and slope <= 1:
        direction = checkCicleRot(xs[0:13],ys[0:13])
        if direction > 0:
            shape = "cw Circle"
        elif direction < 0:
            shape = "ccw Circle"

    elif slope < 0:
        shape = "Right Line"

    elif slope > 4:
        shape = "Left Line"

    else:
        shape = "Not Inferred"

    return (shape)


# This function is called periodically from FuncAnimation
def animate(xs,ys):
    color = 'tab:blue'
    ax1.clear()
    ax1.plot(xs, ys, 0,label='Sensor Data', linewidth=2, color=color)


# Dummy function prevents segfault
def _destroy(event):
    pass

###############################################################################
# Main script

# Create the main window
root = tk.Tk()
root.title("Sensor Dashboard")

# Create the main container
frame = tk.Frame(root)
frame.configure(bg='white')

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Create figure for plotting
figRealTime = figure.Figure(figsize=(2, 2))
figRealTime.subplots_adjust(left=0.1, right=0.8)
ax1 = figRealTime.add_subplot(1, 1, 1)

# Instantiate a new set of axes that shares the same x-axis
figRegress = figure.Figure(figsize=(1,1))
ax2 = figRegress.add_subplot(1,1,1)

# Empty x and y lists for storing data to plot later
xs = []
ys = []


# Create dynamic font for text
dfont = tkFont.Font(size=-24)

# Create a Tk Canvas widget out of our figure
canvasRealTime = FigureCanvasTkAgg(figRealTime, master=frame)
canvas_plot_RealTime = canvasRealTime.get_tk_widget()

canvasRegress = FigureCanvasTkAgg(figRegress, master=frame)
canvas_plot_Regress = canvasRegress.get_tk_widget()
# Create other supporting widgets
label_shape = tk.Label(frame, textvariable=shape(xs,ys), font=dfont, bg='white')
#shape = temp_c
button_quit = tk.Button(    frame,
                            text="Quit",
                            font=dfont,
                            command=root.destroy)
button_regress = tk.Button(    frame,
                            text="Regress",
                            font=dfont,
                            command=root.plotRegress)

# Lay out widgets in a grid in the frame
canvas_plot_RealTime.grid(   row=0,
                    column=0,
                    rowspan=5,
                    columnspan=4,
                    sticky=tk.W+tk.E+tk.N+tk.S)
canvas_plot_Regress.grid(   row=1,
                    column=1,
                    rowspan=2,
                    columnspan=2,
                    sticky=tk.W+tk.E+tk.N+tk.S)

label_shape.grid(row=0, column=4, columnspan=2)
button_quit.grid(row=5, column=4, columnspan=2)

# Add a standard 5 pixel padding to all widgets
for w in frame.winfo_children():
    w.grid(padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
for i in range(0, 5):
    frame.rowconfigure(i, weight=1)
for i in range(0, 5):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Call empty _destroy function on exit to prevent segmentation fault
root.bind("<Destroy>", _destroy)

# Initialize our sensors

# Call animate() function periodically
fargs = (xs,ys)
ani = animation.FuncAnimation(  figRealTime,
                                animate,
                                fargs=fargs,
                                interval=update_interval)

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()
