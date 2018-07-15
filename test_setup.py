from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Test_Setup(QWidget):
    def __init__(self, file_manager):
        super().__init__()

        self.file_manager = file_manager
        self.loaded = False

        #create overall vertical layout
        self.layout = QHBoxLayout(self)

        #creating extra layouts
        self.part1 = QVBoxLayout(self)
        self.part2 = QVBoxLayout(self)
        self.part3 = QVBoxLayout(self)
        self.subject_layout = QVBoxLayout(self)
        self.match_layout = QVBoxLayout(self)
        self.thresh_layout = QHBoxLayout(self)
        self.score_layout = QVBoxLayout(self)
        self.row_layout = QHBoxLayout(self)
        self.r1 = QHBoxLayout(self)
        self.r2 = QHBoxLayout(self)
        self.question_layout = QVBoxLayout(self)
        self.r3 = QHBoxLayout(self)
        self.r4 = QHBoxLayout(self)
        self.rows_layout = QHBoxLayout(self)
        self.load_layout = QHBoxLayout(self)

        #creating items in subject layout
        self.subject_title = QLabel("Subject/Class", self)
        self.subject_title.setStyleSheet("color : blue;")
        self.initSubjTable()

        #creating items in match layout
        self.match_title = QLabel("Match Score Conversion Table", self)
        self.match_title.setStyleSheet("color : blue;")
        self.initMatchTable()

        #creating items in thresh layout
        self.save_thresh_button = QPushButton("Save Match")
        self.save_thresh_button.clicked.connect(self.save_selected)

        #creating items in score layout
        self.score_title = QLabel("Score Conversion Table", self)
        self.score_title.setStyleSheet("color : blue;")
        self.initScoreTable()
        self.table_save_button = QPushButton("Save Table")
        self.table_save_button.clicked.connect(self.save_table)

        #creating items in row layout
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setSuffix(" rows")
        self.row_add = QPushButton("+")
        self.row_add.clicked.connect(self.add_row)

        #creating items in r1 layout
        self.title1 = QLabel("Subject:", self)
        self.combo1 = self.initComboBox( self.file_manager.get_tm_subject_labels() )
        self.combo1.currentIndexChanged.connect(self.refresh_combobox)
        self.combo1.setEditable(True)
        self.add_button1 = QPushButton("+")
        self.add_button1.clicked.connect(self.add_to_combo)
        self.del_button1 = QPushButton("-")
        self.del_button1.clicked.connect(self.del_from_combo )

        self.title2 = QLabel("Type:", self)
        self.combo2 = self.initComboBox([])
        self.combo2.currentIndexChanged.connect(self.refreh_sub_subject)
        self.combo2.setEditable(True)
        self.add_button2 = QPushButton("+")
        self.add_button2.clicked.connect(self.add_to_combo)
        self.del_button2 = QPushButton("-")
        self.del_button2.clicked.connect(self.del_from_combo)

        #creating items in r2 layout
        self.title3 = QLabel("Sub.\nSubject:", self)
        self.combo3 = self.initComboBox([])
        self.combo3.setEditable(True)
        self.add_button3 = QPushButton("+")
        self.add_button3.clicked.connect(self.add_to_combo)
        self.del_button3 = QPushButton("-")
        self.del_button3.clicked.connect(self.del_from_combo)
        self.title4 = QLabel("Essay:", self)
        self.combo4 = self.initComboBox(["1", "2", "3", "4", "5", "6"])
        self.button1 = QPushButton("Load")
        self.button1.clicked.connect(self.load_table)

        #creating items in question layout
        self.question_title = QLabel("Question Type", self)
        self.question_title.setStyleSheet("color : blue;")
        self.initQuestionTable()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_question_type)

        #creating items in load layout
        self.button2 = QPushButton("Load")
        self.button2.clicked.connect(self.load_question_type)
        self.spinbox1 = QSpinBox()
        self.spinbox1.setMinimum(1)
        self.spinbox1.setSuffix(" rows")
        self.row_add1 = QPushButton("+")
        self.row_add1.clicked.connect(self.add_row1)

        #adding to part1 layout
        self.part1.addLayout(self.subject_layout)
        self.part1.addLayout(self.match_layout)

        #adding to subject_layout
        self.subject_layout.addWidget(self.subject_title)
        self.subject_layout.addWidget(self.subj_table)

        #adding to match layout
        self.match_layout.addWidget(self.match_title)
        self.match_layout.addWidget(self.match_table)
        self.match_layout.addLayout(self.thresh_layout)

        #adding to thresh layout
        self.thresh_layout.addWidget(self.save_thresh_button)

        #adding to part2 layout
        self.part2.addLayout(self.score_layout)

        #adding to score layout
        self.score_layout.addWidget(self.score_title)
        self.score_layout.addLayout(self.r1)
        self.score_layout.addLayout(self.r2)
        self.score_layout.addLayout(self.row_layout)
        self.score_layout.addWidget(self.score_table)
        self.score_layout.addWidget(self.table_save_button)

        #adding to row layout
        self.row_layout.addWidget(self.spinbox)
        self.row_layout.addWidget(self.row_add)

        #adding to r1 layout
        self.r1.addWidget(self.title1)
        self.r1.addWidget(self.combo1)
        self.r1.addWidget(self.add_button1)
        self.r1.addWidget(self.del_button1)
        self.r1.addWidget(self.title2)
        self.r1.addWidget(self.combo2)
        self.r1.addWidget(self.add_button2)
        self.r1.addWidget(self.del_button2)

        #adding to r2 layout
        self.r2.addWidget(self.title3)
        self.r2.addWidget(self.combo3)
        self.r2.addWidget(self.add_button3)
        self.r2.addWidget(self.del_button3)
        self.r2.addWidget(self.title4)
        self.r2.addWidget(self.combo4)
        self.r2.addWidget(self.button1)

        #adding to part3 layout
        self.part3.addLayout(self.question_layout)

        #adding to question layout
        self.question_layout.addWidget(self.question_title)
        self.question_layout.addLayout(self.load_layout)
        self.question_layout.addLayout(self.rows_layout)
        self.question_layout.addWidget(self.question_table)
        self.question_layout.addWidget(self.save_button)

        #adding to rows layout
        self.rows_layout.addWidget(self.spinbox1)
        self.rows_layout.addWidget(self.row_add1)

        #adding to load layout
        self.load_layout.addWidget(self.button2)


        #adding to overall layout
        self.layout.addLayout(self.part1)
        self.layout.addLayout(self.part2)
        self.layout.addLayout(self.part3)

        self.setLayout(self.layout)

    def initSubjTable(self):
        # create table
        self.subj_table = QTableWidget()

        self.subjects = self.file_manager.get_tm_subject_labels()

        self.row = len(self.subjects)
        self.col = 1

        row = self.row
        col = self.col

        self.subj_table.setRowCount(row)
        self.subj_table.setColumnCount(col)

        table_labels = ["Name"]

        header = self.subj_table.horizontalHeader()
        #set the table column labels
        for i in range(0, len(table_labels)):
            self.subj_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))
            if i == 0:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        #create comboxbox for each cell
        for i in range(0, row):
            for j in range(0, col):
                self.subj_table.setItem(i, j, QTableWidgetItem( self.subjects[i] ) )

    def initMatchTable(self):
        # create table
        self.match_table = QTableWidget()

        row = len(self.subjects)
        col = 2


        self.match_table.setRowCount(row)
        self.match_table.setColumnCount(col)

        table_labels = ["Test Sheet Type", "Conv. Table Type"]

        header = self.match_table.horizontalHeader()
        #set the table column labels
        for i in range(0, len(table_labels)):
            self.match_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))
            if i == 0:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        #create comboxbox for each cell
        for i in range(0, row):
            for j in range(0, col):
                if j == 0:
                    self.match_table.setItem(i, j, QTableWidgetItem(self.subjects[i]))
                else:
                    combo = QComboBox(self)
                    combo.addItem("None")
                    for key in self.file_manager.get_rt_types( self.subjects[i]).keys() :
                        combo.addItem(key)
                    if self.subjects[i] in self.file_manager.raw_table["Selected"].keys():
                        combo.setCurrentText( self.file_manager.raw_table["Selected"][self.subjects[i]] )

                    self.match_table.setCellWidget(i, j, combo )

    def save_selected(self):
        for i in range(0, self.row):

            subject = self.match_table.item(i, 0 ).text()
            type = self.match_table.cellWidget(i, 1).currentText()
            if type != "None":
                self.file_manager.update_selected(subject, type)

        self.file_manager.save_file("ts")
        buttonReply = QMessageBox.information(self, 'Notification', "Selection was saved successfully!",
                                              QMessageBox.Ok, QMessageBox.Ok)

    def initScoreTable(self):
        # create table
        self.score_table = QTableWidget()

        row = 20
        col = 3

        self.score_table.setRowCount(row)
        self.score_table.setColumnCount(col)

        table_labels = ["Score", "From", "To"]

        #set the table column labels
        for i in range(0, len(table_labels)):
            self.score_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))

        #create comboxbox for each cell
        for i in range(0, row):
            for j in range(0, col):
                self.score_table.setItem(i, j, QTableWidgetItem(""))

    def initQuestionTable(self):
        # create table
        self.question_table = QTableWidget()

        row = 20
        col = 1

        self.question_table.setRowCount(row)
        self.question_table.setColumnCount(col)

        table_labels = ["Question Type"]

        #set the table column labels
        for i in range(0, len(table_labels)):
            self.question_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))

        #create comboxbox for each cell
        for i in range(0, row):
            for j in range(0, col):
                self.question_table.setItem(i, j, QTableWidgetItem(""))

    def initComboBox(self, items):
        combo = QComboBox(self)
        for item in items:
            combo.addItem(item)
        return combo

    def refresh_subject(self):
        self.combo1.clear()

        for subject in self.file_manager.get_tm_subject_labels():
            self.combo1.addItem(subject)

    def refresh_combobox(self):
        self.combo2.clear()

        types = self.file_manager.get_rt_types(self.combo1.currentText() )
        if types != None:
            for key in types.keys():
                self.combo2.addItem(key)


    def refreh_sub_subject(self):
        self.combo3.clear()

        if self.combo2.currentText() != "":
            types = self.file_manager.get_rt_types(self.combo1.currentText())[self.combo2.currentText()]
            if types != None:
                for key in types.keys():
                    self.combo3.addItem(key)

    def load_table(self):
        self.clear_table("score")
        scores = self.file_manager.get_rt_types(self.combo1.currentText())[self.combo2.currentText()][self.combo3.currentText()]

        if "SAT" in self.combo1.currentText() or "ACT" in self.combo1.currentText():
            row = len(scores)
            col = 3

            self.score_table.setRowCount(row)
            self.score_table.setColumnCount(col)

            table_labels = ["Raw Score"]
            table_labels.append(self.combo3.currentText() + "\nSection\nScore" )
            table_labels.append("Delete")

            header = self.score_table.horizontalHeader()
            # set the table column labels
            for i in range(0, len(table_labels)):
                self.score_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))
                if i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)


            for i in range(0, row):
                self.score_table.setItem(i, 0, QTableWidgetItem( str(i) ))
                self.score_table.setItem(i, 1, QTableWidgetItem( str(scores[i] ) ))
                button = QPushButton(str(i))
                button.clicked.connect(self.delete_row)
                self.score_table.setCellWidget(i, 2, button)

    def refresh_table(self, type):
        if type == "subject":
            self.clear_table("subject")
            self.subjects = self.file_manager.get_tm_subject_labels()

            self.row = len(self.subjects)

            row = self.row
            col = self.col

            self.subj_table.setRowCount(row)

            table_labels = ["Name"]

            for i in range(0, row):
                for j in range(0, col):
                    self.subj_table.setItem(i, j, QTableWidgetItem(self.subjects[i]))
        if type == "match":
            self.clear_table("match")

            row = len(self.subjects)
            col = 2

            self.match_table.setRowCount(row)

            # create comboxbox for each cell
            for i in range(0, row):
                for j in range(0, col):
                    if j == 0:
                        self.match_table.setItem(i, j, QTableWidgetItem(self.subjects[i]))
                    else:
                        combo = QComboBox(self)
                        combo.addItem("None")
                        for key in self.file_manager.get_rt_types(self.subjects[i]).keys():
                            combo.addItem(key)
                        if self.subjects[i] in self.file_manager.raw_table["Selected"].keys():
                            combo.setCurrentText(self.file_manager.raw_table["Selected"][self.subjects[i]])

                        self.match_table.setCellWidget(i, j, combo)

    def clear_table(self, type):
        if type == "score":
            while self.score_table.rowCount() > 0:
                self.score_table.removeRow(0)
            count = 3
            while count > 0 :
                self.score_table.removeColumn(0)
                count -= 1
        elif type == "subject":
            while self.subj_table.rowCount() > 0:
                self.subj_table.removeRow(0)
        elif type == "match":
            while self.match_table.rowCount() > 0:
                self.match_table.removeRow(0)
        else:
            while self.question_table.rowCount() > 0:
                self.question_table.removeRow(0)

            count = 1
            while count > 0:
                self.question_table.removeColumn(0)
                count -= 1


    def add_row(self):
        num_rows = self.spinbox.value()
        while num_rows > 0:
            self.score_table.insertRow(self.score_table.rowCount())
            button = QPushButton(str(self.score_table.rowCount() - 1 ))
            button.clicked.connect(self.delete_row)
            self.score_table.setItem(self.score_table.rowCount() - 1, 0,
                                        QTableWidgetItem(str(self.score_table.rowCount() - 1)))
            self.score_table.setItem(self.score_table.rowCount() - 1, 1,
                                     QTableWidgetItem(""))
            self.score_table.setCellWidget( self.score_table.rowCount() - 1, 2, button)
            num_rows -= 1

    def add_row1(self):
        num_rows = self.spinbox1.value()
        while num_rows > 0:
            self.question_table.insertRow(self.question_table.rowCount())
            button = QPushButton(str(self.question_table.rowCount() - 1))
            button.clicked.connect(self.delete_row_question)
            self.question_table.setCellWidget(self.question_table.rowCount() - 1, 1, button)
            num_rows -= 1

    def delete_row(self):
        num = self.sender().text()
        self.score_table.removeRow(int(num))

        # refresh button text
        for i in range(0, self.score_table.rowCount() ):
            j = 2
            id = int(self.score_table.cellWidget(i, j).text())
            if id > int(num):
                button = QPushButton(str(id - 1))
                button.clicked.connect(self.delete_row)
                self.score_table.setCellWidget(i, j, button)

    def delete_row_question(self):
        num = self.sender().text()
        self.question_table.removeRow(int(num))

        # refresh button text
        for i in range(0, self.question_table.rowCount()):
            j = 1
            id = int(self.question_table.cellWidget(i, j).text())
            if id > int(num):
                button = QPushButton(str(id - 1))
                button.clicked.connect(self.delete_row_question)
                self.question_table.setCellWidget(i, j, button)

    def save_table(self):
        subject = self.combo1.currentText()
        sub_type = self.combo2.currentText()
        sub_subject = self.combo3.currentText()

        result = []
        change = False
        if "SAT" in subject or "PSAT" in subject or "ACT" in subject:
            for i in range(0, self.score_table.rowCount() ):
                text = self.score_table.item(i, 1).text()
                score = int(text)
                result.append(score)

            self.file_manager.save_rt(subject, sub_type, sub_subject, result)
            change = True

        if change == True:
            self.file_manager.save_file("ts")
            buttonReply = QMessageBox.information(self, 'Notification', "It was saved successfully!",
                                                  QMessageBox.Ok, QMessageBox.Ok)

    def add_to_combo(self):
        button = self.sender()

        if button == self.add_button1:
            check = self.file_manager.add_rt_subject(self.combo1.currentText())
            if check == 0:
                self.refresh_subject()
                self.refresh_table("subject")
                self.refresh_table("match")
                buttonReply = QMessageBox.information(self, 'Notification', "Added successfully!",
                                                      QMessageBox.Ok, QMessageBox.Ok)

            else:
                buttonReply = QMessageBox.information(self, 'Notification', "You cannot add same subject!",
                                                      QMessageBox.Ok, QMessageBox.Ok)

        elif button == self.add_button2:
            check = self.file_manager.add_rt_type(self.combo1.currentText(), self.combo2.currentText())
            if check == 0:
                self.refresh_combobox()
                self.refresh_table("match")
                buttonReply = QMessageBox.information(self, 'Notification', "Added successfully!",
                                                      QMessageBox.Ok, QMessageBox.Ok)

            else:
                buttonReply = QMessageBox.information(self, 'Notification', "You cannot add same type!",
                                                      QMessageBox.Ok, QMessageBox.Ok)
        elif button == self.add_button3:
            check = self.file_manager.add_rt_sub_subj(self.combo1.currentText(), self.combo2.currentText(),
                                                      self.combo3.currentText())
            if check == 0:
                self.refreh_sub_subject()
                buttonReply = QMessageBox.information(self, 'Notification', "Added successfully!",
                                                      QMessageBox.Ok, QMessageBox.Ok)

            else:
                buttonReply = QMessageBox.information(self, 'Notification', "You cannot add same sub subject!",
                                                      QMessageBox.Ok, QMessageBox.Ok)

    def del_from_combo(self):
        button = self.sender()
        subject = self.combo1.currentText()

        if button == self.del_button1:
            self.file_manager.del_rt_subject(subject)
            self.refresh_subject()
            self.refresh_table("subject")
            self.refresh_table("match")

            buttonReply = QMessageBox.information(self, 'Notification', "Deleted successfully!",
                                                  QMessageBox.Ok, QMessageBox.Ok)

        type = self.combo2.currentText()
        if button == self.del_button2:
            self.file_manager.del_rt_type(subject, type )
            self.refresh_combobox()
            self.refresh_table("match")

            buttonReply = QMessageBox.information(self, 'Notification', "Deleted successfully!",
                                                  QMessageBox.Ok, QMessageBox.Ok)

        sub_subj = self.combo3.currentText()
        if button == self.del_button3:
            self.file_manager.del_rt_sub_subj(subject, type, sub_subj)
            self.refreh_sub_subject()

    def load_question_type(self):
        self.loaded = True
        labels = self.file_manager.get_tm_table_labels("question_type")
        self.clear_table("question")

        row = len(labels)
        col = 2

        self.question_table.setRowCount(row)
        self.question_table.setColumnCount(col)

        table_labels = ["Question Type", "Delete"]

        header = self.question_table.horizontalHeader()
        # set the table column labels
        for i in range(0, len(table_labels)):
            self.question_table.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))
            if i == 0:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)


        # create comboxbox for each cell
        for i in range(0, row):

            self.question_table.setItem(i, 0, QTableWidgetItem( labels[i] ))
            button = QPushButton(str(i))
            button.clicked.connect(self.delete_row_question)
            self.question_table.setCellWidget(i, 1, button)

    def save_question_type(self):
        if self.loaded == False:
            buttonReply = QMessageBox.information(self, 'Notification', "Load data first!",
                                                  QMessageBox.Ok, QMessageBox.Ok)
            return

        data = []
        for i in range(0, self.question_table.rowCount() ):
            text = self.question_table.item(i, 0).text()
            if text == "":
                buttonReply = QMessageBox.information(self, 'Notification', "Can't have any empty rows!",
                                                      QMessageBox.Ok, QMessageBox.Ok)
                break
            else:
                data.append(text)

        self.file_manager.replace_tm_table_labels(data)

        self.file_manager.save_file("tm", "label")
        buttonReply = QMessageBox.information(self, 'Notification', "Saved successfully!",
                                              QMessageBox.Ok, QMessageBox.Ok)




