import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from test_management import *
from auto_correction import *
from correction_results import *
from progress_report import *
from test_setup import *
from file_manager import *
from add_student import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # initialize QDesktopWidget and set the size of the window
        self.dw = QDesktopWidget()
        width = self.dw.availableGeometry().width() * 0.75
        height = self.dw.availableGeometry().height() * 0.75
        self.resize(width, height)
        self.center()
        self.setWindowTitle('Score Correction')

        #initialize status bar
        self.initStatusBar()

        #initialize tab bar
        self.initTab()

        # show the window
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initStatusBar(self):
        self.sb = self.statusBar()
        self.sb.showMessage('Ready')

    def changeStatus(self, message):
        self.sb.showMessage(message)

    def initTab(self):
        self.tw = TableWidget(self)
        self.setCentralWidget(self.tw)

class TableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.file_manager = File_Manager()

        #initialize objects
        self.tabs = QTabWidget()
        self.tab1 = Test_Management(self.file_manager)
        self.tab2 = Auto_Correction(self.file_manager)
        self.tab3 = Correction_Results(self.file_manager)
        #self.tab4 = Progress_Report()
        self.tab5 = Test_Setup(self.file_manager)
        self.tab6 = Add_Student(self.file_manager)
        self.tabs.resize(300, 200)

        # add tabs
        self.tabs.addTab(self.tab1, 'Test Management')
        self.tabs.addTab(self.tab2, 'Auto. Correction')
        self.tabs.addTab(self.tab3, 'Correction Results')
        #self.tabs.addTab(self.tab4, 'Progress Report')
        self.tabs.addTab(self.tab5, 'Test Setup')
        self.tabs.addTab(self.tab6, 'Add Student')

        # Add tabs to our table widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())