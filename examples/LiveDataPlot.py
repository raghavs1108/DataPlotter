# -*- coding: utf-8 -*-
"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

import initExample ## Add path to library (just for examples; you do not need this)

from collections import deque

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import random
import pymysql


conn = pymysql.connect(db="stepdata",host='localhost', user='root', passwd='cdac123')
conn.autocommit(True)
cur = conn.cursor()

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

# p1 = win.addPlot(title="Basic array plotting", y=np.random.normal(size=100))

# p2 = win.addPlot(title="Multiple curves")
# p2.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
# p2.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="Blue curve")
# p2.plot(np.random.normal(size=120)+10, pen=(0,0,255), name="Green curve")

# p3 = win.addPlot(title="Drawing with points")
# p3.plot(np.random.normal(size=100), pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')


# win.nextRow()

# p4 = win.addPlot(title="Parametric, grid enabled")
# x = np.cos(np.linspace(0, 2*np.pi, 1000))
# y = np.sin(np.linspace(0, 4*np.pi, 1000))
# p4.plot(x, y)
# p4.showGrid(x=True, y=True)

# p5 = win.addPlot(title="Scatter plot, axis labels, log scale")
# x = np.random.normal(size=1000) * 1e-5
# y = x*1000 + 0.005 * np.random.normal(size=1000)
# y -= y.min()-1.0
# mask = x > 1e-15
# x = x[mask]
# y = y[mask]
# p5.plot(x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
# p5.setLabel('left', "Y Axis", units='A')
# p5.setLabel('bottom', "Y Axis", units='s')
# p5.setLogMode(x=False, y=False)

# CUSTOM COLOURS
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# END CUSTOM COLOURS

p6 = win.addPlot(title="Updating plot")
# p6.plot(np.random.normal(size=100), pen=(255,0,0))
# p2.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
p6.setLabel('left', "Y Axis", units='')
p6.setLabel('bottom', "X Axis", units='s')
p6.showGrid(x=True, y=True)

curve1 = p6.plot(pen="g")
curve2 = p6.plot(pen="r")
curve3 = p6.plot(pen="b")

data = np.random.normal(size=(1,10))
maxNumberOfValues = 50000;
numberOfValues = 200;
values1 = deque([0])
values2 = deque([0])
ptr = 0
i = 0

refreshSpeed = 20

def xAccelerationArray(data):
    values = []
    for i in data:
        values+=[i[4]]
    return values

def yAccelerationArray(data):
    values = []
    for i in data:
        values+=[i[5]]
    return values

def zAccelerationArray(data):
    values = []
    for i in data:
        values+=[i[6]]
    return values

def phoneYAccelerationArray(data):
    values = []
    for i in data:
        values+=[i[8]]
    return values


def phoneXAccelerationArray(data):
    values = []
    for i in data:
        values+=[i[7]]
    return values

def phoneZAccelerationArray(data):
    values = []
    for i in data:
        values+=[i[9]]
    return values

def stepDetected(data):
    values = []
    for i in data:
        
        values+=[i[9]]
    return values

def update():
    
    global curve1, curve2, data, ptr, p6, i, cur, numberOfValues
    query = "(SELECT * FROM stepdata ORDER BY id DESC LIMIT "+ str(numberOfValues) +") ORDER BY id ASC;"
    cur.execute(query);
    allData = cur.fetchall();
    print(allData[-1][13])

    phoneXAccArr = phoneXAccelerationArray(allData);
    phoneYAccArr = phoneYAccelerationArray(allData);
    phoneZAccArr = phoneZAccelerationArray(allData);
    # p6.setXRange(i -100, i)  # Move the view
    i+=1
    
    # for x in allData:
    #     if x[1] == 1:
    #         line = pg.InfiniteLine(ptr, pen = "y", angle=90, movable=False)
    #         p6.addItem(line)
    #         ptr+=1
    
    curve3.setData(phoneXAccArr)
    curve2.setData(phoneYAccArr)
    curve1.setData(phoneZAccArr)
    p6.enableAutoRange('xy', True)  ## stop auto-scaling after the first data set is plotted
    

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(refreshSpeed)


# win.nextRow()

# p7 = win.addPlot(title="Filled plot, axis disabled")
# y = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(size=1000, scale=0.1)
# p7.plot(y, fillLevel=-0.3, brush=(50,50,200,100))
# p7.showAxis('bottom', False)


# x2 = np.linspace(-100, 100, 1000)
# data2 = np.sin(x2) / x2
# p8 = win.addPlot(title="Region Selection")
# p8.plot(data2, pen=(255,255,255,200))
# lr = pg.LinearRegionItem([400,700])
# lr.setZValue(-10)
# p8.addItem(lr)

# p9 = win.addPlot(title="Zoom on selected region")
# p9.plot(data2)
# def updatePlot():
#     p9.setXRange(*lr.getRegion(), padding=0)
# def updateRegion():
#     lr.setRegion(p9.getViewBox().viewRange()[0])
# lr.sigRegionChanged.connect(updatePlot)
# p9.sigXRangeChanged.connect(updateRegion)
# updatePlot()

## Start Qt event loop unless running in interactive mode or using pyside.

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()