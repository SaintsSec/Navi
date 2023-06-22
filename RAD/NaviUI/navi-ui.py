from PyQt5 import QtWidgets, uic
import sys

#TODO - Link up UI elements to code. 

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi('navi.ui', self)
        textWindow = QtWidgets.QTextEdit()
        textWindow.setText("Hello world!")
        self.show()

#create a qt widget, which will be our window.
app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()

#run the application
app.exec_()
