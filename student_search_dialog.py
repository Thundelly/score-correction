from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import datetime
from generate_sheet import *
import platform
import subprocess

class Student_Search_Dialog(QWidget):
    def __init__(self, file_manager, subject_line, category_line, number_line):
        super().__init__()
        self.file_manager = file_manager
        self.count = 0
        self.student_id = None
        self.subject_line = subject_line
        self.category_line = category_line
        self.number_line = number_line
        self.initUI()
        self.generate_sheet = Generate_Sheet(self.file_manager)


    def initUI(self):
        vbox = QVBoxLayout(self)
        search_field = QHBoxLayout(self)

        name_text = QLabel("Name:", self)
        self.name_line = QLineEdit(self)

        grade_text = QLabel("Grade:", self)
        self.grade_line = QLineEdit(self)

        button = QPushButton("Search")
        button.clicked.connect(self.search)

        self.initTable()


        search_field.addWidget(name_text)
        search_field.addWidget(self.name_line)

        search_field.addWidget(grade_text)
        search_field.addWidget(self.grade_line)

        search_field.addWidget(button)

        print_button = QPushButton("Print")
        print_button.clicked.connect(self.print_sheet)

        vbox.addLayout(search_field)
        vbox.addWidget(self.tableWidget)
        vbox.addWidget(print_button)

        date = datetime.datetime.now()
        month = date.month
        days = date.day
        year = date.year

        self.cur_date = str(month) + "/" + str(days) + "/" + str(year)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 600, 400)
        self.raise_()
        self.setWindowTitle('Select Student Page')

    def initTable(self):
        # create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setFocusPolicy(Qt.StrongFocus)

        self.row = 0
        self.col = 5

        self.tableWidget.setRowCount(self.row)
        self.tableWidget.setColumnCount(self.col)

        self.table_labels = ["Name", "Grade", "Birth Date", "ID" ,"Select"]

        header = self.tableWidget.horizontalHeader()
        #set the table column labels
        for i in range(0, len(self.table_labels)):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(self.table_labels[i]))
            if i == 0:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def search(self):
        self.clear_table_rows()
        if self.name_line.text() == "" and self.grade_line.text() == "":
            for key in self.file_manager.database.keys():
                self.add_row(self.file_manager.database[key], key)
        else:
            result = set()
            if self.name_line.text() != "" and self.grade_line.text() != "":

                for key in self.file_manager.database.keys():
                    name = self.file_manager.database[key]["first_name"] + " " + self.file_manager.database[key][
                        "last_name"]
                    grade = self.file_manager.database[key]["grade"]
                    if self.name_line.text().lower() in name.lower() and self.grade_line.text().lower() in grade.lower():
                        result.add(key)

            else:
                for key in self.file_manager.database.keys():
                    if self.name_line.text() != "":
                        name = self.file_manager.database[key]["first_name"] + " " + self.file_manager.database[key]["last_name"]
                        if self.name_line.text().lower() in name.lower():
                            result.add(key)
                    if self.grade_line.text() != "":
                        grade = self.file_manager.database[key]["grade"]
                        if self.grade_line.text().lower() in grade.lower():
                            result.add(key)
            for id in result:
                self.add_row(self.file_manager.database[id], id)


    def add_row(self, student, student_id):
        i = self.tableWidget.rowCount()
        self.tableWidget.insertRow(i)
        self.tableWidget.setItem(i, 0, QTableWidgetItem(student["first_name"] + " " +  student["last_name"]))
        self.tableWidget.setItem(i, 1, QTableWidgetItem(student["grade"]))
        self.tableWidget.setItem(i, 2, QTableWidgetItem(student["birth_date"]) )
        self.tableWidget.setItem(i, 3, QTableWidgetItem(student_id) )
        checkbox = QCheckBox(self)
        checkbox.stateChanged.connect(self.select_check)
        self.tableWidget.setCellWidget(i, 4, checkbox)

    def select_check(self):
        if self.sender().isChecked(): #unchecked
            self.count += 1
        else:
            self.count -= 1

    def print_sheet(self):
        if self.count > 1:
            buttonReply = QMessageBox.warning(self, 'Warning', "Only select one student!",
                                              QMessageBox.Ok, QMessageBox.Ok)
        else:
            test_info = self.subject_line.currentText() + "-" + self.category_line.currentText() + "-" + self.number_line.currentText()
            test_ori = test_info
            test_info = "".join(test_info.split())
            for i in range(0, self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(i, 4).isChecked():
                    self.student_id = self.tableWidget.item(i, 3).text()
                    break

            student = self.file_manager.get_student(self.student_id)
            name = student["first_name"] + " " + student["last_name"]

            file_path = self.generate_sheet.generate_test(self.student_id, test_info, test_ori )

            buttonReply = QMessageBox.information(self, 'Notification',
                                                  "Answer sheet for " + name + " was created successfully!" ,
                                                  QMessageBox.Ok, QMessageBox.Ok)


            self.open_file(file_path)

    def open_file(self, path1):
        if platform.system() == "Windows":
            os.startfile(path1)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path1])
        else:
            subprocess.Popen(["xdg-open", path1])


    def clear_table_rows(self):

        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
