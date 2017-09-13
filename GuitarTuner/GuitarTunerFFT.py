# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


import numpy as np
import pylab
import time
import random
from math import log2, pow

import pyaudio

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
soundObj = pyaudio.PyAudio()

# Learn what your OS+Hardware can do
defaultCapability = soundObj.get_default_host_api_info()
print (defaultCapability)

# See if you can make it do what you want
isSupported = soundObj.is_format_supported(input_format=pyaudio.paInt8, input_channels=1, rate=22050, input_device=0)
print (isSupported)


CHUNK = 1024*16*3
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


print("* running")

frames = []

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
i = 0


A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def pitch(freq):
    
    freqLog = 12*log2(freq/C0)
    h = round(freqLog)
    octave = h // 12
    n = h % 12
    nFreq = freqLog %12
    deltaPercent = 100*(nFreq - n)
    return name[n] + str(octave), deltaPercent


# Valid: above 166 Hz
# Below 166: result is 3X actual frequency
def soundplot(data):
    global key, percent
    t1=time.time()
    #pylab.clf()
    fft = np.fft.fft(data)
    fftr=10.0*np.log10((abs(fft.real)))[:round(len(fft)/2)]
    fftb=10.0*np.log10((np.sqrt(fft.imag**2+fft.real**2)))[:round(len(data)/2)]
    freq=(np.fft.fftfreq(np.arange(len(data)).shape[-1])[:round(len(data)/2)])
    freqOld = list(freq)
    freq = freq*RATE
    fft = fft[:round(len(fft)/2)]
    #pylab.plot(freq, fftr)
    #pylab.title(i)
    #pylab.grid()
    #pylab.pause(0.0001)
    #pylab.axis([0,len(data),-2**16/2,2**16/2])
    #pylab.show()
    #print("took %.02f ms"%((time.time()-t1)*1000))
    fftrList= list(fftb)
    freqList = list(freq)
    maxIndex = fftrList.index(max(fftrList))
    frequency = freqList[maxIndex]
    key, percent = pitch(freqList[maxIndex])
    
    print("\n")
    print("Frequency (Hz): " + str(frequency))
    print("Original Frequency: " + str(freqOld[maxIndex]))
    print("key : " + str(key))
    print("percent: " + str(percent))
    
    return key, percent
    


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

# Plotting Class
class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        print("setupUi")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(552, 386)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.guitarTuner_label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.guitarTuner_label.setFont(font)
        self.guitarTuner_label.setAlignment(QtCore.Qt.AlignCenter)
        self.guitarTuner_label.setObjectName("guitarTuner_label")
        self.horizontalLayout_6.addWidget(self.guitarTuner_label)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.line_13 = QtWidgets.QFrame(self.centralWidget)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.verticalLayout.addWidget(self.line_13)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.rawAudio_label = QtWidgets.QLabel(self.centralWidget)
        self.rawAudio_label.setObjectName("rawAudio_label")
        self.verticalLayout_4.addWidget(self.rawAudio_label)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fft_label = QtWidgets.QLabel(self.centralWidget)
        self.fft_label.setObjectName("fft_label")
        self.verticalLayout_5.addWidget(self.fft_label)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.line_12 = QtWidgets.QFrame(self.centralWidget)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.verticalLayout.addWidget(self.line_12)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.key_label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.key_label.setFont(font)
        self.key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_label.setObjectName("key_label")
        self.horizontalLayout.addWidget(self.key_label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.low_label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.low_label.sizePolicy().hasHeightForWidth())
        self.low_label.setSizePolicy(sizePolicy)
        self.low_label.setObjectName("low_label")
        self.horizontalLayout_5.addWidget(self.low_label)
        self.line_2 = QtWidgets.QFrame(self.centralWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_5.addWidget(self.line_2)
        self.line_5 = QtWidgets.QFrame(self.centralWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_5.addWidget(self.line_5)
        self.line_4 = QtWidgets.QFrame(self.centralWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_5.addWidget(self.line_4)
        self.line_3 = QtWidgets.QFrame(self.centralWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_5.addWidget(self.line_3)
        self.line_6 = QtWidgets.QFrame(self.centralWidget)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_5.addWidget(self.line_6)
        self.line_7 = QtWidgets.QFrame(self.centralWidget)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_7.setLineWidth(1)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_5.addWidget(self.line_7)
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.line_8 = QtWidgets.QFrame(self.centralWidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.horizontalLayout_5.addWidget(self.line_8)
        self.line_10 = QtWidgets.QFrame(self.centralWidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.horizontalLayout_5.addWidget(self.line_10)
        self.line_11 = QtWidgets.QFrame(self.centralWidget)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.horizontalLayout_5.addWidget(self.line_11)
        self.line_9 = QtWidgets.QFrame(self.centralWidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout_5.addWidget(self.line_9)
        self.high_label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.high_label.sizePolicy().hasHeightForWidth())
        self.high_label.setSizePolicy(sizePolicy)
        self.high_label.setObjectName("high_label")
        self.horizontalLayout_5.addWidget(self.high_label)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalSlider = QtWidgets.QSlider(self.centralWidget)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setPageStep(10)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider.setTickInterval(7.5)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_4.addWidget(self.horizontalSlider)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.guitarTuner_label.setText(_translate("MainWindow", "Python Guitar Tuner"))
        self.rawAudio_label.setText(_translate("MainWindow", "Put audio display here"))
        self.fft_label.setText(_translate("MainWindow", "Put FFT of aduio here"))
        self.key_label.setText(_translate("MainWindow", "G"))
        self.low_label.setText(_translate("MainWindow", "  Low "))
        self.high_label.setText(_translate("MainWindow", "High"))
        print("retranslateUi")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    percent = 0.0
    key = ""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
    
    def updateTuner():
        global frames, key, percent
        t1=time.time()
        try:
            data = stream.read(CHUNK, exception_on_overflow = False)
            #frames.append(data)
            data2 = np.fromstring(data, dtype=np.int16)
            key, percent = soundplot(data2)
            print("key Here: " + str(key))
            ui.key_label.setText(key)
            ui.horizontalSlider.setProperty("value", 50 + percent)
            print("Updated")
        except:
            pass     
        print("took %.02f ms"%((time.time()-t1)*1000))
    
    
    timer = QtCore.QTimer()
    timer.timeout.connect(updateTuner)
    timer.start(100)
    sys.exit(app.exec_())