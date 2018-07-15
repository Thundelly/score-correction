from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Add_Student(QWidget):
    def __init__(self, file_manager):
        super(Add_Student, self).__init__()

        #create form and vertical and horizontal layout
        self.file_manager = file_manager
        self.form_layout = QFormLayout()
        self.vertical_layout = QVBoxLayout()
        self.horizontal_layout = QHBoxLayout()
        self.spacer = QSpacerItem(30, 30)
        self.initTable()

        #create extra layouts
        self.title = QLabel('Please input the student information')
        self.title.setStyleSheet("color: blue")

        self.first_name_label = QLabel('First Name:')
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setFixedWidth(250)

        self.last_name_label = QLabel('Last Name:')
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setFixedWidth(250)

        self.birth_date_label = QLabel('Birth Date:')
        self.birth_date_edit = QLineEdit()
        self.birth_date_edit.setFixedWidth(250)

        self.grade_label = QLabel('Grade:')
        self.grade_edit = QLineEdit()
        self.grade_edit.setFixedWidth(250)

        self.save_btn = QPushButton('Save')
        self.save_btn.setFixedWidth(100)
        self.save_btn.clicked.connect(self.add_student)

        self.table_load_btn = QPushButton('Load Student Information')
        self.table_load_btn.setFixedWidth(200)
        self.table_load_btn.clicked.connect(self.load_table)

        self.table_update_btn = QPushButton('Update Table')
        self.table_update_btn.setFixedWidth(200)
        self.table_update_btn.clicked.connect(self.update_student_info)

        self.delete_row_btn = QPushButton('Delete Row')
        self.delete_row_btn.setFixedWidth(200)
        self.delete_row_btn.clicked.connect(self.inactive_student)

        #add to vertical layout
        self.vertical_layout.addWidget(self.title)
        self.vertical_layout.addItem(self.spacer)
        self.vertical_layout.addWidget(self.first_name_label)
        self.vertical_layout.addWidget(self.first_name_edit)
        self.vertical_layout.addWidget(self.last_name_label)
        self.vertical_layout.addWidget(self.last_name_edit)
        self.vertical_layout.addWidget(self.birth_date_label)
        self.vertical_layout.addWidget(self.birth_date_edit)
        self.vertical_layout.addWidget(self.grade_label)
        self.vertical_layout.addWidget(self.grade_edit)
        self.vertical_layout.addItem(self.spacer)
        self.vertical_layout.addWidget(self.save_btn)

        #create button horizontal layout
        self.btn_horizontal_layout = QHBoxLayout()
        self.btn_horizontal_layout.addWidget(self.table_load_btn)
        self.btn_horizontal_layout.addWidget(self.table_update_btn)
        self.btn_horizontal_layout.addWidget(self.delete_row_btn)

        #create second vertical layout
        self.vertical_layout1 = QVBoxLayout()
        self.vertical_layout1.addWidget(self.tableWidget)
        self.vertical_layout1.addLayout(self.btn_horizontal_layout)
        # self.vertical_layout1.addWidget(self.table_load_btn)

        #add to horizontal layout
        self.horizontal_layout.addLayout(self.vertical_layout)
        self.horizontal_layout.addItem(self.spacer)
        self.horizontal_layout.addLayout(self.vertical_layout1)

        self.form_layout.addRow(self.horizontal_layout)
        self.setLayout(self.form_layout)

    def initTable(self):

        #create tablewidget to display student information
        self.tableWidget = QTableWidget()
        self.tableWidget.setFixedWidth(1000)
        self.tableWidget.setFixedHeight(300)
        self.tableWidget.setFocusPolicy(Qt.StrongFocus)
        # self.tableWidget.itemClicked.connect(self.dumb)

        #set row and column count
        self.row = 0
        self.col = 5

        #create table header label
        self.table_label = ["First Name", "Last Name",
                            "Birth Date", "Grade",
                            "Student ID"]


        #assign initial row and column count
        self.tableWidget.setRowCount(self.row)
        self.tableWidget.setColumnCount(self.col)
        self.tableWidget.setHorizontalHeaderLabels(self.table_label)

    #override enter press event
    def keyPressEvent(self, QKeyEvent):
        key = QKeyEvent.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.dumb()
        else:
            super(Add_Student, self).keyPressEvent(QKeyEvent)

    def dumb(self):
        print("HI")

    def load_table(self):

        self.data = []
        cur_number_of_student = self.file_manager.get_number_of_student()

        for i in range(0, len(cur_number_of_student)):
            cur_number_of_student[i] = int(cur_number_of_student[i])
            self.row = cur_number_of_student[i] - 100
            self.tableWidget.setRowCount(self.row)

        for i in range(100, self.row + 100):
            self.first_name_database = self.file_manager.get_user_info(str(i))
            self.data.append([n for n in self.first_name_database])
        self.data.sort()

        for k in range(0, self.row):
            for j in range(0, self.col):
                if j == 0:
                    self.tableWidget.setItem(k, j, QTableWidgetItem(self.data[k][0]))
                elif j == 1:
                    self.tableWidget.setItem(k, j ,QTableWidgetItem(self.data[k][1]))
                elif j == 2:
                    self.tableWidget.setItem(k, j, QTableWidgetItem(self.data[k][2]))
                elif j == 3:
                    self.tableWidget.setItem(k, j ,QTableWidgetItem(self.data[k][3]))
                elif j == 4:
                    self.tableWidget.setItem(k, j ,QTableWidgetItem(self.data[k][4]))

    def add_student(self):
        self.first = self.first_name_edit.text()
        self.last = self.last_name_edit.text()
        self.birth_date = self.birth_date_edit.text()
        self.grade = self.grade_edit.text()

        self.file_manager.get_next_studentID()
        self.file_manager.add_student_to_database(self.first, self.last, self.birth_date, self.grade)
        self.file_manager.add_student_to_test_record()
        self.file_manager.save_file("student_data")
        self.file_manager.save_file("student_data_id")
        self.file_manager.save_file("cr")

        self.clear_field()

    def clear_field(self):
        self.first_name_edit.clear()
        self.last_name_edit.clear()
        self.birth_date_edit.clear()
        self.grade_edit.clear()

    def update_student_info(self):
        for i in range(0, self.row):
            for j in range(0, 1):
                turn = 1
                id = self.tableWidget.item(i, 4).text()
                first = self.tableWidget.item(i, j).text()
                self.file_manager.update_student_info(first, None, None,
                                                      None, id, turn)
            for j in range(1, 2):
                turn = 2
                id = self.tableWidget.item(i, 4).text()
                last = self.tableWidget.item(i, j).text()
                self.file_manager.update_student_info(None, last, None,
                                                      None, id, turn)
            for j in range(2, 3):
                turn = 3
                id = self.tableWidget.item(i, 4).text()
                birth_date = self.tableWidget.item(i, j).text()
                self.file_manager.update_student_info(None, None, birth_date,
                                                      None, id, turn)
            for j in range(3, 4):
                turn = 4
                id = self.tableWidget.item(i, 4).text()
                grade = self.tableWidget.item(i, j).text()
                self.file_manager.update_student_info(None, None, None,
                                                      grade, id, turn)

    def inactive_student(self):
        print('This button works well')
    # If you put the inactive student to the other json file, increment the number
    # of students moved, and subtract that from the "nextID" to correctly
    # return the number of rows.