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

class ACT_Grader():
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

        self.key_map = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4,
            "F": 0,
            "G": 1,
            "H": 2,
            "J": 3,
            "K": 4
        }

        self.bubble_map = {
            "0": ["A", "F"],
            "1": ["B", "G"],
            "2": ["C", "H"],
            "3": ["D", "J"],
            "4": ["E", "K"]

        }

        self.group_map = {
            "A": 1,
            "B": 1,
            "C": 1,
            "D": 1,
            "E": 1,
            "F": 2,
            "G": 2,
            "H": 2,
            "J": 2,
            "K": 2,
        }



    def get_date(self):
        now = datetime.datetime.now()
        cur_date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
        return cur_date


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

        for i in range(0, len(answers) ):

            key = self.key_map[answers[i][3]]
            self.ANSWER_KEY.append(key)
            temp = [ answers[i][0], answers[i][1], answers[i][2] ]
            self.ANSWER_DESC.append(temp)

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
        x1 = 120
        x2 = 230
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
        return number_ml.find_numbers(warped, "packet")



    def grade_section_1(self):

        im = self.im


        sections = []

        height = 180
        width = 50
        x_steps = [(0, 0), (73, 71), (72, 74), (72, 72), (70, 74), (74, 74)]
        init_steps = [(126, 314), (118, 448)]

        sec1_end = 350
        sec2_end = 495

        x1 = init_steps[0][0]
        x2 = x1 + width

        y1 = init_steps[0][1]
        y2 = y1 + height
        end = 5

        for x in range(0, end):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            sect = im[y1:y2, x1:x2]
            if x == 4:
                y2 = sec1_end
            # cv2.imshow(str(x), sect)

            sections.append(sect)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


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



            # print("count: ", len(questionCnts) )



            for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
                cnts = contours.sort_contours(  questionCnts[i:i + 4]  )[0]
                # print("count1: ", len(cnts))
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

                k = ANSWER_KEY[total_count]
                total_count += 1

                temp = None

                #if self.group_map[str(bubbled[1])] == 1:
                if bubbled[1]%2 != 0:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                        self.bubble_map[str(bubbled[1])][0]  ]
                else:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                            self.bubble_map[str(bubbled[1])][1]  ]

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

                #cv2.drawContours(sec, [cnts[k]], -1, color, 1)
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
        x_steps = [(0, 0), (72, 71), (71, 74), (72, 73), (71, 72), (72, 72)]
        init_steps = [(133, 314), (127, 530)]

        sec1_end = 330
        sec2_end = 495

        x1 = init_steps[1][0]
        x2 = x1 + width

        y1 = init_steps[1][1]
        y2 = y1 + height
        end = 6

        for x in range(0, end):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            sect = im[y1:y2, x1:x2]
            sections.append(sect)
            #cv2.imshow(str(x), sect)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


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
                #if w >= 2 and h >= 2 and ar >= 0.3 and ar <= 1.5:
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

                k = ANSWER_KEY[total_count]
                total_count += 1
                color = None
                temp = None

                if bubbled[1]%2 != 0:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                            self.bubble_map[str(bubbled[1])][0]]
                else:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                            self.bubble_map[str(bubbled[1])][1]]

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


        sections = []

        height = 180
        width = 50
        x_steps = [(0, 0), (75, 71), (71, 74), (74, 74), (75, 75), (74, 74)]
        init_steps = [(126, 83), (118, 448)]

        sec1_end = 350
        sec2_end = 495

        x1 = init_steps[0][0]
        x2 = x1 + width

        y1 = init_steps[0][1]
        y2 = y1 + height
        end = 3

        for x in range(0, end):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            sect = im[y1:y2, x1:x2]
            if x == 4:
                y2 = sec1_end
            #cv2.imshow(str(x), sect)

            sections.append(sect)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


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
                if w >= 2 and h >= 2 and ar >= 0.7 and ar <= 1.4:
                    questionCnts.append(c)

            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]




            #print("count: ", len(questionCnts))
            #
            # cv2.drawContours(sec, questionCnts, -1, (0, 0, 255), 1)
            # cv2.imshow("s", im)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()



            for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
                cnts = contours.sort_contours(  questionCnts[i:i + 4]  )[0]
                count += 1
                bubbled = None
                max = None
                min = None
                blank = False
                #print(len(cnts))
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

                k = ANSWER_KEY[total_count]
                total_count += 1

                temp = None

                #if self.group_map[str(bubbled[1])] == 1:
                if bubbled[1]%2 != 0:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                        self.bubble_map[str(bubbled[1])][0]  ]
                else:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                            self.bubble_map[str(bubbled[1])][1]  ]

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
                    #print(k)
                    cv2.drawContours(sec, [cnts[k]], -1, color, 1)

                #cv2.drawContours(sec, [cnts[k]], -1, color, 1)
                student_answers.append(temp)

        self.student_answers = student_answers
        self.correct = correct
        self.total_count = total_count
        #print("Score/Total:", correct, "/", total_count)

    def grade_section_4(self):

        im = self.im


        sections = []

        height = 180
        width = 50
        x_steps = [(0, 0), (74, 71), (70, 74), (74, 74), (75, 75), (74, 74)]
        init_steps = [(126, 83), (126, 292)]

        sec1_end = 350
        sec2_end = 495

        x1 = init_steps[1][0]
        x2 = x1 + width

        y1 = init_steps[1][1]
        y2 = y1 + height
        end = 3

        for x in range(0, end):
            x1 += x_steps[x][0]
            x2 += x_steps[x][1]
            sect = im[y1:y2, x1:x2]
            if x == 4:
                y2 = sec1_end
            #cv2.imshow(str(x), sect)

            sections.append(sect)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


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
                if w >= 2 and h >= 2 and ar >= 0.7 and ar <= 1.4:
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

                # if max - min < 8:
                #     blank = True

                k = ANSWER_KEY[total_count]
                total_count += 1

                temp = None

                #if self.group_map[str(bubbled[1])] == 1:
                if bubbled[1]%2 != 0:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                        self.bubble_map[str(bubbled[1])][0]  ]
                else:
                    temp = [self.ANSWER_DESC[q][0], self.ANSWER_DESC[q][1], self.ANSWER_DESC[q][2],
                            self.bubble_map[str(bubbled[1])][1]  ]

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

                #print(k)
                if color != None:
                    cv2.drawContours(sec, [cnts[k]], -1, color, 1)

                #cv2.drawContours(sec, [cnts[k]], -1, color, 1)
                student_answers.append(temp)

        self.student_answers = student_answers
        self.correct = correct
        self.total_count = total_count
        #print("Score/Total:", correct, "/", total_count)




