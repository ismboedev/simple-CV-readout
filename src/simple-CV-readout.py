#!/bin/python3
# =========================================================================== #


# =========================================================================== #
# ======================= import needed modules ============================= #

import math         # for the number pi
import os           # for path check
import sys          # for exit
# import tkinter modules for GUI
import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

# =========================================================================== #
# ========================== define functions =============================== #


# show warning message
def alert( str ):
    temp = tkinter.Tk()
    temp.withdraw()
    messagebox.showinfo( "oh", str )
    temp.destroy()


# browse for files
def selectdata():
    askcvfilename = askopenfilename()
    global cvfilename
    cvfilename = askcvfilename

def selecthistory():
    askhistoryfilename = askopenfilename()
    global historyfilename
    historyfilename = askhistoryfilename


# end the window
def end():
    global amplitude
    amplitude = float(E1.get())
    mainWindow.quit()


# =========================================================================== #
# =================== start mainWindow with Buttons ========================= #


mainWindow = tkinter.Tk()
mainWindow.wm_title( "simple-CV-readout" )
#mainWindow.geometry( "190x90" )


F1 = tkinter.Frame( mainWindow )
F2 = tkinter.Frame( mainWindow )
F3 = tkinter.Frame( mainWindow )
F4 = tkinter.Frame( mainWindow )


B1 = tkinter.Button( F1, text = "Data File", width = 10, 
        command = selectdata )

B2 = tkinter.Button( F1, text = "History File", width = 10,
        command = selecthistory )

B3 = tkinter.Button( F3, text = "Calculate\n& Exit", width = 10,
        command = end )



L1 = tkinter.Label( mainWindow, text = "Select your Files below:" )

L2 = tkinter.Label( F2, text = "Amplitude:" )
L3 = tkinter.Label( F2, text = "A" )


E1 = tkinter.Entry ( F2, width = 5)

E1.insert(0, "0.01")


# =========================================================================== #

F1.pack( fill = tkinter.BOTH )
F2.pack( fill = tkinter.BOTH )
F3.pack( fill = tkinter.BOTH )


B1.pack( side = tkinter.LEFT )
B2.pack( side = tkinter.LEFT )

L2.pack( side = tkinter.LEFT )
L3.pack( side = tkinter.RIGHT )
E1.pack( side = tkinter.RIGHT )

B3.pack( side = tkinter.RIGHT )


# start the loop
mainWindow.mainloop()
mainWindow.destroy()


# from here, the Calculate and Exit Button was pressed

# =========================================================================== #
# ==================== Error check if files where chosen ==================== #


# if calculate is pressed without selecting a file
if not 'cvfilename' in globals():
    alert( "No Data file selected" )
    sys.exit( "no data file selected" )

# if calculate is pressed but the file selection was aborted:
if ( cvfilename == "" ) or ( cvfilename == () ):
    alert( "NO! Try not! DO or DO NOT,\nThere is no try." ) 
    sys.exit( "no data file selected" )



if not 'historyfilename' in globals():
    alert( "no history file selected" )
    sys.exit( "no history file selected" )

if ( historyfilename == "" ) or ( historyfilename == () ):
    alert( "if you forget your history, you can't know your future (data)!" )
    sys.exit( "no history file selected" )


# =========================================================================== #
# =========================== read CV data ================================== #


cv_file = open( cvfilename, mode = 'r' )
cv_data = cv_file.read()
cv_file.close()

# create list witch each element a row
cv_row = cv_data.splitlines()

# read number of measurements
num_chunks = int( cv_row[-1].split(';')[0] )



# =========================================================================== #
# =========================== read history data ============================= #


history_file = open( historyfilename, mode='r' )
history = history_file.read()
history_file.close()

history_row = history.splitlines()

names = []
for g in range ( 0, num_chunks+1 ):
    names.append( history_row[g+1].split(';')[3] )


# =========================================================================== #
# =========================== read data path ================================ #


letter = 0
index = 0
size = 0
path = ''
for h in reversed( cvfilename ):
    if h == '/':
        letter += 1
        size = len( cvfilename ) - index
        for x in range( size ):
            path = path + cvfilename[x]
        break
    index += 1


# =========================================================================== #
# ======================== calculate capacitance ============================ #
# ======================== and write output files =========================== #


for i in range( 0, num_chunks+1 ):

    gridline = cv_row[ 11 + 29*i ]
    freqline = cv_row[ 8 + 29*i ]
    rline = cv_row[ 15 + 29*i ]
    phaseline = cv_row[ 12 + 29*i ]
    size = int( gridline.split(';')[2] )

    grid = []
    for j in range ( 4, size+4 ):
        grid.append( gridline.split(';')[j] )

    freq = []
    for j in range (4, size + 4 ):
        freq.append( freqline.split(';')[j] )

    phase = []
    for j in range (4, size + 4 ):
        phase.append( phaseline.split(';')[j] )

    r = []
    for j in range (4, size + 4 ):
        r.append( rline.split(';')[j] )


    capacitance = []

    for k in range ( 0, size ):
        capacitance.append( str( float(r[k]) / ( 2 * math.pi * float(freq[k]) * amplitude ) ) )

    # create output files
    if not os.path.exists( path + "CV_output" ):
        os.makedirs( path + "CV_output" )


    filename = "CV_chunk_" + str(i) + "_" + names[i] + ".dat"
    
    output = open( path + "CV_output/" + filename, mode='w' )

    output.write( "voltage\t" + "capacitance\t" + "frequency\t" + "r\t" + "phase\n" )
    output.write( "V\t" + "F\t" + "Hz\t" + "A\t" + "°\n" )
    
    for l in range ( 0, size ):
        output.write( grid[l] + "\t" + capacitance[l] + "\t" + freq[l] + "\t" +
                r[l] + "\t" + phase[l] + "\n" )

    output.close()


# =========================================================================== #
