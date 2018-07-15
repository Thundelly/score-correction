from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Progress_Report(QWidget):
    def __init__(self):
        super().__init__()
        #create overall vertical layout
        self.layout = QHBoxLayout(self)

        #creating extra layouts
        self.info_layout = QVBoxLayout(self)
        self.active_layout = QHBoxLayout(self)
        self.report_layout = QHBoxLayout(self)
        self.right_layout = QVBoxLayout(self)
        self.table_layout = QHBoxLayout(self)
        self.subject_layout = QVBoxLayout(self)
        self.result_layout = QVBoxLayout(self)
        self.print_layout = QHBoxLayout(self)

        #creating items in info layout
        self.initInfoTable()
        self.report_title = QLabel("Report Term", self)
        self.report_title.setStyleSheet("color : blue;")

        #creating items in active layout
        self.active_title = QLabel("Student Info", self)
        self.active_title.setStyleSheet("color : blue;")
        self.active_space = QLabel("------------------------", self)
        self.active_combo = self.initComboBox(["Active", "Inactive"])

        #creating items in report layout
        self.start_date = QLineEdit("3/16/2017", self)
        self.dash = QLabel("-", self)
        self.end_date = QLineEdit("3/16/2018", self)
        self.refresh_button = QPushButton("Refresh", self)

        #creating itmes in subject layout
        self.subject_title = QLabel("All Subject", self)
        self.subject_title.setStyleSheet("color : blue;")
        self.subject_checkbox = QCheckBox("Select All", self)
        self.initSubjectTable()

        #creating items in result layout
        self.result_title = QLabel("Result", self)
        self.result_title.setStyleSheet("color : blue;")
        self.initResultTable()

        #creating items in print layout
        self.print_button = QPushButton("Print Report", self)
        self.generate_button = QPushButton("Generate Report", self)

        #adding to info layout
        self.info_layout.addLayout(self.active_layout)
        self.info_layout.addWidget(self.info_table)
        self.info_layout.addWidget(self.report_title)
        self.info_layout.addLayout(self.report_layout)

        #adding to active layout
        self.active_layout.addWidget(self.active_title)
        self.active_layout.addWidget(self.active_space)
        self.active_layout.addWidget(self.active_combo)

        #adding to report layout
        self.report_layout.addWidget(self.start_date)
        self.report_layout.addWidget(self.dash)
        self.report_layout.addWidget(self.end_date)
        self.report_layout.addWidget(self.refresh_button)

        #adding to right layout
        self.right_layout.addLayout(self.table_layout)
        self.right_layout.addLayout(self.print_layout)

        #adding to table layout
        self.table_layout.addLayout(self.subject_layout)
        self.table_layout.addLayout(self.result_layout)

        #adding to subject layout
        self.subject_layout.addWidget(self.subject_title)
        self.subject_layout.addWidget(self.subject_checkbox)
        self.subject_layout.addWidget(self.subject_table)

        #adding to reuslt layout
        self.result_layout.addWidget(self.result_title)
        self.result_layout.addWidget(self.result_table)

        #adding to print layout
        self.print_layout.addWidget(self.print_button)
        self.print_layout.addWidget(self.generate_button)

        #adding to overall layout
        self.layout.addLayout(self.info_layout)
        self.layout.addLayout(self.right_layout)

        self.setLayout(self.layout)

    def initInfoTable(self):
        # create table
        self.info_table = QTableWidget()

        row = 21
        col = 5

        self.info_table.setRowCount(row)
        self.info_table.setColumnCount(col)

        table_labels = ["Class", "Grade", "Student ID", "Student", "Select"]

        #set the table column labels
        for i in range(0, len(table_labels)):
            self.info_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))

        #create comboxbox for each cell
        for i in range(0, row):
            for j in range(0, col):
                if j != 4:
                    self.info_table.setItem(i, j, QTableWidgetItem(""))
                else:
                    checkbox = QCheckBox("", self)
                    self.info_table.setCellWidget(i, j, checkbox)

    def initSubjectTable(self):
        # create table
        self.subject_table = QTableWidget()

        row = 1
        col = 2

        self.subject_table.setRowCount(row)
        self.subject_table.setColumnCount(col)

        table_labels = ["Subject", "Select"]

        #set the table column labels
        for i in range(0, len(table_labels)):
            self.subject_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))

        #create comboxbox for each cell
        for i in range(0, row):
            for j in range(0, col):
                if j < 1:
                    self.subject_table.setItem(i, j, QTableWidgetItem(""))
                else:
                    checkbox = QCheckBox("", self)
                    self.subject_table.setCellWidget(i, j, checkbox)

    def initResultTable(self):
        # create table
        self.result_table = QTableWidget()

        row = 12
        col = 4

        self.result_table.setRowCount(row)
        self.result_table.setColumnCount(col)

        table_labels = ["Scan\nSelect", "Test Date", "Point", "Comment"]

        #set the table column labels
        for i in range(0, len(table_labels)):
            self.result_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))

        #create comboxbox for each cell
        for i in range(0, row):
            for j in range(0, col):
                if j != 0:
                    self.result_table.setItem(i, j, QTableWidgetItem(""))
                else:
                    checkbox = QCheckBox("", self)
                    self.result_table.setCellWidget(i, j, checkbox)

    def initComboBox(self, items):
        combo = QComboBox(self)
        for item in items:
            combo.addItem(item)
        return combo
