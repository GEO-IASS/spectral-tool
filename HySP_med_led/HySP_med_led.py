import pyfirmata
import time
import epix_framegrabber
from matplotlib import pylab,pyplot
import numpy
#from HySP_med_led import epix_framegrabber

try:
    epix_framegrabber.Camera()
    epix_available = True
except epix_framegrabber.CameraOpenError:
    epix_available = False




#open the camera
camera = epix_framegrabber.Camera()

aa = camera.open(8, [2048, 1088],camera = "PhotonFocus",exposure = 10,frametime = 100.0)

#camera.set_tap_configuration(2)

# put the correct settings for camera, correct CLTap, bitdepth

#create an array like this GOOD_PIX = numpy.zeros((x_size_image,y_size_image,LED))
fig1 = pylab.figure()

#for each LED

#1. take a picture

#2. if image int < somenumber 
#if too bright -> while too bright decrease exposure
#if too dim -> while 

#3. once you find the right image , save it in GOOD_PIX

#4. move to next LED



camera.set_exposure(1000000)
#print(camera.cam.properties['ExposureTimeAbs'])


bb = camera.start_sequence_capture(1)
cc = camera.get_image() # this is your picture
max = numpy.max(cc)
bb = numpy.array(aa)


#plt.imshow(cc)

f = pyplot.figure()
ax = f.gca()
f.show()


ax.imshow(cc)
f.canvas.draw()
for i in range(0,3):
    
    camera.set_exposure(10000*(10*i))    
    #aa = camera.start_sequence_capture(1)

    bb= camera.start_sequence_capture(1)
    cc = camera.get_image() # this is your picture
    max = numpy.max(cc)
    ax.imshow(cc)
    f.canvas.draw()
###    #bb = numpy.array(aa)




    #camera.close()
    #perfect image
    #->
    #GOOD_PIX[:,:,LEDnum] = perfect image
    ##fig1.imshow(cc)
    ##pylab.show()


camera.close()



#try:
#    board = pyfirmata.ArduinoDue('\\.\COM6')
#except Exception:
#    print('error')

#for i in range(22,25):  
    
##    #remember to put PIN down!! only one LED open at the time
#    board.digital[i].write(1)
#    time.sleep(1)
#    board.digital[i].write(0)



    





#"""
#This recipe opens a simple window in PyQt to poll the serial port for 
#data and print it out. Uses threads and a queue.

#DON'T FORGET TO SET SERIALPORT BEFORE RUNNING THIS CODE

#Here is an Arduino Sketch to use:
#    ***********
#void setup() {
#  Serial.begin(115200);
#}
#void loop() {
#  Serial.println("I blinked");
#  delay(1000);
#}
#    ***********
#This recipe depends on PyQt and pySerial. Qt 4 is world class code 
#and I like how it looks. PyQt is not completely open source, 
#but I think PySide is. Tested on Qt4.6 / Win 7 / Duemilanove

#Author: Dirk Swart, Ithaca, NY. 2011-05-20. www.wickeddevice.com

#Based on threads recipe by Jacob Hallen, AB Strakt, Sweden. 2001-10-17
#As adapted by Boudewijn Rempt, Netherlands. 2002-04-15

#PS: This code is provided with no warranty, express or implied. It is 
#meant to demonstrate a concept only, not for actual use. 
#Code is in the public domain.
#"""
#__author__ = 'Dirk Swart, Doudewijn Rempt, Jacob Hallen'

#import sys, time, threading, random, Queue
#from PyQt5 import QtGui, QtCore as qt
#import serial

#SERIALPORT = 'COM6'

#class GuiPart(QtGui.QMainWindow):

#    def __init__(self, queue, endcommand, *args):
#        QtGui.QMainWindow.__init__(self, *args)
#        self.setWindowTitle('Arduino Serial Demo')
#        self.queue = queue
#        # We show the result of the thread in the gui, instead of the console
#        self.editor = QtGui.QTextEdit(self)
#        self.setCentralWidget(self.editor)
#        self.endcommand = endcommand    
        
#    def closeEvent(self, ev):
#        self.endcommand()

#    def processIncoming(self):
#        """
#        Handle all the messages currently in the queue (if any).
#        """
#        while self.queue.qsize():
#            try:
#                msg = self.queue.get(0)
#                # Check contents of message and do what it says
#                # As a test, we simply print it
#                self.editor.insertPlainText(str(msg))
#            except Queue.Empty:
#                pass

#class ThreadedClient:
#    """
#    Launch the main part of the GUI and the worker thread. periodicCall and
#    endApplication could reside in the GUI part, but putting them here
#    means that you have all the thread controls in a single place.
#    """
#    def __init__(self):
#        # Create the queue
#        self.queue = Queue.Queue()

#        # Set up the GUI part
#        self.gui=GuiPart(self.queue, self.endApplication)
#        self.gui.show()

#        # A timer to periodically call periodicCall :-)
#        self.timer = qt.QTimer()
#        qt.QObject.connect(self.timer,
#                           qt.SIGNAL("timeout()"),
#                           self.periodicCall)
#        # Start the timer -- this replaces the initial call to periodicCall
#        self.timer.start(100)

#        # Set up the thread to do asynchronous I/O
#        # More can be made if necessary
#        self.running = 1
#        self.thread1 = threading.Thread(target=self.workerThread1)
#        self.thread1.start()

#    def periodicCall(self):
#        """
#        Check every 100 ms if there is something new in the queue.
#        """
#        self.gui.processIncoming()
#        if not self.running:
#            root.quit()

#    def endApplication(self):
#        self.running = 0

#    def workerThread1(self):
#        """
#        This is where we handle the asynchronous I/O. 
#        Put your stuff here.
#        """
#        while self.running:
#            #This is where we poll the Serial port. 
#            #time.sleep(rand.random() * 0.3)
#            #msg = rand.random()
#            #self.queue.put(msg)
#            ser = serial.Serial(SERIALPORT, 115200)
#            msg = ser.readline();
#            if (msg):
#                self.queue.put(msg)
#            else: pass  
#            ser.close()

##rand = random.Random()
#root = QtGui.QApplication(sys.argv)
#client = ThreadedClient()
#sys.exit(root.exec_())

##import sys
##import glob
##import serial


##def serial_ports():
##    """ Lists serial port names

##        :raises EnvironmentError:
##            On unsupported or unknown platforms
##        :returns:
##            A list of the serial ports available on the system
##    """
##    if sys.platform.startswith('win'):
##        ports = ['COM%s' % (i + 1) for i in range(256)]
##    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
##        # this excludes your current terminal "/dev/tty"
##        ports = glob.glob('/dev/tty[A-Za-z]*')
##    elif sys.platform.startswith('darwin'):
##        ports = glob.glob('/dev/tty.*')
##    else:
##        raise EnvironmentError('Unsupported platform')

##    result = []
##    for port in ports:
##        try:
##            s = serial.Serial(port)
##            s.close()
##            result.append(port)
##        except (OSError, serial.SerialException):
##            pass
##    return result


##if __name__ == '__main__':
##    print(serial_ports())

##def main():

##    app = QtGui.QApplication(sys.argv)
##    ex = captureFrames()
##    app.aboutToQuit.connect(ex.closing_sequence)
##    sys.exit(app.exec_())


##if __name__ == '__main__':
##    main()