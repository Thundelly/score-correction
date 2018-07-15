from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from student_search_dialog import *

class Test_Management(QWidget):
    def __init__(self, file_manager):
        super().__init__()

        #instantiate file manager class
        self.file_manager = file_manager
        self.add_status = False
        self.load_status = False


        #create overall vertical layout
        self.layout = QVBoxLayout(self)

        #test sheet type section box
        self.type_layout = QVBoxLayout(self)
        self.select_layout = QHBoxLayout(self)
        self.subject_layout = QHBoxLayout(self)
        self.category_layout = QHBoxLayout(self)
        self.number_layout = QHBoxLayout(self)
        self.section_layout = QHBoxLayout(self)
        self.detail_layout = QHBoxLayout(self)
        self.custom_layout = QHBoxLayout(self)
        self.button_layout = QHBoxLayout(self)

        #creating items in type layout
        self.type_title = QLabel("Test Sheet Type", self)
        self.type_title.setStyleSheet("color : blue;")

        #creating items in select layout
        self.type1 = QLabel("Subject:", self)
        self.combo1 = self.initComboBox( self.file_manager.get_tm_subject_labels(), 0 )
        self.combo1.setCurrentText("None")

        self.combo1.setEditable(True)
        self.combo1.currentIndexChanged.connect(self.refresh_combobox)
        self.combo1.editTextChanged.connect(self.subject_combo_changed)
        self.combo1.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.combo1_add = QPushButton("+")
        self.combo1_add.clicked.connect(self.label_added)
        self.combo1_delete = QPushButton("-")
        self.combo1_delete.clicked.connect(self.label_deleted)

        self.type2 = QLabel("Category: ", self)
        self.combo2 = self.initComboBox([])
        self.combo2.setEditable(True)
        self.combo2.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.combo2_add = QPushButton("+")
        self.combo2_add.clicked.connect(self.label_added)
        self.combo2_delete = QPushButton("-")
        self.combo2_delete.clicked.connect(self.label_deleted)

        self.type3 = QLabel("Number: ", self)
        self.combo3 = self.initComboBox( [])
        self.combo3.setEditable(True)
        self.combo3.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.combo3_add = QPushButton("+")
        self.combo3_add.clicked.connect(self.label_added)
        self.combo3_delete = QPushButton("-")
        self.combo3_delete.clicked.connect(self.label_deleted)

        self.sd = Student_Search_Dialog(self.file_manager, self.combo1, self.combo2, self.combo3)

        self.type4 = QLabel("Section: ", self)
        self.combo4 = self.initComboBox( [])
        self.combo4_add = QPushButton("+")
        self.combo4_add.clicked.connect(self.label_added)
        self.combo4_delete = QPushButton("-")
        self.combo4_delete.clicked.connect(self.label_deleted)
        self.combo4.setEditable(True)
        self.combo4.view().setMinimumWidth(200)
        self.loadButton = QPushButton('Load')
        self.loadButton.clicked.connect(self.load_table)
        self.clearButton = QPushButton('Clear')
        self.clearButton.clicked.connect(self.clear_table_rows)

        #creating items in detail layout
        self.detail_title = QLabel("Detail Information", self)
        self.detail_title.setStyleSheet("color : blue;")
        self.detail_info = QLabel("SAT Subject:", self)
        self.detail_combo = self.initComboBox( self.file_manager.get_tm_sat_subject_labels() )
        self.detail_combo.setCurrentText("None")
        self.detail_combo.setEditable(True)
        self.detail_combo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.detail_combo_add = QPushButton("+")
        self.detail_combo_add.clicked.connect(self.label_added)
        self.detail_combo_delete = QPushButton("-")
        self.detail_combo_delete.clicked.connect(self.label_deleted)
        self.initTable()

        #creating items in button layout
        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        self.print_button = QPushButton("Print Scantron")
        self.print_button.clicked.connect(self.print_scantron)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)

        #creating items in custom layout
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setSuffix(" rows")
        self.row_add = QPushButton("+")
        self.row_add.clicked.connect(self.add_row_table)

        #adding to type layout
        self.type_layout.addWidget(self.type_title)
        self.type_layout.addLayout(self.select_layout)

        #adding to corresponding layout and select layout
        self.subject_layout.addWidget(self.type1)
        self.subject_layout.addWidget(self.combo1)
        self.subject_layout.addWidget(self.combo1_add)
        self.subject_layout.addWidget(self.combo1_delete)
        self.select_layout.addLayout(self.subject_layout)
        self.category_layout.addWidget(self.type2)
        self.category_layout.addWidget(self.combo2)
        self.category_layout.addWidget(self.combo2_add)
        self.category_layout.addWidget(self.combo2_delete)
        self.select_layout.addLayout(self.category_layout)
        self.number_layout.addWidget(self.type3)
        self.number_layout.addWidget(self.combo3)
        self.number_layout.addWidget(self.combo3_add)
        self.number_layout.addWidget(self.combo3_delete)
        self.select_layout.addLayout(self.number_layout)
        self.section_layout.addWidget(self.type4)
        self.section_layout.addWidget(self.combo4)
        self.section_layout.addWidget(self.combo4_add)
        self.section_layout.addWidget(self.combo4_delete)
        self.select_layout.addLayout(self.section_layout)
        self.select_layout.addWidget(self.loadButton)
        self.select_layout.addWidget(self.clearButton)

        #adding to detail layout
        self.detail_layout.addWidget(self.detail_title)
        self.detail_layout.addWidget(self.detail_info)
        self.detail_layout.addWidget(self.detail_combo)
        self.detail_layout.addWidget(self.detail_combo_add)
        self.detail_layout.addWidget(self.detail_combo_delete)

        #adding to custom layout
        self.custom_layout.addWidget(self.spinbox)
        self.custom_layout.addWidget(self.row_add)

        #adding to button layout
        self.button_layout.addWidget(self.import_button)
        self.button_layout.addWidget(self.export_button)
        self.button_layout.addWidget(self.print_button)
        self.button_layout.addWidget(self.save_button)

        #adding to overall layout
        self.layout.addLayout(self.type_layout)
        self.layout.addLayout(self.detail_layout)
        self.layout.addLayout(self.custom_layout)
        self.layout.addWidget(self.tableWidget)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def initComboBox(self, items, key = None):
        combo = QComboBox(self)
        if key == 0:
            self.subject = items[0]
            combo.addItem("None")
        for item in items:
            combo.addItem(item)
        return combo

    def initTable(self):
        self.keys = list(self.file_manager.get_tm_table_keys())
        # create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setFocusPolicy(Qt.StrongFocus)
        self.tableWidget.keyReleaseEvent = self.keyReleaseEvent

        self.row = 0
        self.col = 5

        self.tableWidget.setRowCount(self.row)
        self.tableWidget.setColumnCount(self.col)

        self.table_labels = ["Answer Type", "Question Type",
                        "Difficulty Level", "Correct Answer", "Delete"]

        header = self.tableWidget.horizontalHeader()
        #set the table column labels
        for i in range(0, len(self.table_labels)):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(self.table_labels[i]))
            if i == 0:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def add_row_table(self):
        old_row = self.row
        self.row += self.spinbox.value()

        for i in range(old_row, self.row):
            self.tableWidget.insertRow(i)
            for j in range(0, self.col):
                if j < 3:
                    temp = self.file_manager.get_tm_table_labels(self.keys[j])
                    temp.sort()
                    combobox = self.initComboBox( temp )
                    combobox.setEditable(True)
                    self.tableWidget.setCellWidget(i, j, combobox)
                elif j == 3:
                    lineEdit = QLineEdit()
                    self.tableWidget.setCellWidget(i, j, lineEdit)
                elif j == 4:
                    button = QPushButton(str(i))
                    button.clicked.connect(self.delete_row)
                    self.tableWidget.setCellWidget(i, j, button)

    def subject_added(self):
        self.combo1.clear()

        for subject in self.file_manager.get_tm_subject_labels():
            self.combo1.addItem(subject)



    def label_added(self):
        button = self.sender()
        check = True

        self.add_status = True
        if button == self.combo1_add:
            new_label = self.subject
            if self.subject == "":
                check = False
            else:
                self.file_manager.set_ready(False)
                check = self.file_manager.add_tm_subject_labels(new_label)
                self.file_manager.raw_table[new_label] = {}
                self.file_manager.save_file("ts")
                if check == False:
                    buttonReply = QMessageBox.warning(self, 'Warning', "That subject already exist!",
                                                      QMessageBox.Ok, QMessageBox.Ok)
                    return
                self.update_combobox(self.combo1)
                self.load_combobox()
        elif button == self.combo2_add:
            new_label = self.combo2.currentText()
            if self.combo2.currentText() == "":
                check = False
            else:
                check_status = self.file_manager.add_tm_category_labels(new_label, self.combo1.currentText())
                if check_status == 1:
                    buttonReply = QMessageBox.warning(self, 'Warning', "Add new subject with + button first!",
                                                      QMessageBox.Ok, QMessageBox.Ok)
                elif check_status == 2:
                    buttonReply = QMessageBox.warning(self, 'Warning', "That category already exist!",
                                                      QMessageBox.Ok, QMessageBox.Ok)
                self.update_combobox(self.combo2)

        elif button == self.combo3_add:
            new_label = self.combo3.currentText()
            if self.combo3.currentText() == "":
                check = False
            else:
                check_status = self.file_manager.add_tm_number_labels(new_label, self.combo1.currentText())
                if check_status == 1:
                    buttonReply = QMessageBox.warning(self, 'Warning', "Add new subject with + button first!",
                                                      QMessageBox.Ok, QMessageBox.Ok)
                elif check_status == 2:
                    buttonReply = QMessageBox.warning(self, 'Warning', "That number already exist!",
                                                      QMessageBox.Ok, QMessageBox.Ok)

                self.update_combobox(self.combo3)
        elif button == self.combo4_add:
            new_label = self.combo4.currentText()
            if self.combo4.currentText() == "":
                check = False
            else:
                if "SAT I" in self.subject:
                    sections = ["Reading", "Math Calculator", "Math No Calculator", "Writing and Language"]
                    for sect in sections:
                        self.file_manager.add_tm_section_labels(sect, self.combo1.currentText())
                else:
                    self.file_manager.add_tm_section_labels(new_label, self.combo1.currentText())
                self.update_combobox(self.combo4)
        else:
            new_label = self.detail_combo.currentText()
            if self.detail_combo.currentText() == "":
                check = False
            else:
                self.file_manager.add_tm_sat_subject_labels(new_label)
                self.update_combobox(self.detail_combo)

        if not check:
            buttonReply = QMessageBox.warning(self, 'Warning', "Input field cannot be empty!",
                                              QMessageBox.Ok, QMessageBox.Ok)

    def label_deleted(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to delete?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.No:
            return

        button = self.sender()
        check = True
        self.add_status = True
        if button == self.combo1_delete:
            if self.combo1.count() > 0:
                label = self.subject
                self.file_manager.delete_tm_subject_labels(label)
                self.update_combobox(self.combo1)
                self.load_combobox()
            else:
                check = False
        elif button == self.combo2_delete:
            if self.combo2.count() > 0:
                label = self.combo2.currentText()
                self.file_manager.delete_tm_category_labels(label, self.combo1.currentText())
                self.update_combobox(self.combo2)
            else:
                check = False
        elif button == self.combo3_delete:
            if self.combo3.count() > 0:
                label = self.combo3.currentText()
                self.file_manager.delete_tm_number_labels(label, self.combo1.currentText())
                self.update_combobox(self.combo3)
            else:
                check = False
        elif button == self.combo4_delete:
            if self.combo4.count() > 0:
                label = self.combo4.currentText()
                self.file_manager.delete_tm_section_labels(label, self.combo1.currentText())
                self.update_combobox(self.combo4)
            else:
                check = False
        else:
            if self.detail_combo.count() > 0:
                label = self.detail_combo.currentText()
                self.file_manager.delete_tm_sat_subject_labels(label)
                self.update_combobox(self.detail_combo)
            else:
                check = False

        if not check:
            buttonReply = QMessageBox.warning(self, 'Warning', "Input field cannot be empty!",
                                              QMessageBox.Ok, QMessageBox.Ok)

    def update_combobox(self, combobox):
        combobox.clear()
        if combobox == self.combo1:
            for i in range(0, self.file_manager.get_tm_subject_count() ):
                combobox.addItem(self.file_manager.get_tm_subject_labels()[i])
        elif combobox == self.combo2:
            for i in range(0, self.file_manager.get_tm_category_count( self.combo1.currentText() ) ):
                combobox.addItem(self.file_manager.get_tm_category_labels( self.combo1.currentText() )[i])
        elif combobox == self.combo3:
            for i in range(0, self.file_manager.get_tm_number_count(self.combo1.currentText() ) ):
                combobox.addItem(self.file_manager.get_tm_number_labels(self.combo1.currentText())[i])
        elif combobox == self.combo4:
            for i in range(0, self.file_manager.get_tm_section_count(self.combo1.currentText()) ):
                combobox.addItem(self.file_manager.get_tm_section_labels(self.combo1.currentText())[i])
        else:
            for i in range(0, self.file_manager.get_tm_sat_subject_count() ):
                combobox.addItem(self.file_manager.get_tm_sat_subject_labels()[i])
        self.add_status = False

    def subject_combo_changed(self):
        self.subject = self.sender().currentText()

    def load_combobox(self):

        self.update_combobox(self.combo2)
        self.update_combobox(self.combo3)
        self.update_combobox(self.combo4)
        #self.update_combobox(self.detail_combo)

    def refresh_combobox(self):
        if not self.add_status:
            self.update_combobox(self.combo2)
            self.update_combobox(self.combo3)
            self.update_combobox(self.combo4)
            #self.update_combobox(self.detail_combo)

    def refresh_table(self):
        print("labels: ", self.type_data)
        for i in range(0, self.row):
            for j in range(0, self.col):
                if j == 1:

                    if self.tableWidget.cellWidget(i, j).currentText() not in self.type_data:
                        self.file_manager.set_tm_table_labels(self.tableWidget.cellWidget(i, j).currentText())

                        break

        self.update_table()
        self.clear_table_rows()
        self.load_table()

    def update_table(self):
        table = []

        for i in range(0, self.row):
            temp = []
            for j in range(0, self.col-1):
                if j == 3:
                    text = self.tableWidget.cellWidget(i, j).text()
                else:
                    text = self.tableWidget.cellWidget(i, j).currentText()
                temp.append(text)
            table.append(temp)

        self.file_manager.set_tm_table_data(self.combo1.currentText(),
                                            self.combo2.currentText(),
                                            self.combo3.currentText(),
                                            self.combo4.currentText(),
                                            table
                                            )

        self.file_manager.save_file("tm", "table")

    def load_table(self):

        #check if all input fields is not empty and sat subject is None

        if ( self.combo1.currentText() != "" and
            self.combo2.currentText() != "" and
            self.combo3.currentText() != "" and
            self.combo4.currentText() != "" and self.detail_combo.currentText() == "None"
            ):

            table = self.file_manager.get_tm_table_data(self.combo1.currentText(),
                                                        self.combo2.currentText(),
                                                        self.combo3.currentText(),
                                                        self.combo4.currentText()
                                                        )

            if len(table) == 0:
                buttonReply = QMessageBox.warning(self, 'Warning', "Answer you selected is empty!",
                                                  QMessageBox.Ok, QMessageBox.Ok)
                self.clear_table_rows()
                return
            self.clear_table_rows()
            self.row = len(table)
            self.type_num = 0
            self.type_data = []
            self.load_status = True

            for i in range(0, self.row):
                self.tableWidget.insertRow(i)
                for j in range(0, self.col):
                    temp = 0
                    if j < len(self.keys):
                        temp = self.file_manager.get_tm_table_labels(self.keys[j])
                        temp.sort()
                    if j == 1:
                        self.type_num = len(temp)
                        self.type_data = temp
                    if j == 3:
                        lineEdit = QLineEdit()
                        lineEdit.setText(table[i][j])
                        self.tableWidget.setCellWidget(i, j, lineEdit)
                    elif j == 4:
                        button = QPushButton(str(i))
                        button.clicked.connect(self.delete_row)
                        self.tableWidget.setCellWidget(i, j, button)

                    else:
                        combobox = self.initComboBox( temp )
                        combobox.setCurrentText(table[i][j])
                        combobox.setEditable(True)
                        self.tableWidget.setCellWidget(i, j, combobox)


        else:
            buttonReply = QMessageBox.warning(self, 'Warning', "Input field cannot be empty and\nSAT subject should be None!",
                                              QMessageBox.Ok, QMessageBox.Ok)
            self.load_status = False

    def delete_row(self):
        num = self.sender().text()
        self.tableWidget.removeRow(int(num) )
        self.row -= 1

        #refresh button text
        for i in range(0, self.row):
            j = 4
            id = int( self.tableWidget.cellWidget(i, j).text() )
            if (id - 1 ) >= 0 and id > int(num):
                button = QPushButton(str(id-1))
                button.clicked.connect(self.delete_row)
                self.tableWidget.setCellWidget(i, j, button)

    def clear_table_rows(self):
        self.row = 0
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        self.load_status = False

    def keyReleaseEvent(self, e):

        if e.key() == Qt.Key_Tab:
            self.refresh_table()

    def save_file(self):
        self.file_manager.save_file("tm", "label")
        self.update_table()
        buttonReply = QMessageBox.information(self, 'Notification', "File was saved successfully!",
                                           QMessageBox.Ok , QMessageBox.Ok)

    def print_scantron(self):
        if self.load_status == False:
            buttonReply = QMessageBox.information(self, 'Notification', "Load the answers first before print!",
                                                  QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.sd.show()
            #print(self.file_manager.get_next_packetID())
