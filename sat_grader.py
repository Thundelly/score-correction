from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import pytesseract
import argparse
import imutils
import cv2
import copy
import os
from PIL import Image
from number_ml import *
from math import sqrt
import datetime
import pathlib

class SAT_Grader():
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.im = None
        self.score_table = {}
        self.score_table["1"] = None
        self.score_table["2"] = None
        self.score_table["3"] = None
        self.score_table["4"] = None

        self.total_count1 = None
        self.total_count2 = None

        self.th = None

        self.key_map = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "/": 0,
            ".": [0, 1],
            "0": [2, 1],
            "1": [1, 3, 2],
            "2": [2, 4, 3],
            "3": [3, 5, 4],
            "4": [4, 6, 5],
            "5": [5, 7, 6],
            "6": [6, 8, 7],
            "7": [7, 9, 8],
            "8": [8, 10, 9],
            "9": [9, 11, 10]
        }

        self.bubble_map = {
            "0": "A",
            "1": "B",
            "2": "C",
            "3": "D"
        }

        self.number_map = {
            "0": [".", "/", "/", "."],
            "1": ["1", ".", ".","0"],
            "2": ["2", "0", "0", "1"],
            "3": ["3", "1", "1", "2"],
            "4": ["4", "2", "2", "3"],
            "5": ["5", "3", "3", "4"],
            "6": ["6", "4", "4", "5"],
            "7": ["7", "5", "5", "6"],
            "8": ["8", "6", "6", "7"],
            "9": ["9", "7", "7", "8"],
            "10": [" ", "8", "8", "9"],
            "11": [" ", "9", "9", " "],
            "B": [" ", " ", " ", " "]

        }

    def get_date(self):
        now = datetime.datetime.now()
        cur_date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
        return cur_date

    def set_thresh(self, th):
        self.th = th


    def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    def load_image(self, file_path):

        self.im = cv2.imread(file_path)
        self.im = self.image_resize(self.im, height=800)

    def save_image(self, filename, date):

        cur_dir = os.getcwd()
        pathlib.Path(cur_dir + '/results/success/' + date).mkdir(parents=True, exist_ok=True)
        #print("Path: ",  cur_dir + '/results/success/' + date + '/' + filename + '.jpg')
        #os.path.join(os.path.expanduser('~'), 'Desktop', 'tropical_image_sig5.bmp'
        #filename = filename.replace(" ", "_")
        filename = filename.replace(":", "_")

        cv2.imwrite( os.path.join(cur_dir, 'results', 'success', date, filename + '.jpg'), self.im  )
        #print(os.path.join(cur_dir, 'results', 'success', date, filename + '.jpg') )
        #cv2.imwrite( cur_dir + '/results/success/' + date + '/' + filename + '.jpg', self.im)

    def load_answer(self, subject, category, number, section):
        self.ANSWER_KEY = []
        self.ANSWER_DESC = []

        self.subject = subject
        self.category = category
        self.number = number
        self.section = section

        answers = self.file_manager.get_tm_table_data(subject, category, number, section)
        key1 = None
        for i in range(0, len(answers) ):

            if self.hasNumbers(answers[i][3]):
                key1 = answers[i][3]
            else:
                key1 = self.key_map[answers[i][3].replace(" ", "")]

            # print("Answer: ", key1)
            self.ANSWER_KEY.append(key1)
            temp = [ answers[i][0], answers[i][1], answers[i][2] ]
            self.ANSWER_DESC.append(temp)


    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)


    def get_score(self, sect_num):
        if self.score_table[sect_num] is not None:
            return self.score_table[sect_num]

    def show_image(self):
        cv2.imshow("Corrected", self.im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def find_pageNum(self):
        x1 = 450
        x2 = 550
        y1 = 600
        y2 = 725

        rect = np.array( [(x1, y1), (x2, y1), (x2, y2), (x1,y2 )] , dtype = "float32")
        maxWidth = x2 - x1
        maxHeight = y2 - y1


        im = self.im

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")




        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(im, M, (maxWidth, maxHeight))

        # cv2.imshow("Test", warped)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        number_ml = Number_ML()
        return number_ml.find_numbers(warped, "page")

    def find_packetID(self):

        #first number
        x1 = 152
        x2 = 182
        y1 = 600
        y2 = 725

        rect = np.array( [(x1, y1), (x2, y1), (x2, y2), (x1,y2 )] , dtype = "float32")
        maxWidth = x2 - x1
        maxHeight = y2 - y1

        im = self.im

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(im, M, (maxWidth, maxHeight))

        # cv2.imshow("Test", warped)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        number_ml = Number_ML()
        num1 = number_ml.find_numbers(warped, "packet")

        x1 = 183
        x2 = 213
        y1 = 600
        y2 = 725

        rect = np.array([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], dtype="float32")
        maxWidth = x2 - x1
        maxHeight = y2 - y1

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(im, M, (maxWidth, maxHeight))

        # cv2.imshow("Test", warped)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        num2 = number_ml.find_numbers(warped, "packet")

        return str(num1) + str(num2)

    def grade_section_1(self):

        im = self.im


        sections = []

        height = 116
        width = 50
        x_steps = [(0, 0), (75, 71), (73, 74), (74, 74), (75, 75), (74, 74)]
        init_steps = [(133, 314), (118, 448)]

        sec1_end = 350
        sec2_end = 495

        x1 = init_steps[0][0]
        x2 = x1 + width

        y1 = init_steps[0][1]
        y2 = y1 + height
        end = 6

        for x in range(0, end):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            sect = im[y1:y2, x1:x2]
            if x == 4:
                y2 = sec1_end
            sections.append(sect)


        ANSWER_KEY = self.ANSWER_KEY

        correct = 0
        count = 0

        student_answers = []
        total_count = 0
        correct = 0

        for sec in sections:

            imgray = cv2.cvtColor(sec, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            im2, cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            docCnt = None

            if len(cnts) > 0:
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                for c in cnts:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    if len(approx) == 4:
                        docCnt = approx
                        #cv2.drawContours(im, [docCnt], -1, (0, 255, 0), 2)
                        break

            warped = four_point_transform(imgray, docCnt.reshape(4, 2))

            thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        #cv2.drawContours(sec1, cnts, -1, (0, 0, 255), 1)


            questionCnts = []

            for c in cnts:
                # compute the bounding box of the contour, then use the
                # bounding box to derive the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                #print("w,h,ar: ", w, h, ar)
                # in order to label the contour as a question, region
                # should be sufficiently wide, sufficiently tall, and
                # have an aspect ratio approximately equal to 1
                if w >= 2 and h >= 2 and ar >= 0.8 and ar <= 1.4:
                    questionCnts.append(c)

            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

            #cv2.drawContours(sec, questionCnts, 0, (0,0,255), 1)



            #print("count: ", len(questionCnts))



            for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
                cnts = contours.sort_contours(  questionCnts[i:i + 4]  )[0]
                count += 1
                bubbled = None
                max = None
                min = None
                blank = False

                for (j, c) in enumerate(cnts):

                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)

                    if bubbled is None:
                        bubbled = (total, j)
                        max = total
                        min = total
                    if total > max:
                        max = total
                        bubbled = (total, j)
                    if total < min:
                        min = total

                print(bubbled[0])
                if self.th is not None:
                    if bubbled[0] <= self.th:
                        blank = True
                # if max - min < 8:
                #     blank = True


                k = ANSWER_KEY[total_count]
                total_count += 1

                temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                        self.bubble_map[str(bubbled[1])]]

                # print("#: ", total_count ," real key: ", self.bubble_map[str(k)], " user ans: ", self.bubble_map[str(bubbled[1])] )
                color = None
                if blank == True:
                    temp.append("B")
                elif k == bubbled[1]:
                    color = (0, 255, 0)  # green
                    correct += 1
                    temp.append("C")
                else:
                    temp.append("W")
                    color = (0, 0, 255)  # red


                if color != None:
                    cv2.drawContours(sec, [cnts[k]], -1, color, 1)

                cv2.drawContours(sec, [cnts[k]], -1, color, 1)
                student_answers.append(temp)

        self.student_answers = student_answers
        self.correct = correct
        self.total_count = total_count
        #print("Score/Total:", correct, "/", total_count)



    def grade_section_2(self):

        im = self.im

        sections = []

        height = 116
        width = 50
        x_steps = [(0, 0), (75, 71), (73, 74), (74, 74), (75, 75), (74, 74)]
        init_steps = [(133, 314), (133, 467)]

        sec1_end = 330
        sec2_end = 495

        x1 = init_steps[1][0]
        x2 = x1 + width

        y1 = init_steps[1][1]
        y2 = y1 + height
        end = 5

        for x in range(0, end):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            sect = im[y1:y2, x1:x2]
            sections.append(sect)


        ANSWER_KEY = self.ANSWER_KEY

        count = 0
        total_count = 0
        correct = 0
        student_answers = []

        for sec in sections:


            imgray = cv2.cvtColor(sec, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            im2, cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            docCnt = None

            if len(cnts) > 0:
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                for c in cnts:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    if len(approx) == 4:
                        docCnt = approx

                        break

            warped = four_point_transform(imgray, docCnt.reshape(4, 2))

            thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

            cnts = cnts[0] if imutils.is_cv2() else cnts[1]



            questionCnts = []

            for c in cnts:
                # compute the bounding box of the contour, then use the
                # bounding box to derive the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                #print("w,h,ar: ", w, h, ar)
                # in order to label the contour as a question, region
                # should be sufficiently wide, sufficiently tall, and
                # have an aspect ratio approximately equal to 1
                if w >= 2 and h >= 2 and ar >= 0.8 and ar <= 1.4:
                    questionCnts.append(c)

            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

            #print("count: ", len(questionCnts))



            for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
                cnts = contours.sort_contours(  questionCnts[i:i + 4]  )[0]
                count += 1
                bubbled = None
                max = None
                min = None
                blank = False

                for (j, c) in enumerate(cnts):

                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)

                    if bubbled is None:
                        bubbled = (total, j)
                        max = total
                        min = total
                    if total > max:
                        max = total
                        bubbled = (total, j)
                    if total < min:
                        min = total

                # if max - min < 8:
                #     blank = True

                print(bubbled[0])
                if self.th is not None:
                    if bubbled[0] <= self.th:
                        blank = True

                k = ANSWER_KEY[total_count]
                total_count += 1
                color = None
                temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                        self.bubble_map[str(bubbled[1])]]

                if blank == True:
                    temp.append("B")
                elif k == bubbled[1]:
                    color = (0, 255, 0)  # green
                    correct += 1
                    temp.append("C")

                else:
                    color = (0, 0, 255)
                    temp.append("W")

                if color != None:
                    cv2.drawContours(sec, [cnts[k]], -1, color, 1)

                student_answers.append(temp)

        self.student_answers = student_answers
        self.correct = correct
        self.total_count = total_count
        #print("Score/Total:", correct, "/", count)


    def grade_section_3(self):

        im = self.im

        student_answers = []

        sections = []

        height = 179
        width = 50

        x_steps = [(0, 0), (73, 75), (76, 74), (73, 74), (74, 75), (74, 74)]
        init_steps = [(133, 80)]

        sec1_end = 101
        sec2_end = 495

        x1 = init_steps[0][0]
        x2 = x1 + width

        y1 = init_steps[0][1]
        y2 = y1 + height
        end = 6

        for x in range(0, end):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            if x > 0:
                height = 150
                y1 = 104
                y2 = y1 + height
            sect = im[y1:y2, x1:x2]
            sections.append(sect)
            # cv2.imshow(str(x), sect)

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        ANSWER_KEY = self.ANSWER_KEY

        count = 0
        correct = 0
        total_count = 0

        check = True
        for sec in sections:
            count += 1
            imgray = cv2.cvtColor(sec, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            im2, cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            docCnt = None

            if len(cnts) > 0:
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                for c in cnts:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    if len(approx) == 4:
                        docCnt = approx
                        # cv2.drawContours(im, [docCnt], -1, (0, 255, 0), 2)
                        break

            warped = four_point_transform(imgray, docCnt.reshape(4, 2))

            thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

            questionCnts = []
            ori = []
            for c in cnts:
                # compute the bounding box of the contour, then use the
                # bounding box to derive the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                # print("w,h,ar: ", w, h, ar)
                # in order to label the contour as a question, region
                # should be sufficiently wide, sufficiently tall, and
                # have an aspect ratio approximately equal to 1
                if w >= 2 and h >= 2 and ar >= 0.8 and ar <= 1.4:
                    questionCnts.append(c)
                    ori.append(c)

            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
            ori = contours.sort_contours(ori)[0]

            inc = 4
            start = 0
            num = 0
            end = 10
            user_answer = []
            if count > 1:
                total_count += 1
                q = total_count

                pos = []

                while num < 4:
                    cnts = contours.sort_contours(ori[start:end], method="top-to-bottom")[0]

                    bubbled = None
                    if len(cnts) > 11 and check == True:
                        cnt_copy = []
                        for x in range(0, 12):
                            cnt_copy.append(cnts[x])

                        cnts = contours.sort_contours(cnt_copy,  method="top-to-bottom")[0]
                        check = False


                    #print("count: ", len(cnts))
                    blank = False
                    min = None
                    max = None


                    for (j, c) in enumerate(cnts):

                        mask = np.zeros(thresh.shape, dtype="uint8")
                        cv2.drawContours(mask, [c], -1, 255, -1)
                        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                        total = cv2.countNonZero(mask)


                        if bubbled is None:
                            max = total
                            min = total
                            bubbled = (total, j)
                        if total >= (bubbled[0] ):
                            max = total
                            bubbled = (total, j)
                        if min > total and num > 1:
                            min = total

                    limit = None
                    if num < 2:
                        limit = 8
                    else:
                        limit = 7


                    # if (max - min) < limit and (max-min) != 0:
                    #     blank = True
                    if self.th is not None:
                        if bubbled[0] <= self.th:
                            blank = True

                    if blank == False:
                        user_answer.append(str(bubbled[1]))
                        pos.append( cnts[bubbled[1]] )
                    else:
                        user_answer.append("B")

                    num += 1
                    if num == 3:
                        start = end
                        end += 11
                    else:
                        start = end
                        end += 12

                k = ANSWER_KEY[q-1]

                answer = ""
                for x in range(0, len(user_answer) ):
                    answer += self.number_map[user_answer[x]][x]

                color = (0, 0, 255)  # red
                # print("user answer: ", answer, " real answer: ", k)
                # print("real_answer: ", k)


                temp = [self.ANSWER_DESC[q-1][0], self.ANSWER_DESC[q-1][1], self.ANSWER_DESC[q-1][2], answer]

                k = k.split(",")

                answer_res = False
                for x in k:
                    if x in answer:
                        correct += 1
                        color = (0, 255, 0)  # green
                        answer_res = True
                        break



                if answer_res == True:
                    temp.append("C")
                else:
                    temp.append("W")


                for item in pos:
                    cv2.drawContours(sec, item, -1, color, 1)
                student_answers.append(temp)



            else: # none number insert answers

                for (q, i) in enumerate(np.arange(start, len(questionCnts), inc)):
                    cnts = contours.sort_contours(questionCnts[i:i + inc])[0]
                    bubbled = None
                    max = None
                    min = None
                    blank = False

                    for (j, c) in enumerate(cnts):

                        mask = np.zeros(thresh.shape, dtype="uint8")
                        cv2.drawContours(mask, [c], -1, 255, -1)
                        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                        total = cv2.countNonZero(mask)

                        if bubbled is None:
                            bubbled = (total, j)
                            max = total
                            min = total
                        if total > max:
                            max = total
                            bubbled = (total, j)
                        if total < min:
                            min = total

                    # if max - min < 7:
                    #     blank = True

                    if self.th is not None:
                        if bubbled[0] <= self.th:
                            blank = True



                    color = (0, 0, 255)  # red
                    k = ANSWER_KEY[total_count]
                    temp = [ self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                             self.bubble_map[str(bubbled[1])] ]

                    total_count += 1
                    if blank == True:
                        temp.append("B")
                    elif k == bubbled[1]:
                        color = (0, 255, 0)  # green
                        correct += 1
                        temp.append("C")
                        cv2.drawContours(sec, [cnts[k]], -1, color, 1)
                    else:
                        temp.append("W")
                        cv2.drawContours(sec, [cnts[k]], -1, color, 1)
                    #

                    student_answers.append(temp)

        self.student_answers = student_answers
        self.correct = correct
        self.total_count = total_count
        self.total_count1 = total_count
        #print("Score/Total:", correct, "/", total_count)


    def grade_section_4(self):

        im = self.im

        sections = []
        student_answers = []

        height = 179
        width = 50

        x_steps = [(0, 0), (75, 75), (76, 74), (73, 74), (74, 75), (74, 74)]
        init_steps = [(130, 290)]

        x1 = init_steps[0][0]
        x2 = x1 + width

        y1 = init_steps[0][1]
        y2 = y1 + height
        end = 6

        new_x1 = None

        #cv2.imshow("1", sect )


        for x in range(0, 6):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            if x > 1:
                height = 150
                y1 = 317
                y2 = y1 + height
            if x == 2:
                new_x1 = x1
            sect = im[y1:y2, x1:x2]
            sections.append(sect)
            # cv2.imshow(str(x), sect)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()



        x1 = new_x1
        x2 = x1 + width

        y1 = 503
        height = 150
        y2 = y1 + height


        x_steps = [(0, 0), (73, 70), (0, 0), (73, 74), (74, 75), (74, 74)]

        for x in range(2, 6):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            sect = im[y1:y2, x1:x2]
            sections.append(sect)
            # cv2.imshow(str(x + 10), sect)

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        
        ANSWER_KEY = self.ANSWER_KEY

        count = 0
        correct = 0
        total_count = 0
        num1 = 0
        check = True
        ben10 = 0

        for sec in sections:
            count += 1
            imgray = cv2.cvtColor(sec, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            im2, cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            docCnt = None

            if len(cnts) > 0:
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                for c in cnts:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    if len(approx) == 4:
                        docCnt = approx
                        # cv2.drawContours(im, [docCnt], -1, (0, 255, 0), 2)
                        break

            warped = four_point_transform(imgray, docCnt.reshape(4, 2))

            thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

            questionCnts = []
            ori = []
            ben = []

            for c in cnts:
                # compute the bounding box of the contour, then use the
                # bounding box to derive the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                ben.append( [w, h, ar] )
                # print("w,h,ar: ", w, h, ar)
                # in order to label the contour as a question, region
                # should be sufficiently wide, sufficiently tall, and
                # have an aspect ratio approximately equal to 1
                if w >= 2 and h >= 2 and ar >= 0.8 and ar <= 1.4:
                    questionCnts.append(c)
                    ori.append(c)
            # print("b: ", len(cnts))
            if len(cnts) == 0:
                print(ben10)
            ben10 += 1
            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
            ori = contours.sort_contours(ori)[0]


            #print("Q: ", len(questionCnts))

            inc = 4
            start = 0
            num = 0
            end = 10



            if count > 2:
                #print("size: ", len(ANSWER_KEY))
                total_count += 1
                q = total_count
                pos = []
                user_answer = []
                while num < 4:

                    cnts = contours.sort_contours(ori[start:end], method="top-to-bottom")[0]

                    bubbled = None
                    if len(cnts) > 11 and check == True:
                        cnt_copy = []
                        for x in range(0, 12):
                            cnt_copy.append(cnts[x])
                        cnts = contours.sort_contours(cnt_copy,  method="top-to-bottom")[0]
                        check = False

                    #print("count: ", len(cnts))
                    blank = False
                    min = None
                    max = None

                    for (j, c) in enumerate(cnts):

                        mask = np.zeros(thresh.shape, dtype="uint8")
                        cv2.drawContours(mask, [c], -1, 255, -1)
                        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                        total = cv2.countNonZero(mask)

                        if bubbled is None:
                            max = total
                            min = total
                            bubbled = (total, j)
                        if total >= (bubbled[0]):
                            max = total
                            bubbled = (total, j)
                        if min > total and num > 1:
                            min = total

                    # print("diff: ", max-min)
                    # if (max - min) < 7 and (max - min) != 0:
                    #     blank = True

                    if self.th is not None:
                        if bubbled[0] <= self.th:
                            blank = True

                    if blank == False:
                        user_answer.append(str(bubbled[1]))
                        pos.append(cnts[bubbled[1]])
                    else:
                        user_answer.append("B")

                    num += 1
                    if num == 3:
                        start = end
                        end += 11
                    else:
                        start = end
                        end += 12


                k = ANSWER_KEY[q-1]

                answer = ""
                for x in range(0, len(user_answer)):

                    answer += self.number_map[user_answer[x]][x]


                color = (0, 0, 255)  # red
                # print("user answer: ", answer)
                # print("real_answer: ", k)

                temp = [self.ANSWER_DESC[q - 1][0], self.ANSWER_DESC[q - 1][1], self.ANSWER_DESC[q - 1][2], answer]

                k = k.split(",")

                answer_res = False
                for x in k:
                    if x in answer:
                        correct += 1
                        color = (0, 255, 0)  # green
                        answer_res = True
                        break

                if answer_res == True:
                    temp.append("C")
                else:
                    temp.append("W")

                for item in pos:
                    cv2.drawContours(sec, item, -1, color, 1)
                student_answers.append(temp)


            else:

                for (q, i) in enumerate(np.arange(start, len(questionCnts), inc)):
                    cnts = contours.sort_contours(questionCnts[i:i + inc])[0]
                    bubbled = None
                    max = None
                    min = None
                    blank = False

                    for (j, c) in enumerate(cnts):

                        mask = np.zeros(thresh.shape, dtype="uint8")
                        cv2.drawContours(mask, [c], -1, 255, -1)
                        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                        total = cv2.countNonZero(mask)

                        if bubbled is None:
                            bubbled = (total, j)
                            max = total
                            min = total
                        if total > max:
                            max = total
                            bubbled = (total, j)
                        if total < min:
                            min = total

                    #print( num1 , ": " ,max - min)


                    color = (0, 0, 255)  # red

                    k = ANSWER_KEY[num1]
                    num1 += 1
                    temp = [self.ANSWER_DESC[num1][0], self.ANSWER_DESC[num1][1], self.ANSWER_DESC[num1][2],
                            self.bubble_map[str(bubbled[1])]]

                    if self.th is not None:
                        if bubbled[0] <= self.th:
                            blank = True

                    total_count += 1
                    if blank == True:
                        temp.append("B")
                    elif k == bubbled[1]:
                        color = (0, 255, 0)  # green
                        correct += 1
                        temp.append("C")
                        cv2.drawContours(sec, [cnts[k]], -1, color, 1)
                    else:
                        temp.append("W")
                        cv2.drawContours(sec, [cnts[k]], -1, color, 1)
                    #

                    student_answers.append(temp)

        self.student_answers = student_answers
        self.correct = correct
        self.total_count = total_count
        self.total_count2 = total_count
        #print("Score/Total:", correct, "/", total_count)

    def standard_deviation(self, lst ):
        """Calculates the standard deviation for a list of numbers."""
        num_items = len(lst)
        mean = sum(lst) / num_items
        differences = [x - mean for x in lst]
        sq_differences = [d ** 2 for d in differences]
        ssd = sum(sq_differences)

        # Note: it would be better to return a value and then print it outside
        # the function, but this is just a quick way to print out the values along
        # the way.


        variance = ssd / (num_items - 1)
        sd = sqrt(variance)
        return sd