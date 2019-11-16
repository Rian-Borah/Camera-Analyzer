from coordData import *
from statistics import mean
from numpy import *
from matplotlib import pyplot as plt
from matplotlib import style

'''
Patterns:

    left = increasing slope
    right = decreasing slope
    ccwCircle = cos(decreasing to increasing)
    cwCircle = sin(increasing to decreasing)
'''

            #set plot data
style.use("fivethirtyeight")
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


sensorData = cwCircle         #take data from sensor [array]


x = []
time = range(len(sensorData))   #make time array for X-Axis

for i in sensorData:            #take Y-Vales from sensorData
    x.append(int(i[0]))

ys = array(x, dtype=float64)    #make compatible array out of sensorData
xs = array(time, dtype=float64)


def best_fit_slope_and_intercept(xs,ys):            #take two arrays of coordinates
    slope = ((mean(xs) * mean(ys)) - (mean(xs * ys))) / ((mean(xs) ** 2) - mean(xs**2))
    #statiscal formula

    intercept = mean(ys) - (slope * mean(xs))
    #statiscal formula

    return slope , intercept

def checkCicleRot(xs,ys):
    slope = ((mean(xs) * mean(ys)) - (mean(xs * ys))) / ((mean(xs) ** 2) - mean(xs**2))

    return slope


slope , intercept = best_fit_slope_and_intercept(xs,ys)     #returns two floats

regression_line = [(slope*x) + intercept for x in xs]       #forms Y-Values of regression line

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

print(shape)

plt.scatter(time,x,c='red', label = 'Data Scatter')
plt.plot(xs,regression_line, c='blue', label='Regression Line')


plt.legend()
plt.show()
