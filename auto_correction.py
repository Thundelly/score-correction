import os
import shutil
import datetime
import pathlib
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sat_grader import *
from psat_grader import *
from act_grader import *


class Auto_Correction(QWidget):
    def __init__(self, file_manager):
        super().__init__()
        #create directories
        cur_dir = os.getcwd()
        pathlib.Path(cur_dir + '/scans').mkdir(parents=True, exist_ok=True)
        pathlib.Path(cur_dir + '/results/success').mkdir(parents=True, exist_ok=True)
        pathlib.Path(cur_dir + '/results/fail').mkdir(parents=True, exist_ok=True)

        #create overall vertical layout
        self.layout = QVBoxLayout(self)
        self.file = None
        self.file_manager = file_manager
        self.sg = SAT_Grader(self.file_manager)
        self.pg = PSAT_Grader(self.file_manager)
        self.ag = ACT_Grader(self.file_manager)

        #creating extra layouts
        self.clear_layout = QVBoxLayout(self)
        self.folder_layout = QHBoxLayout(self)
        self.scan_layout = QVBoxLayout(self)
        self.correction_layout = QVBoxLayout(self)
        self.cor_layout = QHBoxLayout(self)
        self.image_layout = QVBoxLayout(self)
        self.summary_layout = QVBoxLayout(self)
        self.start_layout = QHBoxLayout(self)

        #creating items in clear layout
        self.one_title = QLabel("1. Clear scan image folder", self)
        self.one_title.setStyleSheet("color : blue;")

        #creating items in folder layout
        self.title1 = QLabel("Before start to scan for test sheet, clean scan folder first!", self)
        self.title1.setStyleSheet("color : red;")
        self.path = QLabel("Path", self)
        self.path.setStyleSheet("color : green;")
        self.clear_button = QPushButton("Clear folder", self)
        self.clear_button.clicked.connect(self.clear_path)
        self.check_button = QPushButton("Select folder", self)
        self.check_button.clicked.connect(self.get_path)
        self.combo = QSpinBox()
        self.combo.setMinimum(1)
        # ADDED CODE
        self.combo.setValue(32)
        self.select_check = QCheckBox("threshold:", self)
        # ADDED CODE
        self.select_check.setChecked(True)


        #creating items in scan layout
        self.title2 = QLabel("2. Scan test sheet", self)
        self.title2.setStyleSheet("color : blue;")


        #creating items in correction layout
        self.title3 = QLabel("3. Correction", self)
        self.title3.setStyleSheet("color : blue;")

        #creating items in image layout
        self.title4 = QLabel("Scan Image", self)
        self.title4.setStyleSheet("color : blue;")

        #image set up
        self.image = QLabel(self)
        pixmap = QPixmap(cur_dir + "/test_images/scan.jpg")
        pixmap = pixmap.scaled( pixmap.width()/3, pixmap.height()/3, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(pixmap)

        #creating itmes in summary layout
        self.title5 = QLabel("Correction Summary", self)
        self.title5.setStyleSheet("color : blue;")
        self.initTable()
        self.tableWidget.horizontalHeader().resizeSections(QHeaderView.Interactive)
        self.tableWidget.cellClicked.connect(self.highlight_row)

        #creating items in start layout
        self.date_title = QLabel("Test Date:", self)
        self.date = QLabel(self.get_date() , self)
        self.date.setStyleSheet("color : blue;")
        self.start_button = QPushButton("Start Correction", self)
        self.start_button.clicked.connect(self.start_correction)

        #adding to clear layout
        self.clear_layout.addWidget(self.one_title)
        self.clear_layout.addLayout(self.folder_layout)

        #adding to folder layout
        self.folder_layout.addWidget(self.title1)
        self.folder_layout.addWidget(self.path)
        self.folder_layout.addWidget(self.clear_button)
        self.folder_layout.addWidget(self.check_button)
        self.folder_layout.addWidget(self.combo)
        self.folder_layout.addWidget(self.select_check)

        #adding to scan layout
        self.scan_layout.addWidget(self.title2)


        #adding to correction layout
        self.correction_layout.addWidget(self.title3)
        self.correction_layout.addLayout(self.cor_layout)

        #adding to corr layout
        self.cor_layout.addLayout(self.image_layout)
        self.cor_layout.addLayout(self.summary_layout)

        #adding to image layout
        self.image_layout.addWidget(self.title4)
        self.image_layout.addWidget(self.image)

        #adding to summary layout
        self.summary_layout.addWidget(self.title5)
        self.summary_layout.addWidget(self.tableWidget)
        self.summary_layout.addLayout(self.start_layout)

        #adding to start layout
        self.start_layout.addWidget(self.date_title)
        self.start_layout.addWidget(self.date)
        self.start_layout.addWidget(self.start_button)

        #adding to overall layout
        self.layout.addLayout(self.clear_layout)
        self.layout.addLayout(self.scan_layout)
        self.layout.addLayout(self.correction_layout)
        self.setLayout(self.layout)

    def initTable(self):
        # create table
        self.tableWidget = QTableWidget()

        row = 0
        col = 6

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(col)

        table_labels = ["File Name", "Student ID", "Correct\nCounts", "Question\nCounts", "%", "Status"]

        #set the table column labels
        for i in range(0, len(table_labels)):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(table_labels[i]))

    def clear_path(self):
        if self.file == None:
            buttonReply = QMessageBox.warning(self, 'Warning', "Select your folder first!",
                                              QMessageBox.Ok, QMessageBox.Ok)
            return

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to clear the folder?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            folder = self.file
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)


    def get_path(self):
        self.file = str(QFileDialog.getExistingDirectory(self, "Select Location where scanned images are saved"))
        self.path.setText(self.file)


    def start_correction(self):

        if self.file == None or self.file == "":
            buttonReply = QMessageBox.warning(self, 'Warning', "Select your folder first!",
                                              QMessageBox.Ok, QMessageBox.Ok)
            return

        mode = -1
        if self.select_check.isChecked():
            self.sg.set_thresh(self.combo.value())
        else:
            self.sg.set_thresh(None)


        #clear success and fail folder
        cur_dir = os.getcwd()
        folder = cur_dir + '/results/success'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        folder = cur_dir + '/results/fail'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

        #go through scans folder
        folder = self.file
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path) and ".jpg" in file_path:
                    #print("Path: ", file_path)
                    self.sg.load_image(file_path)
                    packetID = self.sg.find_packetID()
                    pageNum = self.sg.find_pageNum()
                    #print("ID: ", packetID, "Page: ", pageNum)
                    #info = self.file_manager.get_packet_info( str(packetID) )
                    test_info = self.file_manager.get_packet_info( str(packetID) )
                    info = test_info
                    #print("info: ", test_info)
                    if "PSAT" in test_info["test_type"]:
                        self.pg.load_image(file_path)
                    elif "ACT" in test_info["test_type"]:
                        self.ag.load_image((file_path))

                    #print(test_info["test_type"])

                    if "2" in pageNum :
                        if "SAT I" in test_info["test_type"]:
                            #print("second page sat correction")
                            test_info = test_info["test_type"].split("-")
                            self.sg.load_answer(test_info[0], test_info[1], test_info[2], "Math No Calculator")
                            self.sg.grade_section_3()
                            self.file_manager.add_log( self.get_date(), info["student_id"], test_info[0]
                                                       , test_info[1], test_info[2], "Math No Calculator"
                                                       , (str(self.sg.correct) + "/" + str(self.sg.total_count))
                                                       , str(self.get_percent(self.sg.correct, self.sg.total_count))
                                                       , self.sg.student_answers
                                                       )
                            correct1 = self.sg.correct
                            total1 = self.sg.total_count

                            self.sg.load_answer(test_info[0], test_info[1], test_info[2], "Math Calculator")
                            self.sg.grade_section_4()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Math Calculator"
                                                      , (str(self.sg.correct) + "/" + str(self.sg.total_count))
                                                      , str(self.get_percent(self.sg.correct, self.sg.total_count))
                                                      , self.sg.student_answers
                                                      )
                            correct2 = self.sg.correct
                            total2 = self.sg.total_count

                            first_name = self.file_manager.get_student(info["student_id"])["first_name"]
                            last_name = self.file_manager.get_student(info["student_id"])["last_name"]
                            name = first_name + " " + last_name + ":" + info["test_type"] + ":Pg-" + pageNum
                            # name = name.replace(" ", "_")
                            name = name.replace(":", "_")
                            self.sg.save_image(name, self.get_date(1))
                            self.file_manager.save_file("log")
                            self.add_row(name, info["student_id"], str(correct1 + correct2), str(total1 + total2),
                                         str(self.get_percent(correct1 + correct2, total1 + total2)), "Success"
                                         )

                        elif "PSAT" in test_info["test_type"]:
                            # print("second page sat correction")
                            test_info = test_info["test_type"].split("-")
                            self.pg.load_answer(test_info[0], test_info[1], test_info[2], "Math No Calculator")
                            self.pg.grade_section_3()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Math No Calculator"
                                                      , (str(self.pg.correct) + "/" + str(self.pg.total_count))
                                                      , str(self.get_percent(self.pg.correct, self.pg.total_count))
                                                      , self.pg.student_answers
                                                      )
                            correct1 = self.pg.correct
                            total1 = self.pg.total_count

                            self.pg.load_answer(test_info[0], test_info[1], test_info[2], "Math Calculator")
                            self.pg.grade_section_4()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Math Calculator"
                                                      , (str(self.pg.correct) + "/" + str(self.pg.total_count))
                                                      , str(self.get_percent(self.pg.correct, self.pg.total_count))
                                                      , self.pg.student_answers
                                                      )
                            correct2 = self.pg.correct
                            total2 = self.pg.total_count

                            first_name = self.file_manager.get_student(info["student_id"])["first_name"]
                            last_name = self.file_manager.get_student(info["student_id"])["last_name"]
                            name = first_name + " " + last_name + ":" + info["test_type"] + ":Pg-" + pageNum

                            name = name.replace(":", "_")
                            self.pg.save_image(name, self.get_date(1))
                            self.file_manager.save_file("log")
                            self.add_row(name, info["student_id"], str(correct1 + correct2), str(total1 + total2),
                                         str(self.get_percent(correct1 + correct2, total1 + total2)), "Success"
                                         )

                        elif "ACT" in test_info["test_type"]:
                            test_info = test_info["test_type"].split("-")
                            self.ag.load_answer(test_info[0], test_info[1], test_info[2], "Reading")
                            self.ag.grade_section_3()

                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Reading"
                                                      , (str(self.ag.correct) + "/" + str(self.ag.total_count))
                                                      , str(self.get_percent(self.ag.correct, self.ag.total_count))
                                                      , self.ag.student_answers
                                                      )
                            correct1 = self.ag.correct
                            total1 = self.ag.total_count

                            self.ag.load_answer(test_info[0], test_info[1], test_info[2], "Science")
                            self.ag.grade_section_4()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Science"
                                                      , (str(self.ag.correct) + "/" + str(self.ag.total_count))
                                                      , str(self.get_percent(self.ag.correct, self.ag.total_count))
                                                      , self.ag.student_answers)

                            correct2 = self.ag.correct
                            total2 = self.ag.total_count

                            first_name = self.file_manager.get_student(info["student_id"])["first_name"]
                            last_name = self.file_manager.get_student(info["student_id"])["last_name"]
                            name = first_name + " " + last_name + ":" + info["test_type"] + ":Pg-" + pageNum

                            name = name.replace(":", "_")
                            self.ag.save_image(name, self.get_date(1))
                            self.file_manager.save_file("log")
                            self.add_row(name, info["student_id"], str(correct1 + correct2), str(total1 + total2),
                                         str(self.get_percent(correct1 + correct2, total1 + total2)), "Success"
                                         )


                    elif "1" in pageNum:
                        if "SAT I" in test_info["test_type"]:
                            test_info = test_info["test_type"].split("-")
                            # print("test_infO: ", test_info)
                            self.sg.load_answer(test_info[0], test_info[1], test_info[2], "Reading")
                            self.sg.grade_section_1()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Reading"
                                                      , (str(self.sg.correct) + "/" + str(self.sg.total_count))
                                                      , str(self.get_percent(self.sg.correct, self.sg.total_count))
                                                      , self.sg.student_answers
                                                      )
                            correct1 = self.sg.correct
                            total1 = self.sg.total_count

                            self.sg.load_answer(test_info[0], test_info[1], test_info[2], "Writing and Language")
                            self.sg.grade_section_2()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Writing and Language"
                                                      , (str(self.sg.correct) + "/" + str(self.sg.total_count))
                                                      , str(self.get_percent(self.sg.correct, self.sg.total_count))
                                                      , self.sg.student_answers
                                                      )
                            correct2 = self.sg.correct
                            total2 = self.sg.total_count

                            first_name = self.file_manager.get_student(info["student_id"])["first_name"]
                            last_name = self.file_manager.get_student(info["student_id"])["last_name"]
                            name = first_name + " " + last_name + ":" + info["test_type"] + ":Pg-" + pageNum
                            # name = name.replace(" ", "_")
                            name = name.replace(":", "_")
                            self.sg.save_image(name, self.get_date(1))
                            self.file_manager.save_file("log")
                            self.add_row(name, info["student_id"], str(correct1 + correct2), str(total1 + total2),
                                         str(self.get_percent(correct1 + correct2, total1 + total2)), "Success"
                                         )
                        elif "PSAT" in test_info["test_type"]:
                            test_info = test_info["test_type"].split("-")
                            self.pg.load_answer(test_info[0], test_info[1], test_info[2], "Reading")
                            self.pg.grade_section_1()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Reading"
                                                      , (str(self.pg.correct) + "/" + str(self.pg.total_count))
                                                      , str(self.get_percent(self.pg.correct, self.pg.total_count))
                                                      , self.pg.student_answers
                                                      )
                            correct1 = self.pg.correct
                            total1 = self.pg.total_count

                            self.pg.load_answer(test_info[0], test_info[1], test_info[2], "Writing and Language")
                            self.pg.grade_section_2()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Writing and Language"
                                                      , (str(self.pg.correct) + "/" + str(self.pg.total_count))
                                                      , str(self.get_percent(self.pg.correct, self.pg.total_count))
                                                      , self.pg.student_answers
                                                      )
                            correct2 = self.pg.correct
                            total2 = self.pg.total_count

                            first_name = self.file_manager.get_student(info["student_id"])["first_name"]
                            last_name = self.file_manager.get_student(info["student_id"])["last_name"]
                            name = first_name + " " + last_name + ":" + info["test_type"] + ":Pg-" + pageNum
                            # name = name.replace(" ", "_")
                            name = name.replace(":", "_")
                            self.pg.save_image(name, self.get_date(1))
                            self.file_manager.save_file("log")
                            self.add_row(name, info["student_id"], str(correct1 + correct2), str(total1 + total2),
                                         str(self.get_percent(correct1 + correct2, total1 + total2)), "Success"
                                         )
                        elif "ACT" in test_info["test_type"]:
                            test_info = test_info["test_type"].split("-")
                            self.ag.load_answer(test_info[0], test_info[1], test_info[2], "English")
                            self.ag.grade_section_1()

                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "English"
                                                      , (str(self.ag.correct) + "/" + str(self.ag.total_count))
                                                      , str(self.get_percent(self.ag.correct, self.ag.total_count))
                                                      , self.ag.student_answers
                                                      )
                            correct1 = self.ag.correct
                            total1 = self.ag.total_count

                            self.ag.load_answer(test_info[0], test_info[1], test_info[2], "Math")
                            self.ag.grade_section_2()
                            self.file_manager.add_log(self.get_date(), info["student_id"], test_info[0]
                                                      , test_info[1], test_info[2], "Math"
                                                      , (str(self.ag.correct) + "/" + str(self.ag.total_count))
                                                      , str(self.get_percent(self.ag.correct, self.ag.total_count))
                                                      , self.ag.student_answers)

                            correct2 = self.ag.correct
                            total2 = self.ag.total_count

                            first_name = self.file_manager.get_student(info["student_id"])["first_name"]
                            last_name = self.file_manager.get_student(info["student_id"])["last_name"]
                            name = first_name + " " + last_name + ":" + info["test_type"] + ":Pg-" + pageNum

                            name = name.replace(":", "_")
                            self.ag.save_image(name, self.get_date(1))
                            self.file_manager.save_file("log")
                            self.add_row(name, info["student_id"], str(correct1 + correct2), str(total1 + total2),
                                         str(self.get_percent(correct1 + correct2, total1 + total2)), "Success"
                                         )



                    #self.sg.show_image()

                    #self.change_image(file_path)
                    buttonReply = QMessageBox.information(self, 'Notification', "Correction completed!",
                                                          QMessageBox.Ok, QMessageBox.Ok)

            except Exception as e:
                print(e)
                packetID = self.sg.find_packetID()
                pageNum = self.sg.find_pageNum()
                info = self.file_manager.get_packet_info(str(packetID))
                first_name = self.file_manager.get_student(info["student_id"])["first_name"]
                last_name = self.file_manager.get_student(info["student_id"])["last_name"]
                name = first_name + " " + last_name + ":" + info["test_type"] + ":Pg-" + pageNum
                self.sg.save_image(name, self.get_date(1))
                #self.file_manager.save_file("log")
                self.add_row(name, info["student_id"], str(correct1 + correct2), str(total1 + total2),
                             str(self.get_percent(correct1 + correct2, total1 + total2)), "Failed"
                             )


    def get_percent(self, correct, total_count):
        return int( round(correct/float(total_count), 2) * 100)

    def change_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled( pixmap.width()/3, pixmap.height()/3)
        self.image.setPixmap(pixmap)

    def get_date(self, type=None):
        now = datetime.datetime.now()
        cur_date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
        if type != None:
            cur_date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)
        return cur_date

    def add_row(self, file_name, student_id, correct, total_count, percent, status):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem( file_name ) )
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(student_id))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(correct))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(total_count))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(percent))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, QTableWidgetItem(status))

    def highlight_row(self, row):
        self.tableWidget.selectRow(row)
        file_name = self.tableWidget.item( row , 0).text()
        self.show_detail(row, file_name)

    def show_detail(self, row, file_name ):
        file_path = os.getcwd() + "/results/success/" + self.get_date(1) + "/" + file_name
        self.change_image(file_path)


