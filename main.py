import sys
from win import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage,QPainter,QPen

class WhiteBoard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        print(self.size())
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(QtCore.Qt.white)
        self.ui.pushButton_clear.pressed.connect(lambda: self.clearScreen())
        self.ui.pushButton_pen.pressed.connect(lambda: self.switchPenAndEraser("pen"))
        self.ui.pushButton_eraser.pressed.connect(lambda: self.switchPenAndEraser("eraser"))
        self.ui.pushButton_insize.pressed.connect(lambda: self.changeBrushSize(1))
        self.ui.pushButton_decsize.pressed.connect(lambda: self.changeBrushSize(0))
        self.ui.pushButton_color.pressed.connect(lambda: self.selectColor())
        self.ui.pushButton_save.pressed.connect(lambda: self.save())
        self.lastpencolor=QtCore.Qt.black
        self.buttonColor=None
        self.is_pen_selected=True
        self.pen_size=2
        self.eraser_size=2
        # drawing flag
        self.drawing = False
        # default brush size
        self.brushSize = None
        self.brushColor=self.lastpencolor

        self.show()

    def save(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "",
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        if filePath == "":
            return
        self.image.save(filePath)
    def selectColor(self):
        dialog = QtWidgets.QColorDialog(self)
    
        self.lastpencolor=dialog.getColor()
        self.buttonColor=self.lastpencolor.getRgb()[0:3]
        self.ui.pushButton_color.setStyleSheet(f"background-color: rgb({self.buttonColor[0]},{self.buttonColor[1]},{self.buttonColor[2]}); \n color: rgb(255,255,255); ")
        
    

    def changeBrushSize(self,option):
        if self.is_pen_selected==True:
            if option==1:
                self.pen_size+=2
            else:
                self.pen_size-=2
        else:
            if option==1:
                self.eraser_size+=2
            else:
                self.eraser_size-=2

    def switchPenAndEraser(self,option):
        if option=="pen":
            self.is_pen_selected=True
        else:
            self.is_pen_selected=False


    def clearScreen(self):
        self.image.fill(QtCore.Qt.white)
        self.update()

    def mousePressEvent(self, event):
 
        # if left mouse button is pressed
        if event.button() == QtCore.Qt.LeftButton:
            # make drawing flag true
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.pos()
 
    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
         
        # checking if left button is pressed and drawing flag is true
        if (event.buttons() & QtCore.Qt.LeftButton) & self.drawing:
             
            # creating painter object
            painter = QPainter(self.image)
            if self.is_pen_selected==True:
                self.brushSize=self.pen_size
                self.brushColor=self.lastpencolor
            else:
                self.brushSize=self.eraser_size
                self.brushColor=QtCore.Qt.white
            # set the pen of the painter
            painter.setPen(QPen(self.brushColor, self.brushSize,
                            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
             
            # draw line from the last point of cursor to the current point
            # this will draw only one step
            painter.drawLine(self.lastPoint, event.pos())
             
            # change the last point
            self.lastPoint = event.pos()
            # update
            self.update()
 
    # method for mouse left button release
    def mouseReleaseEvent(self, event):
 
        if event.button() == QtCore.Qt.LeftButton:
            # make drawing flag false
            self.drawing = False
 
    # paint event
    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)

        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
 

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    whiteboard=WhiteBoard()
    sys.exit(app.exec_())
