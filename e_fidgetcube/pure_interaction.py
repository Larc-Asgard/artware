from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QPoint, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPainter
import sys


class Outline(QWidget):
    def __init__(self, parent):
        super(Outline, self).__init__(parent)
        self.brush = QBrush(QColor(100,100,100), 1)
        self.pen = QPen(QColor(180,180,180),1)
        self.pen.setWidth(7.5)
        self.font = QFont("Arial", 18, QFont.Medium)
        self.text = ""

    # This method gets called every time an Outline needs to draw itself
    # to the screen.
    def paintEvent(self, event):
        outline = self.rect()
        qp = QPainter(self)
        qp.setFont(self.font)
        qp.setPen(self.pen)
        qp.setBrush(self.brush)
        qp.drawRect(outline) # draw a rectangle on the bounding box of this widget

class Handle(QObject):
    handleMoved = pyqtSignal(QPoint)

    def __init__(self, label, xpos, ypos, radius):
        super(Handle, self).__init__()
        self.pos = QPoint(xpos, ypos)
        self.label = label
        self.radius = radius
    def __str__(self):
        stringval = "%s (%d, %d)" % (self.label, self.pos.x(), self.pos.y())
        return stringval
    def setPos(self, newpos):
        self.pos.setX(newpos.x())
        self.pos.setY(newpos.y())
        self.handleMoved.emit(self.pos)
    def x(self):
        return self.pos.x()
    def y(self):
        return self.pos.y()
    def bounds(self):
        return QRect(self.x()-self.radius, self.y()-self.radius, self.radius * 2, self.radius * 2)

class XYGraph(QWidget):
    def __init__(self, parent=None):
        super(XYGraph, self).__init__(parent)
        self.handleBrush = QBrush(QColor(140,140,140))
        self.backgroundBrush = QBrush(QColor(180, 180, 180))
        self.linePen = QPen(Qt.SolidLine)
        self.linePen.setColor(QColor(220,220,220))
        self.linePen.setWidth(3)
        self.currentHandle = None
        self.dragStartPos = None
        self.setMinimumSize(300, 300)
        self.move(0,0)
        self.handles = [Handle('H1',165,165,50)]

        for handle in self.handles:
            self.positionlabel = QLabel(self)
            self.positionlabel.setStyleSheet("""
                QLabel{
                color:white;
                }
            """)
            self.positiontext = "%d, %d" % (handle.pos.x(), handle.pos.y())
            self.positionlabel.setText(self.positiontext)
            self.positionlabel.move(handle.pos.x()-20, handle.pos.y()-5)
            handle.handleMoved.connect(self.updateLabel)

        #handle represented by a QPoint
    def updateLabel(self, handle):
        self.positiontext = "%d, %d" % (handle.x(), handle.y())
        self.positionlabel.setText(self.positiontext)
        self.positionlabel.move(handle.x()-20, handle.y()-5)

    # This method gets called every time an Outline needs to draw itself
    # to the screen.
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(self.linePen)
        qp.setBrush(self.backgroundBrush)
        qp.drawEllipse(50,50,230,230) # draw an outline around the graph
        # qp.drawEllipse(self.rect())

        qp.setBrush(self.handleBrush)
        lasthandle = None
        for handle in self.handles:
            qp.drawEllipse(handle.bounds())
            if lasthandle != None:
                qp.drawLine(lasthandle.x(), lasthandle.y(), handle.x(), handle.y())
            lasthandle = handle

    def mousePressEvent(self, event):
        mouseX = event.pos().x()
        mouseY = event.pos().y()
        # Check if the mouse is inside the bounds of a handle
        self.currentHandle = None
        for handle in self.handles:
            h = handle.bounds()
            if mouseX > h.left() and mouseX < h.right() and mouseY > h.top() and mouseY < h.bottom():
                # mouse is inside this handle's bounding box
                print ("Glide Location: " + self.positiontext)
                self.currentHandle = handle
                self.dragStartPos = QPoint(handle.x(), handle.y())
                break

    def mouseMoveEvent(self, event):
        if self.currentHandle != None:
            w = self.width()
            h = self.height()
            mouse = event.pos()
            if  mouse.x() > 50 and mouse.x() < w-90 and mouse.y() > 50 and mouse.y() < h-60:
                self.currentHandle.setPos(mouse)
            else:
                self.currentHandle.setPos(self.dragStartPos)
                self.dragStartPos = None
                self.currentHandle = None
            self.update()

    def mouseReleaseEvent(self, event):
        if self.currentHandle != None:
            self.currentHandle = None
            print ("Glide Location: " + self.positiontext)


class MyWin(QWidget):

    switchStyle = """
        QPushButton {
            background-color: grey;
            border-radius: 20px;
            border: 6px Solid lightgrey;
            max-width: 100px;
            max-height: 200px;
            font-size: 36px;
            color: white;
        }
        QPushButton:checked {
            background-color: white;
            color: grey;
        }

    """

    def __init__(self):
        super(MyWin, self).__init__()
        self.button1counter = 0
        self.switchon = False
        self.text1 = "%d" % (self.button1counter)
        self.button2counter = 0
        self.text2 = "%d" % (self.button2counter)
        self.button3counter = 0
        self.text3 = "%d" % (self.button3counter)
        self.button4counter = 0
        self.text4 = "%d" % (self.button4counter)
        self.button5counter = 0
        self.text5 = "%d" % (self.button5counter)

        self.initGUI()

    def turnOn(self):
        if self.switchon == False:
            self.switch.setText("ON")
            self.switchon = True
            print("The switch is on.")
        else:
            self.switch.setText("OFF")
            self.switchon = False
            print("The switch is off.")


    # def unclick(self):
    #     self.switch.setText("OFF")
    #     self.but.setChecked(False)

    def Button1Clicked(self):
        self.button1counter += 1
        self.text1 = "%d" % (self.button1counter)
        self.button1.setText(self.text1)
        print ("Button 1: " + self.text1)

    def Button2Clicked(self):
        self.button2counter += 1
        self.text2 = "%d" % (self.button2counter)
        self.button2.setText(self.text2)
        print ("Button 2: " + self.text2)

    def Button3Clicked(self):
        self.button3counter += 1
        self.text3 = "%d" % (self.button3counter)
        self.button3.setText(self.text3)
        print ("Button 3: " + self.text3)

    def Button4Clicked(self):
        self.button4counter += 1
        self.text4 = "%d" % (self.button4counter)
        self.button4.setText(self.text4)
        print ("Button 4: " + self.text4)

    def Button5Clicked(self):
        self.button5counter += 1
        self.text5 = "%d" % (self.button5counter)
        self.button5.setText(self.text5)
        print ("Button 5: " + self.text5)

    def printprogress1(self):
        self.number = self.slider1.value()
        self.text = "%d" %(self.number)
        print ("Slider 1: " + self.text + "%")

    def printprogress2(self):
        self.number = self.slider2.value()
        self.text = "%d" %(self.number)
        print ("Slider 2: " + self.text + "%")

    def printprogress3(self):
        self.number = self.slider3.value()
        self.text = "%d" %(self.number)
        print ("Slider 3: " + self.text + "%")

    def printdial(self):
        self.number = self.dial.value()
        self.text =  "%d" %(self.number)
        print ("Dial: " + self.text + "%")
        
    def initGUI(self):
        self.setWindowTitle("The Pure Interaction")
        height = 900
        width = 1150
        self.setGeometry(100,100, width, height)
        #drawing the fidget cube
        face1 = Outline(self)
        face1.setGeometry(550, 50, 250, 250)
        face2 = Outline(self)
        face2.setGeometry(50, 300, 250, 250)
        face3 = Outline(self)
        face3.setGeometry(300, 300, 250, 250)
        face4 = Outline(self)
        face4.setGeometry(550, 300, 250, 250)
        face5 = Outline(self)
        face5.setGeometry(800, 300, 250, 250)
        face6 = Outline(self)
        face6.setGeometry(550, 550, 250, 250)
        #the dragger
        graph = XYGraph(self)
        graph.move(510, 10)
        #the buttons
        self.button1 = QPushButton("0", self)
        self.button1.resize(50,50)
        self.button1.move(550+25,300+25)
        self.button1.clicked.connect(self.Button1Clicked)
        self.button2 = QPushButton("0", self)
        self.button2.resize(50,50)
        self.button2.move(550+175,300+25)
        self.button2.clicked.connect(self.Button2Clicked)
        self.button3 = QPushButton("0", self)
        self.button3.resize(50,50)
        self.button3.move(550+125-25,300+125-25)
        self.button3.clicked.connect(self.Button3Clicked)
        self.button4 = QPushButton("0",self)
        self.button4.resize(50,50)
        self.button4.move(550+25,300+175)
        self.button4.clicked.connect(self.Button4Clicked)
        self.button5 = QPushButton("0",self)
        self.button5.resize(50,50)
        self.button5.move(550+175,300+175)
        self.button5.clicked.connect(self.Button5Clicked)
        #the dial and meter
        self.dial = QDial(self)
        self.dial.resize(250,250)
        self.dial.move(300, 300)
        self.diallabel = QLabel(self)
        self.diallabel.setFont(QFont("Monaco", 18, QFont.Bold))
        self.diallabel.setStyleSheet("""
            QLabel{
            color: white;
            }
        """
        )
        self.diallabel.setNum(0)
        self.diallabel.move(525,515)
        self.dial.valueChanged.connect(self.diallabel.setNum)
        self.dial.valueChanged.connect(self.printdial)
        #the slider and progress bar
        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.resize(100, 25)
        self.slider1.move(800+125, 300+45)
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.progress1 = QProgressBar(self)
        self.progress1.resize(100, 5)
        self.progress1.move(925,345-5)
        self.progress1.setTextVisible(0)
        self.slider2.resize(100, 25)
        self.slider2.move(800+125, 300+115)
        self.progress2 = QProgressBar(self)
        self.progress2.setTextVisible(0)
        self.progress2.resize(100, 5)
        self.progress2.move(925,415-5)
        self.slider3 = QSlider(Qt.Horizontal, self)
        self.slider3.resize(100, 25)
        self.slider3.move(800+125, 300+185)
        self.progress3 = QProgressBar(self)
        self.progress3.resize(100, 5)
        self.progress3.move(925,485-5)
        self.progress3.setTextVisible(0)
        #connect the progress bar with slider
        self.slider1.valueChanged.connect(self.progress1.setValue)
        self.slider1.valueChanged.connect(self.printprogress1)
        self.slider2.valueChanged.connect(self.progress2.setValue)
        self.slider2.valueChanged.connect(self.printprogress2)
        self.slider3.valueChanged.connect(self.progress3.setValue)
        self.slider3.valueChanged.connect(self.printprogress3)
        #mimicking the useless metal ball
        self.ballbutton = QPushButton(self)
        self.ballbutton.setStyleSheet("""
            QPushButton {
                background-color: grey;
                border-width: 3px;
                border-style: solid;
                border-radius: 50px;
                border-color: lightgrey;
                margin: 10px;
                padding: 20px;
                min-width: 55px;
                min-height: 55px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)
        self.ballbutton.move(805,365)
        #switch
        self.switch = QPushButton("OFF", self)
        self.switch.setGeometry(self.rect())
        self.switch.move(120,320)
        self.switch.setCheckable(True) # make this button behave like a checkbox
        self.switch.clicked.connect(self.turnOn)
        self.switch.setStyleSheet(self.switchStyle)
        #textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.setPlainText("Type in your worry here.")
        self.textbox.move(575, 575)
        self.textbox.resize(200,200)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = MyWin()
    sys.exit(app.exec_())
