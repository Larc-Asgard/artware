from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPainter
import sys

class Outline(QWidget):
    def __init__(self, parent):
        super(Outline, self).__init__(parent)
        self.brush = QBrush(QColor(100,100,100), 1)
        self.pen = QPen(QColor(180,180,180),1)
        self.pen.setWidth(7.5)

    # This method gets called every time an Outline needs to draw itself
    # to the screen.
    def paintEvent(self, event):
        outline = self.rect()
        qp = QPainter(self)
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
        self.linePen.setColor(QColor(230,230,230))
        self.linePen.setWidth(3)
        self.currentHandle = None
        self.dragStartPos = None
        self.setMinimumSize(300, 300)
        self.move(0,0)
        self.handles = [Handle('H1',150,150,50)]
        # 4 handles each represented by a QPoint

    # This method gets called every time an Outline needs to draw itself
    # to the screen.
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(self.linePen)
        qp.setBrush(self.backgroundBrush)
        qp.drawEllipse(35,35,230,230) # draw an outline around the graph
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
                self.currentHandle = handle
                self.dragStartPos = QPoint(handle.x(), handle.y())
                break

    def mouseMoveEvent(self, event):
        if self.currentHandle != None:
            w = self.width()
            h = self.height()
            mouse = event.pos()
            if  mouse.x() > 40 and mouse.x() < w-40 and mouse.y() > 40 and mouse.y() < h-40:
                self.currentHandle.setPos(mouse)
            else:
                self.currentHandle.setPos(self.dragStartPos)
                self.dragStartPos = None
                self.currentHandle = None
            self.update()

    def mouseReleaseEvent(self, event):
        if self.currentHandle != None:
            self.currentHandle = None

class MyWin(QWidget):

    switchStyle = """
        QPushButton {
            background-color: grey;
            border-radius: 20px;
            border: 6px Solid lightgrey;
            max-width: 100px;
            max-height: 200px;
        }
        QPushButton:checked {
            background-color: white;
        }

    """

    def __init__(self):
        super(MyWin, self).__init__()
        self.initGUI()

    def turnOn(self):
        self.but.setText("")

    def unclick(self):
        self.but.setText("")
        self.but.setChecked(False)

    def initGUI(self):
        self.setWindowTitle("The Pure Interface")
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
        #the buttons
        button1 = QPushButton(self)
        button1.resize(50,50)
        button1.move(550+25,300+25)
        button2 = QPushButton(self)
        button2.resize(50,50)
        button2.move(550+175,300+25)
        button3 = QPushButton(self)
        button3.resize(50,50)
        button3.move(550+125-25,300+125-25)
        button4 = QPushButton(self)
        button4.resize(50,50)
        button4.move(550+25,300+175)
        button5 = QPushButton(self)
        button5.resize(50,50)
        button5.move(550+175,300+175)
        #the dial
        dial = QDial(self)
        dial.resize(250,250)
        dial.move(300, 300)
        #the slider
        slider1 = QSlider(Qt.Horizontal, self)
        slider1.resize(100, 25)
        slider1.move(800+125, 300+45)
        slider2 = QSlider(Qt.Horizontal, self)
        slider2.resize(100, 25)
        slider2.move(800+125, 300+115)
        slider3 = QSlider(Qt.Horizontal, self)
        slider3.resize(100, 25)
        slider3.move(800+125, 300+185)
        #mimicking the useless metal ball
        ballbutton = QPushButton(self)
        ballbutton.setStyleSheet("""
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
        ballbutton.move(805,365)
        #the dragger
        graph = XYGraph(self)
        graph.move(525, 25)
        #switch
        self.but = QPushButton("", self)
        self.but.setGeometry(self.rect())
        self.but.move(120,320)
        self.but.setCheckable(True) # make this button behave like a checkbox
        self.but.clicked.connect(self.turnOn)
        self.but.setStyleSheet(self.switchStyle)
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
