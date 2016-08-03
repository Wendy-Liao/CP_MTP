#!/usr/bin/env python

import sys
import subprocess
import time
import threading
import ConfigParser
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class FirmwareCheck(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
   
        self.Init()
        self.UI()
        self.message()
        self.time1()

    def Init(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('testlist.config')
        self.timer = QTimer(self)
        self.timeout = int(self.config.get('FirmwareCheck', 'Timeout'))
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.time1)
        self.timer.start(1000)
    
    def UI(self):
        self.setWindowTitle("FirmwareCheck!")
        self.messageLayout = QVBoxLayout()
        self.setGeometry(200, 100, 500, 500)
        self.msg = QTextEdit()
        self.time = QLabel('Time: ' + str(self.timeout))
        self.messageLayout.addWidget(self.time)
        self.messageLayout.addWidget(self.msg)
        self.setLayout(self.messageLayout)

        
    def message(self):
        result = subprocess.Popen("ls",stdout=subprocess.PIPE,shell=True)
        (self.output, self.err) = result.communicate()
        self.returncode = result.wait()

    def time1(self):
        self.finished = False
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        self.time.setText('Time' + str(self.timeout))
        if self.timeout == 5:
            self.msg.setText(timestamp + ' Start doing test')
        elif self.timeout == 0:
            self.msg.append(timestamp + self.output)
            self.msg.append(timestamp + ' End test')
        elif self.timeout == -1:
            self.finished =  True
            self.timer.stop()
            self.close()
            
        self.timeout = self.timeout - 1 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_ui = FirmwareCheck()
    main_ui.show()
    app.exec_()