import json
import pathlib
import os
import copy
from shutil import *
cur_dir = os.getcwd() + "/database/"

class File_Manager():
    def __init__(self):
        with open(cur_dir + "labels.json", "r") as jsonFile:
            self.data = json.load(jsonFile)

        with open(cur_dir + "answers.json", "r") as jsonFile:
            self.answers = json.load(jsonFile)

        with open(cur_dir + "log.json", "r") as jsonFile:
            self.log = json.load(jsonFile)

        with open(cur_dir + "database.json", "r") as jsonFile:
            self.database = json.load(jsonFile)

        with open(cur_dir + "database_id.json", "r") as jsonFile:
            self.database_id = json.load(jsonFile)

        with open(cur_dir + "test_record.json", "r") as jsonFile:
            self.test_record = json.load(jsonFile)

        with open(cur_dir + "raw_table.json", "r") as jsonFile:
            self.raw_table = json.load(jsonFile)

        with open(cur_dir + "test_sheet_data.json", "r") as jsonFile:
            self.sheet_data = json.load(jsonFile)

        # test management labels
        self.tm_labels = self.data["test_management"]["test_type"]
        self.tm_table = self.data["test_management"]["table_label"]

        self.ready = True
        self.count = 0
        self.id_count = {}

    #function for ready
    def get_ready(self):
        return self.ready

    def set_ready(self, status):
        self.ready = status

    #function for subject labels
    def get_tm_subject_labels(self):
        self.tm_labels["subject"].sort()
        return self.tm_labels["subject"]

    def add_tm_subject_labels(self, subject):
        ready = True
        keys = self.tm_labels.keys()
        for key in keys:
            if key == "subject":
                if subject not in self.tm_labels[key]:
                    self.tm_labels["subject"].append(subject)
                    self.tm_labels["subject"].sort()
                else:
                    ready = False
            elif key != "sat_subject":
                if subject not in self.tm_labels[key].keys():
                    self.tm_labels[key][subject] = []
                else:
                    ready = False

        return ready




    def delete_tm_subject_labels(self, subject):
        keys = self.tm_labels.keys()
        for key in keys:
            if key == "subject":
                self.tm_labels[key].remove(subject)
            elif key != "sat_subject":
                del self.tm_labels[key][subject]

    def get_tm_subject_count(self):
        return len(self.tm_labels["subject"])

    #function for category labels
    def get_tm_category_labels(self, subject):
        self.tm_labels["category"][subject].sort()
        return self.tm_labels["category"][subject]

    def add_tm_category_labels(self, category, subject):
        if subject not in self.tm_labels["category"].keys():
            return 1
        else:
            if category not in self.tm_labels["category"][subject]:
                self.tm_labels["category"][subject].append(category)
                self.tm_labels["category"][subject].sort()
                return 0
            else:
                return 2

    def delete_tm_category_labels(self, category, subject):
        self.tm_labels["category"][subject].remove(category)

    def get_tm_category_count(self, subject):
        if subject != "None":
            return len(self.tm_labels["category"][subject])
        return None

    #functions for number labels
    def get_tm_number_labels(self, subject):
        self.tm_labels["number"][subject].sort()
        return self.tm_labels["number"][subject]

    def add_tm_number_labels(self, number, subject):
        if subject not in self.tm_labels["number"].keys():
            return 1
        else:
            if number not in self.tm_labels["number"][subject]:
                self.tm_labels["number"][subject].append(number)
                self.tm_labels["number"][subject].sort()
                return 0
            else:
                return 2


    def delete_tm_number_labels(self, number, subject):
        self.tm_labels["number"][subject].remove(number)

    def get_tm_number_count(self, subject):
        return len(self.tm_labels["number"][subject])

    #functions for section labels
    def get_tm_section_labels(self, subject):
        self.tm_labels["section"][subject].sort()
        return self.tm_labels["section"][subject]

    def add_tm_section_labels(self, section, subject):
        self.tm_labels["section"][subject].append(section)
        self.tm_labels["section"][subject].sort()

    def delete_tm_section_labels(self, section, subject):
        self.tm_labels["section"][subject].remove(section)

    def get_tm_section_count(self, subject):
        return len(self.tm_labels["section"][subject])

    #functions for sat subject labels
    def get_tm_sat_subject_labels(self):
        self.tm_labels["sat_subject"].sort()
        return self.tm_labels["sat_subject"]

    def add_tm_sat_subject_labels(self, sat_subject):
        self.tm_labels["sat_subject"].append(sat_subject)
        self.tm_labels["sat_subject"].sort()

    def delete_tm_sat_subject_labels(self, sat_subject):
        self.tm_labels["sat_subject"].remove(sat_subject)

    def get_tm_sat_subject_count(self):
        return len(self.tm_labels["sat_subject"])

    def get_tm_table_keys(self):
        return self.tm_table.keys()

    def get_tm_table_labels(self, key):
        return self.tm_table[key]

    def set_tm_table_labels(self, new_label):
        self.tm_table["question_type"].append(new_label)
        self.tm_table["question_type"].sort()

    def replace_tm_table_labels(self, data):
        self.tm_table["question_type"] = data

    def get_tm_table_data(self, subject, category, number, section):
        data = 0
        try:
            return self.answers[subject][category][number][section]
        except:
            return []

    def set_tm_table_data(self, subject, category, number, section, new_answers):
        if subject not in list(self.answers.keys() ):
            self.answers[subject] = {}

        if category not in list(self.answers[subject].keys()):
            self.answers[subject][category] = {}

        if number not in list(self.answers[subject][category].keys()):
            self.answers[subject][category][number] = {}

        if section not in list(self.answers[subject][category][number].keys()):
            self.answers[subject][category][number][section] = []

        self.answers[subject][category][number][section] = new_answers

    def get_log(self, date):
        if date in self.log.keys():
            print(self.log[date])
            return self.log[date]
        else:
            return []

    def add_log(self, date ,student_id, subject, category, number, section, score, percent, data):
        if date not in self.log.keys():
            self.log[date] = []

        temp = [student_id, subject, category, number, section, score, percent, data]
        self.log[date].append(temp)

    def get_user_info(self, id):
        if id in self.database.keys():
            #user exists
            return [self.database[id]["first_name"],
                    self.database[id]["last_name"],
                    self.database[id]["birth_date"],
                    self.database[id]["grade"],
                    id
                    ]
        else:
            return None

    def get_number_of_student(self):
        return [self.database_id["nextID"]]

    def get_student_keys(self):
        return self.database.keys()

    def get_student(self, id):
        if id in self.database.keys():
            #user exists
            return self.database[id]
        else:
            return None

    def get_next_studentID(self):
        self.student_id = self.database_id["nextID"]
        self.database_id["nextID"] += 1
        print(self.student_id)
        return self.student_id

    def add_student_to_database(self, first, last, birth_date, grade):
        self.database[self.student_id] = {
            "first_name": first,
            "last_name": last,
            "birth_date": birth_date,
            "grade": grade
        }

    def add_student_to_test_record(self):
        self.test_record[self.student_id] = {
            "test_info": {}
        }

    def update_student_info(self, f, l, b, g, id, turn):
        dict = list(self.database[id].values())
        first = dict[0]
        last = dict[1]
        birth = dict[2]
        grade = dict[3]

        if turn == 1:
            self.database[id] = {
                "first_name": f,
                "last_name": last,
                "birth_date": birth,
                "grade": grade
            }
            self.save_file("student_data")
        elif turn == 2:
            self.database[id] = {
                "first_name": first,
                "last_name": l,
                "birth_date": birth,
                "grade": grade
            }
            self.save_file("student_data")
        elif turn == 3:
            self.database[id] = {
                "first_name": first,
                "last_name": last,
                "birth_date": b,
                "grade": grade
            }
            self.save_file("student_data")
        elif turn == 4:
            self.database[id] = {
                "first_name": first,
                "last_name": last,
                "birth_date": birth,
                "grade": g
            }
            self.save_file("student_data")


    def get_test_info(self, id):
        if id in self.test_record.keys():
            #user exists
            return self.test_record[id]["test_info"]
        else:
            return None

    def save_test_to_student(self, id, date, test_info):
        student = self.test_record[id]
        if "test_info" not in student.keys():
            student["test_info"] = {}

        if date not in student["test_info"].keys():
            student["test_info"][date] = []
        temp = test_info.copy()
        temp.pop(0)
        student["test_info"][date].append(temp)

    #raw table methods
    def get_rt_types(self, subject):
        if subject in self.raw_table.keys():
            return self.raw_table[subject]
        else:
            return None

    def update_selected(self, subject, type):
        self.raw_table["Selected"][subject] = type

    def add_rt_subject(self, subject):
        if subject == "":
            return 1
        if subject not in self.raw_table.keys():
            self.raw_table[subject] = {}
            self.add_tm_subject_labels(subject)
            return 0
        else:
            return 1

    def del_rt_subject(self, subject):
        if subject == "":
            return
        del self.raw_table[subject]
        self.delete_tm_subject_labels(subject)

    def add_rt_type(self, subject, type):
        if subject == "" or type == "":
            return 1

        if subject in self.raw_table.keys():
            if type not in self.raw_table[subject].keys():
                self.raw_table[subject][type] = {}
                return 0
            else:
                return 1
        else:
            return 1

    def del_rt_type(self, subject, type):
        if subject == "" or type == "":
            return
        del self.raw_table[subject][type]

    def add_rt_sub_subj(self, subject, type, sub_subj):
        if subject == "" or type == "" or sub_subj == "":
            return

        if subject in self.raw_table.keys():
            if type in self.raw_table[subject].keys():
                if sub_subj not in self.raw_table[subject][type].keys():
                    self.raw_table[subject][type][sub_subj] = []
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 1

    def del_rt_sub_subj(self, subject, type, sub_subj):
        if subject == "" or type == "" or sub_subj == "":
            return

        del self.raw_table[subject][type][sub_subj]

    def save_rt(self, subject, sub_type, sub_subject, data):
        self.raw_table[subject][sub_type][sub_subject] = data

    def get_rt(self, subject, section):
        if subject not in self.raw_table.keys():
            return None
        else: #subject exist
            selected = self.raw_table["Selected"][subject]
            if section not in self.raw_table[subject][selected].keys():
                return None
            else:
                return self.raw_table[subject][selected][section]


    def get_next_packetID(self):
        # print(self.sheet_data["nextID"])
        packet_id = self.sheet_data["nextID"]
        nums = list(packet_id)

        t_d = int(nums[0])
        o_d = int(nums[1])

        o_d += 1
        if o_d == 10:
            o_d = 0
            t_d += 1

        if t_d == 10:
            t_d = 0

        t_d = str(t_d)
        o_d = str(o_d)
        self.sheet_data["nextID"] = t_d + o_d

        # self.sheet_data["nextID"] += 1
        # if self.sheet_data["nextID"] > 9:
        #     self.sheet_data["nextID"] = 0

        return list(packet_id)

    def create_packetID(self, packet_id, student_id, date, test_type):
        self.sheet_data["data"][packet_id] = {
            "student_id": student_id,
            "date": date,
            "test_type": test_type
        }

    def get_packet_info(self, packet_id):
        if packet_id in self.sheet_data["data"].keys():
            # if packet_id not in self.id_count.keys():
            #     self.id_count[packet_id] = 1
            # else:
            #     self.id_count[packet_id] += 1

            # if self.id_count[packet_id] == 2:
            #     temp = self.sheet_data["data"][packet_id].copy()
            #
            #     del self.sheet_data["data"][packet_id]
            #     self.save_file("packet")
            #     # self.count = 0
            #     return temp
            return self.sheet_data["data"][packet_id]
        else:
            return None

    def save_file(self, tab=None, type=None):
        if tab == "tm":
            if type == "label":
                with open(cur_dir + "labels.json", "w") as jsonFile:
                    json.dump(self.data, jsonFile, indent=4)
            elif type == "table":
                with open(cur_dir + "answers.json", "w") as jsonFile:
                    json.dump(self.answers, jsonFile, indent=4)
        elif tab == "cr":
            with open(cur_dir + "test_record.json", "w") as jsonFile:
                json.dump(self.test_record, jsonFile, indent=4)
            with open(cur_dir + "test_record.json", "r") as jsonFile:
                self.test_record = json.load(jsonFile)
        elif tab == "ts":
            with open(cur_dir + "raw_table.json", "w") as jsonFile:
                json.dump(self.raw_table, jsonFile, indent=4)
        elif tab == "packet":
            with open(cur_dir + "test_sheet_data.json", "w") as jsonFile:
                json.dump(self.sheet_data, jsonFile, indent=4)
        elif tab == "log":
            with open(cur_dir + "log.json", "w") as jsonFile:
                json.dump(self.log, jsonFile, indent=4)
        elif tab == "student_data":
            with open(cur_dir + "database.json", "w") as jsonFile:
                json.dump(self.database, jsonFile, indent=4)
            with open(cur_dir + "database.json", "r") as jsonFile:
                self.database = json.load(jsonFile)
        elif tab == "student_data_id":
            with open(cur_dir + "database_id.json", "w") as jsonFile:
                json.dump(self.database_id, jsonFile, indent=4)
            with open(cur_dir + "database_id.json", "r") as jsonFile:
                self.database_id = json.load(jsonFile)
