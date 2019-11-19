#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FOR STORED DATA, SIMULATED AS REAL TIME

Created on Thu Nov 14 20:32:40 2019

@authors: anmolsingh, rianborah
"""
import data
import serial
import matplotlib.pyplot as plt, numpy as np, time
from matplotlib import style

#style.use("fivethirtyeight")
sim = True

if not sim:
    arduino = serial.Serial('/dev/cu.usbmodem14301')

plt.figure(figsize = (15, 15))

#destinationFileName = 'ccwCircle5.txt'

file = data.ccwCircle

def get_line(x, *args):
    if x:
        data, counter = args[0], args[1]
        arrayName = np.array(data)[:(counter + 1)]
        return (0, arrayName[-1, 0], arrayName[-1, 1])
    else:
        #arguments = *args
        raw = list(map(chr, arduino.readline()))[:-2]
        tabIndices = [i[0] for i in enumerate(raw) if i[1] == '\t']
        index, x, y = [raw[(start + 1):end] for start, end in zip([-1] + tabIndices, tabIndices + [len(raw)])]
        index, x, y = [int(''.join(index)), int(''.join(x)), int(''.join(y))]
        return (index, x, y)

def analyzeData(sensorData, BoolPlot = False):

    #x = []

    #time = np.arange(sensorData)   #make time array for X-Axis

    #for i in sensorData:            #take Y-Vales from sensorData
    #    x.append(int(i[0]))

    #ys = np.array(x, dtype=float64)    #make compatible array out of sensorData
    #xs = np.array(time, dtype=float64)

    xs, ys = np.arange(len(sensorData[:, 0])), sensorData[:, 0]

    def best_fit_slope_and_intercept(xs,ys):            #take two arrays of coordinates
        slope = ((np.mean(xs) * np.mean(ys)) - (np.mean(xs * ys))) / ((np.mean(xs) ** 2) - np.mean(xs**2))
        #statiscal formula

        intercept = np.mean(ys) - (slope * np.mean(xs))
        #statiscal formula

        return slope , intercept

    def checkCicleRot(xs,ys):
        slope = ((np.mean(xs) * np.mean(ys)) - (np.mean(xs * ys))) / ((np.mean(xs) ** 2) - np.mean(xs**2))

        return slope


    slope , intercept = best_fit_slope_and_intercept(xs,ys)     #returns two floats

    regression_line = (slope*xs + intercept)        #forms Y-Values of regression line

    print("Slope: ",slope, "Intercept: ",intercept)

    if slope >= -0.70 and slope <= 1:
        direction = checkCicleRot(xs[0:13],ys[0:13])
        if direction > 0:
            shape = "cwCircle"
        elif direction < 0:
            shape = "ccwCircle"

    elif slope < 0:
        shape = "rightLine"

    elif slope > 4:
        shape = "leftLine"

    else:
        shape = "not inferred"


    if BoolPlot:

        style.use("fivethirtyeight")
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        plt.scatter(np.arange(len(xs)), ys, c='red', label = 'Data Scatter')
        plt.plot(xs,regression_line, c='blue', label='Regression Line')
        plt.legend()
        plt.show()

    return (shape)

if not sim:
    arduino.reset_input_buffer()

    while arduino.in_waiting == 0:
        pass

Data = np.array([[0, 0]])

counter = 0

print("Started getting data for gesture 1")

plt.ylim(-20, 320)

#while arduino.in_waiting > 0:

while True:
    if sim:
        index, x1, y1 = get_line(True, file, counter)
    else:
        index, x1, y1 = get_line(False)
    if counter == 0:
        Data =  np.array([[x1, y1]])
    else:
        Data = np.vstack((Data, np.array([[x1, y1]])))
    counter += 1
    t = np.arange(counter)
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(Data[:, 0], 'b')
    plt.title('X')
    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(Data[:, 1], 'r')

    #plt.plot(t, data[:, 0], 'r', t, data[:, 1], 'b')
    #plt.legend(['X', 'Y'])
    #time.sleep(0.1)
    plt.pause(0.001)
    if sim:
        if counter == len(file):
            break
    else:
        if arduino.in_waiting == 0:
            break

plt.show()

#dataFile = open(destinationFileName, mode = 'w')

#for i in data:
#    dataFile.write(str(i[0]) + " " + str(i[1]) + "\n")

#dataFile.close()
if not sim:
    arduino.reset_input_buffer()
    arduino.close()

print()

print(analyzeData(Data, True))

print()

print("Done")
