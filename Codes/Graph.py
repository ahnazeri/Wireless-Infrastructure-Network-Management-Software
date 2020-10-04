from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import random

t_1=[]
cosinus_signal_1=[]
sinus_signal_1=[]
t_2=[]
cosinus_signal_2=[]
sinus_signal_2=[]
t_3=[]
cosinus_signal_3=[]
sinus_signal_3=[]
t_4=[]
cosinus_signal_4=[]
sinus_signal_4=[]
class GraphWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("Graph.ui",self)

        self.setWindowTitle("Graph Page")

        self.Plot1Button.clicked.connect(self.update_animation1)
        self.Plot2Button.clicked.connect(self.update_animation2)
        self.Plot3Button.clicked.connect(self.update_animation3)
        self.Plot4Button.clicked.connect(self.update_animation4)
        # self.addToolBar(NavigationToolbar(self.MplWidget1.canvas, self))
        # self.addToolBar(NavigationToolbar(self.MplWidget2.canvas, self))
        # self.addToolBar(NavigationToolbar(self.MplWidget3.canvas, self))
        # self.addToolBar(NavigationToolbar(self.MplWidget4.canvas, self))

    def update_animation1(self):
        t_1.clear()
        cosinus_signal_1.clear()
        sinus_signal_1.clear()
        self.ani1 = animation.FuncAnimation(self.MplWidget1, self.update_axes1, 
        self.update_graph1, interval=500, repeat=False)

        self.MplWidget1.canvas.draw()
    def update_animation2(self):
        self.ani2 = animation.FuncAnimation(self.MplWidget2, self.update_axes2, 
        self.update_graph2, interval=500, repeat=False)
        t_2.clear()
        cosinus_signal_2.clear()
        sinus_signal_2.clear()
        self.MplWidget2.canvas.draw() 

    def update_animation3(self):
        self.ani3 = animation.FuncAnimation(self.MplWidget3, self.update_axes3, 
        self.update_graph3, interval=500, repeat=False)
        t_3.clear()
        cosinus_signal_3.clear()
        sinus_signal_3.clear()
        self.MplWidget3.canvas.draw()        

    def update_animation4(self):
        self.ani4 = animation.FuncAnimation(self.MplWidget4, self.update_axes4, 
        self.update_graph4, interval=500, repeat=False)
        t_4.clear()
        cosinus_signal_4.clear()
        sinus_signal_4.clear()
        self.MplWidget4.canvas.draw()        
    
    def update_graph1(self):
        t1 = 1
        while True:

            fs = 500
            f=10

            t1=t1+0.1
            cosinus_signal1 = np.cos(2 * np.pi* t1/2)
            sinus_signal1 = np.sin(2 * np.pi * t1/2)
            yield t1, cosinus_signal1, sinus_signal1
        # self.MplWidget1.canvas.axes.clear()
        # self.MplWidget1.canvas.axes.plot(t, cosinus_signal)
        # self.MplWidget1.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget1.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        # self.MplWidget1.canvas.axes.set_title('Cosinus - Sinus Signal')
        # self.MplWidget1.canvas.draw()

        # self.MplWidget2.canvas.axes.clear()
        # self.MplWidget2.canvas.axes.plot(t, cosinus_signal)
        # self.MplWidget2.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget2.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        # self.MplWidget2.canvas.axes.set_title('Cosinus - Sinus Signal')
        # self.MplWidget2.canvas.draw()

        # self.MplWidget3.canvas.axes.clear()
        # self.MplWidget3.canvas.axes.plot(t, cosinus_signal)
        # self.MplWidget3.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget3.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        # self.MplWidget3.canvas.axes.set_title('Cosinus - Sinus Signal')
        # self.MplWidget3.canvas.draw()

        # self.MplWidget4.canvas.axes.clear()
        # self.MplWidget4.canvas.axes.plot(t, cosinus_signal)
        # self.MplWidget4.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget4.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        # self.MplWidget4.canvas.axes.set_title('Cosinus - Sinus Signal')
        # self.MplWidget4.canvas.draw()
    def update_graph2(self):
        t1 = 1
        while True:

            fs = 500
            f=10

            t1=t1+0.1
            cosinus_signal1 = np.cos(2 * np.pi* t1/2)
            sinus_signal1 = np.sin(2 * np.pi * t1/2)
            yield t1, cosinus_signal1, sinus_signal1

    def update_graph3(self):
        t1 = 1
        while True:

            fs = 500
            f=10

            t1=t1+0.1
            cosinus_signal1 = np.cos(2 * np.pi* t1/2)
            sinus_signal1 = np.sin(2 * np.pi * t1/2)
            yield t1, cosinus_signal1, sinus_signal1

    def update_graph4(self):
        t1 = 1
        while True:

            fs = 500
            f=10

            t1=t1+0.1
            cosinus_signal1 = np.cos(2 * np.pi* t1/2)
            sinus_signal1 = np.sin(2 * np.pi * t1/2)
            yield t1, cosinus_signal1, sinus_signal1
    
    def update_axes1(self, update):
        t_1.append(update[0])
        cosinus_signal_1.append(update[1])
        sinus_signal_1.append(update[2]) 
        if(len(t_1)>=20):
            t_1.pop(0)
            cosinus_signal_1.pop(0)
            sinus_signal_1.pop(0)

        self.MplWidget1.canvas.axes.clear()
        self.MplWidget1.canvas.axes.plot(t_1, cosinus_signal_1, marker='o')
        self.MplWidget1.canvas.axes.plot(t_1, sinus_signal_1,linestyle='--', marker='o')
        
    def update_axes2(self, update):
        t_2.append(update[0])
        cosinus_signal_2.append(update[1])
        sinus_signal_2.append(update[2]) 
        if(len(t_2)>=20):
            t_2.pop(0)
            cosinus_signal_2.pop(0)
            sinus_signal_2.pop(0)

        self.MplWidget2.canvas.axes.clear()
        self.MplWidget2.canvas.axes.plot(t_2, cosinus_signal_2, marker='o')
        self.MplWidget2.canvas.axes.plot(t_2, sinus_signal_2,linestyle='--', marker='o')

    def update_axes3(self, update):
        t_3.append(update[0])
        cosinus_signal_3.append(update[1])
        sinus_signal_3.append(update[2]) 
        if(len(t_3)>=20):
            t_3.pop(0)
            cosinus_signal_3.pop(0)
            sinus_signal_3.pop(0)
        self.MplWidget3.canvas.axes.clear()
        self.MplWidget3.canvas.axes.plot(t_3, cosinus_signal_3, marker='o')
        self.MplWidget3.canvas.axes.plot(t_3, sinus_signal_3,linestyle='--', marker='o')

    def update_axes4(self, update):
        t_4.append(update[0])
        cosinus_signal_4.append(update[1])
        sinus_signal_4.append(update[2]) 
        if(len(t_4)>=20):
            t_4.pop(0)
            cosinus_signal_4.pop(0)
            sinus_signal_4.pop(0)

        self.MplWidget4.canvas.axes.clear()
        self.MplWidget4.canvas.axes.plot(t_4, cosinus_signal_4, marker='o')
        self.MplWidget4.canvas.axes.plot(t_4, sinus_signal_4,linestyle='--', marker='o')



app = QApplication([])
window = GraphWidget()
window.show()
app.exec_()