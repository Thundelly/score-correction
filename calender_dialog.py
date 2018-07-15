from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Calender_Dialog(QWidget):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)


        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)

        vbox.addWidget(cal)
        self.lbl = QLabel(self)
        date = cal.selectedDate()
        month = date.month()
        days = date.day()
        year = date.year()

        self.cur_date = str(month) + "/" + str(days) + "/" + str(year)

        self.lbl.setText(self.cur_date)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 350, 300)
        self.raise_()
        self.setWindowTitle('Calendar')

    # We retrieve the selected date by calling the selectedDate() method.
    # Then we transform the date object into string and set it to the label widget.
    def showDate(self, date):
        month = date.month()
        days = date.day()
        year = date.year()
        self.cur_date = str(month) + "/" + str(days) + "/" + str(year)
        self.lbl.setText(self.cur_date)
        self.label.setText(self.cur_date)
