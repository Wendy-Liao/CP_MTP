#!/usr/bin/env python

import sys
import ConfigParser
import threading
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import FirmwareCheck

class MyThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def setup(self, item_name):
        self.item_name = item_name

    def run(self):
        time.sleep(1)  # random sleep to imitate working
        self.trigger.emit(self.item_name)

class Main_UI(QWidget):

    def __init__(self, parent = None):
        super(Main_UI, self).__init__(parent)
        self.config = ConfigParser.ConfigParser()
        self.testlist = []
        self.buttons = []
        self.getTestList()
        self.CreateLayout()
        #self.Connect()
        self.setGeometry(200, 100, 1000, 500)
        #self.showMaximized()
        
    def getTestList(self):
        self.config.read('testlist.config')
        for each_section in self.config.sections():
            if self.config.get(each_section, 'enable') == 'true':
                self.testlist.append(each_section) 
        
    def CreateLayout(self):
        #self.groupBox = QGroupBox(self)
        UI_layout = QVBoxLayout()
        UI_Up_layout = QHBoxLayout()
        UI_Down_layout = QHBoxLayout()
        button_layout = QGridLayout()

        button_layout.setSpacing(0)
        UI_Down_layout.setSpacing(40)
        
        self.result = QTextEdit()

        self.deviceID = QLabel('Serial.No')
        self.deviceIDEdit = QLineEdit()
        #self.deviceIDEdit.setMaximumHeight(100)
        UI_Up_layout.addWidget(self.deviceID)
        UI_Up_layout.addWidget(self.deviceIDEdit)
        
        positions = [(i,j) for i in range(3) for j in range(3)]
        for position, item in zip(positions, self.testlist):
            width = 120
            height = 50
            button = QPushButton("&" + item)
            button.setFixedSize(width,height)
            self.buttons.append(button)
            button_layout.addWidget(button, *position)
        
        for item in self.testlist:
            index = self.config.get(item,'index')
            self.connect(self.buttons[int(index)],SIGNAL("clicked()"),lambda item_name=item:self.BtnActivity(item_name))
        
        UI_Down_layout.addLayout(button_layout)
        UI_Down_layout.addWidget(self.result)
        UI_layout.addLayout(UI_Up_layout)
        UI_layout.addLayout(UI_Down_layout)
        self.setLayout(UI_layout)

    def BtnActivity(self, item_name):
            if item_name == 'FirmwareCheck':
                self.getTestitem(item_name)
                self.test_item = FirmwareCheck.FirmwareCheck()
                self.test_item.show()
                self.StartThread()
            if item_name == 'ImageCheck':
                self.getTestitem(item_name)
                self.test_item = FirmwareCheck.FirmwareCheck()
                self.test_item.show()
                self.StartThread()

    def getTestitem(self, item_name):
        self.item_name = item_name
        self.index = int(self.config.get(item_name, 'index'))

    def StartThread(self):
        self.test_item.show()
        thread = MyThread(self)    
        thread.trigger.connect(self.UpdateUI) 
        thread.setup(self.item_name)            
        thread.start()  

    def UpdateUI(self, item_name):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if(self.test_item.finished):
            self.buttons[self.index].setStyleSheet("background-color: rgb(0, 255, 0)")
            self.result.append(timestamp + ' Done %s test' %item_name)
        else:
            self.result.append(timestamp + ' Start %s test' %item_name)
            self.StartThread()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_ui = Main_UI()
    main_ui.show()
    app.exec_()

