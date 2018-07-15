import cv2
import numpy as np

class Number_ML():
    def __init__(self):
        self.image = None

    def find_numbers(self, image, type):
        #######   training part    ###############
        samples = np.loadtxt('training_data/generalsamples.data',np.float32)
        responses = np.loadtxt('training_data/generalresponses.data',np.float32)
        responses = responses.reshape((responses.size,1))

        model = cv2.ml.KNearest_create()
        model.train(samples,cv2.ml.ROW_SAMPLE,responses)

        ############################# testing part  #########################

        im = image
        out = np.zeros(im.shape,np.uint8)
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

        im2, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        number_map = {}

        thresh_hold = None
        if type == "packet":
            thresh_hold = 30
        else:
            thresh_hold = 25

        for cnt in contours:
            if cv2.contourArea(cnt)>50:
                [x,y,w,h] = cv2.boundingRect(cnt)

                if h>thresh_hold:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    #retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
                    retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)

                    string = str(int((results[0][0])) )

                    number_map[int(x)] = string

                    #cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

        keys = []
        for key in number_map.keys():
            keys.append(key)
        keys.sort()
        result = ""
        for key in keys:
            result += number_map[key]
        return result

