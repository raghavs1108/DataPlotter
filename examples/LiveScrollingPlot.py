import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.GraphicsWindow()
win.setWindowTitle('Live Scrolling Plots')

# 3) Plot icn chunks, adding one new plot curve for every 100 samples
chunkSize = 10000000
# Remove chunks after we have 10
maxChunks = 10
startTime = 0
p5 = win.addPlot(colspan=2)
p5.setLabel('left', "Y Axis", units='')
p5.setLabel('bottom', "X Axis", units='s')
p5.showGrid(x=True, y=True)
p5.setXRange(-10, 0)

win.nextRow()

p6 = win.addPlot(colspan=2)
p6.setLabel('left', "Y Axis", units='')
p6.setLabel('bottom', "X Axis", units='s')
p6.showGrid(x=True, y=True)
p6.setXRange(-10, 0)

win.nextRow()

p7 = win.addPlot(colspan=2)
p7.setLabel('left', "Y Axis", units='')
p7.setLabel('bottom', "X Axis", units='s')
p7.showGrid(x=True, y=True)
p7.setXRange(-10, 0)

curves = []

ptr5 = 0
maxDataCount = 5000000

refreshSpeed = 20

dataArr = []
xVal = []
yVal1 = []
yVal2 = []
yVal3 = []
yVal4 = []
yVal5 = []
yVal6 = []

curve1 = p5.plot(pen = "w")
curve2 = p6.plot(pen = "w")
curve3 = p7.plot(pen = "w")
# curve4 = p5.plot(pen = "y")
# curve5 = p5.plot(pen = "o")
# curve6 = p5.plot(pen = "w")

curves.append(curve1)
curves.append(curve2)
curves.append(curve3)
# curves.append(curve4)
# curves.append(curve5)
# curves.append(curve6)

def update():
    
    
    global curve1, curve2, curve3, p5, ptr5, curves, xVal, yVal1, yVal2, yVal3, yVal4, yVal5, yVal6, startTime, maxDataCount
    f = open("data.txt", "r+");
    d = f.readline()
    
    while d:
        values = d.split(",")
        try:
        	xAcc = float(values[3])
        except Exception as e:
        	print "values[3]: " + str(values)
       	try:
        	yAcc = float(values[4])
        except Exception as e:
        	print "values[4]: " + str(values)
        try:
        	zAcc = float(values[5])
        except Exception as e:
        	print "values[5]: " + str(values)
        try:
        	phonexAcc = float(values[6])
        except Exception as e:
        	print "values[6]: " + str(values)
        try:
        	phoneyAcc = float(values[7])
        except Exception as e:
        	print "values[7]: " + str(values)
        try:
        	phonezAcc = float(values[8])
        except Exception as e:
        	print "values[8]: " + str(values)
        try:
        	datetime = values[12]
	        date = datetime.split(" ")[0]
	        time = datetime.split(" ")[1]

	        hours = int(time.split(":")[0])
	        minutes = int(time.split(":")[1])
	        temp = time.split(":")[2]
	        seconds = int(temp.split(".")[0])
	        milliseconds = float(temp.split(".")[1])
	        milliseconds = (milliseconds)/1000
	        
	        time = float((hours*3600)+(minutes*60)+seconds)
	        now = time + milliseconds
        except Exception as e:
        	print "values[12]: " + str(values)
        # print now
        for c in curves:
            c.setPos(-(now-startTime), 0)
        
        xVal.append(now)

        yVal1.append(phonexAcc)
        yVal2.append(phoneyAcc)
        yVal3.append(zAcc)
        ptr5 += 1
        d = f.readline()

    f.truncate()
    f.close()
    try:
        curve1.setData(x=xVal, y=yVal1)
        curve2.setData(x=xVal, y=yVal2)
        curve3.setData(x=xVal, y=yVal3)
    except Exception as e:
        print e
    if len(xVal) > maxDataCount:
        xVal = xVal[1:]
        yVal1 = yVal1[1:]
        yVal2 = yVal2[1:]
        yVal3 = yVal3[1:]

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(refreshSpeed)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
