from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
from threading import Thread
import login_rc
import Main_rc
import Config_rc
import Zigbee_rc
from time import sleep
import serial
import sys
import glob


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

def dev_to_list(power_device):
    return_list=list([])
    return_list.append(power_device.name)
    return_list.append(power_device.speed)
    return_list.append(power_device.vp1)
    return_list.append(power_device.cp1)
    return_list.append(power_device.pp1)
    return_list.append(power_device.qp1)
    return_list.append(power_device.vp2)
    return_list.append(power_device.cp2)
    return_list.append(power_device.pp2)
    return_list.append(power_device.qp2)
    return_list.append(power_device.vp3)
    return_list.append(power_device.cp3)
    return_list.append(power_device.pp3)
    return_list.append(power_device.qp3)
    return_list.append(power_device.key)
    return return_list    

class Power_Device():
    count=0
    def __init__(self, name='', key='', speed=0, vp1=0, cp1=0, pp1=0, qp1=0, vp2=0, cp2=0, pp2=0, qp2=0, vp3=0, cp3=0, pp3=0, qp3=0):
        self.name=name
        self.key=key
        self.speed=speed
        self.vp1=vp1
        self.cp1=cp1
        self.pp1=pp1
        self.qp1=qp1
        self.vp2=vp2
        self.cp2=cp2
        self.pp2=pp2
        self.qp2=qp2
        self.vp3=vp3
        self.cp3=cp3
        self.pp3=pp3
        self.qp3=qp3
        Power_Device.count=Power_Device.count+1
    
    def filter_data(self,value_list):
        if(self.key==value_list[0] and self.key=='s'):
            self.vp1=value_list[1]
            self.cp1=value_list[2]
            self.pp1=value_list[3]
            self.qp1=value_list[4]

        elif (self.key==value_list[0]):
            self.vp1=value_list[1]
            self.vp2=value_list[2]
            self.vp3=value_list[3]

            self.cp1=value_list[4]
            self.cp2=value_list[5]
            self.cp3=value_list[6]

            self.pp1=value_list[7]
            self.pp2=value_list[8]
            self.pp3=value_list[9]

            self.qp1=value_list[10]       
            self.qp2=value_list[11]
            self.qp3=value_list[12]

    def get_count(self):
        return (Power_Device.count)
    
    def print_info(self):
        print('Device_name:%s \nspeed:%s \nPhase1:\tvoltage:%sv\tcurrent:%sA \tP:%sw\tQ:%sw \nPhase2:\tvoltage:%sv\tcurrent:%sA\tP:%sw\tQ:%sw \nPhase3:\tvoltage:%sv\tcurrent:%sA\tP:%sw\tQ:%sw' % (self.name, self.speed, self.vp1, self.cp1, self.pp1, self.qp1, self.vp2, self.cp2, self.pp2, self.qp2, self.vp3, self.cp3, self.pp3, self.qp3))

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):

        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def serial_xbee():
    ser = serial.Serial('COM6', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
    sleep(1)
    count=0
    flag=0
    while True:
        while(count<=100):
            sleep(0.1)
            count=count+1
        if ser.inWaiting() > 0 :
            data = ser.readline()
            if flag==1:
                data = data.decode("utf-8")
                value_list=data.split('*')
                for i in range(0,len(list_Power_Devices)):
                    list_Power_Devices[i].filter_data(value_list)
                    list_Power_Devices[i].print_info()

            flag=1

def test_func():
    data='M1*1*2*3*4*5*6*7*8*9*10*11*12'
    value_list=data.split('*')
    for i in range(0,len(list_Power_Devices)):
        list_Power_Devices[i].filter_data(value_list)
        print(list_Power_Devices[i].name)
        print(list_Power_Devices[i].key)
        print(list_Power_Devices[i].vp1)
        print(list_Power_Devices[i].count)
    

class LoginWindow(QMainWindow):
    username=''
    password=''
    flag = 0
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__()
        loadUi('Login.ui', self)
        
        self.setWindowTitle("Login Page")
        self.pushButton.clicked.connect(self.login_button_clicked)
        self.show()

    def login_button_clicked(self):
        self.username= self.lineEdit_user.text()
        self.password= self.lineEdit_pass.text()
        if(self.username=='a' and self.password == 'a'):
            # self.flag = 1
            self.close()
            self.next = ConfigWindow()
        
class ConfigWindow(QMainWindow):
    table_index = 0
    global list_Power_Devices
    list_Power_Devices =[]
    def __init__(self, *args, **kwargs):
        super(ConfigWindow, self).__init__()
        loadUi('Config.ui', self)
        self.setWindowTitle("Config Page")
        self.AddButton.clicked.connect(self.Add_button_clicked)
        self.SetButton.clicked.connect(self.Set_button_clicked)
        self.LSButton.clicked.connect(self.LS_button_clicked)
        self.ZigbeeButton.clicked.connect(self.Zigbee_button_clicked)
        self.show()
    
    def Add_button_clicked(self):

        Item1=QTableWidgetItem()
        Item1.setText(self.lineEdit_Name.text())
        self.TableWidget.setItem(self.table_index, 0, Item1)
        
        Item2=QTableWidgetItem()
        Item2.setText(self.lineEdit_Key.text())
        self.TableWidget.setItem(self.table_index, 1, Item2)

        power_device_tempt = Power_Device(self.lineEdit_Name.text(),self.lineEdit_Key.text())
        list_Power_Devices.append(power_device_tempt)
        
        # print(list_Power_Devices)
        # print(list_Power_Devices[0])

        rowPosition = self.TableWidget.rowCount()
        self.TableWidget.insertRow(rowPosition)
        # Item1=self.TableWidget.item(self.table_index,0)
        # Item1.setText(self.lineEdit_Name.text())
        # Item2=self.TableWidget.item(self.table_index,1)
        # Item2.setText(self.lineEdit_Key.text())
        self.table_index = self.table_index +1 

    def LS_button_clicked(self):
        self.close()
        self.next = MainWindow()
    def Set_button_clicked(self):
        ####...
        ####...
        self.close()
        self.next = MainWindow()

        Xbee_core = Thread(target=serial_xbee,args=())
        Xbee_core.start()
        # test_core = Thread(target=test_func,args=(self.next))
        # test_core.start()

    def Zigbee_button_clicked(self):
        self.next = ZigbeeWindow()

class ZigbeeWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ZigbeeWindow, self).__init__()
        loadUi('Zigbee.ui', self)
        
        self.setWindowTitle("Zigbee Page")
        self.SetupButton.clicked.connect(self.Setup_button_clicked)
        self.PortcomboBox.addItems(serial_ports())
        self.show()


    def Setup_button_clicked(self):
        command_list = []

        # print(command_list)
        
        Com_name = self.PortcomboBox.currentText()
        
        ser = serial.Serial(Com_name, baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
        if (self.CoordradioButton.isChecked() == True):
            command_file = open('Coordinator_settings.txt',"r")
            for x in command_file:
                command_list.append(x.rstrip('\n'))
        elif (self.EndradioButton.isChecked() == True):
            command_file = open('EndDevice_settings.txt',"r")
            for x in command_file:
                command_list.append(x.rstrip('\n'))
        
        a='+++'
        ser.write(a.encode())
        data = ser.read(3).decode('ascii')

        for i in range(0,len(command_list)):
            ser.write(command_list[i].encode()+b'\x0D')
            data = ser.read(3).decode('ascii')
            sleep(0.1)
            print(data)
        print('FINISH')
        ser.write('ATWR'.encode()+b'\x0D')
        data = ser.read(3).decode('ascii')
        print(data)


# def update_table(tablewindow):
#     while True:
#         for i in range(len(list_Power_Devices)):
#             translated_list=dev_to_list(list_Power_Devices[i])
#             #tablewindow.tableWidget.insertRow(tablewindow.tableWidget.rowCount())
#             for j in range(14):
#                 item=QTableWidgetItem()
#                 item.setText(str(translated_list[j]))
#                 tablewindow.tableWidget.setItem(i, j, item)
#             sleep(0.5)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        loadUi('Main.ui', self)
        self.setWindowTitle("Main Page")
        self.TableButton.clicked.connect(self.Table_button_clicked)
        self.GraphButton.clicked.connect(self.Graph_button_clicked)
        self.show()
    def Table_button_clicked(self):
            # self.close()
            self.next = TableWindow()
            # t_update_table=Thread(target=update_table, args=(self.next,))
            # t_update_table.start()
    def Graph_button_clicked(self):
        # self.close()
        self.next = GraphWindow()

class TableWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(TableWindow, self).__init__()
        loadUi('Table.ui', self)
        self.tableWidget.setRowCount(len(list_Power_Devices))
        self.setWindowTitle("Table Page")
        self.show()
    def update_table(self):
        
        for i in range(len(list_Power_Devices)):
            translated_list=dev_to_list(list_Power_Devices[i])
           #tablewindow.tableWidget.insertRow(tablewindow.tableWidget.rowCount())
            for j in range(14):
                item=QTableWidgetItem()
                item.setText(str(translated_list[j]))
                self.tableWidget.setItem(i, j, item)
            sleep(0.5)
        QTimer.singleShot(10000, self.update_table)
        # Item1=QTableWidgetItem()
        # Item1.setText(self.lineEdit_Name.text())
        # self.TableWidget.setItem(self.table_index, 0, Item1)
        
        # Item2=QTableWidgetItem()
        # Item2.setText(self.lineEdit_Key.text())
        # self.TableWidget.setItem(self.table_index, 1, Item2)

class GraphWindow(QMainWindow):

    def __init__(self):
        
        super(GraphWindow, self).__init__()

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
        self.show()

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




