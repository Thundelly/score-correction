from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import os
from skimage import exposure


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
# ratio = image.shape[0] / 300.0
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

# cv2.imshow("test", edged)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
screenCnt = None


if len(cnts) > 0:
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
image_resized = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
# cv2.imshow("LEL", image_resized)

pts = screenCnt.reshape(4, 2)
rect = np.zeros((4, 2), dtype="float32")

s = pts.sum(axis=1)
rect[0] = pts[np.argmin(s)]
rect[2] = pts[np.argmax(s)]

diff = np.diff(pts, axis=1)
rect[1] = pts[np.argmin(diff)]
rect[3] = pts[np.argmax(diff)]

# rect *= ratio

(tl, tr, br, bl) = rect
widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

maxWidth = max(int(widthA), int(widthB))
maxHeight = max(int(heightA), int(heightB))

dst = np.array([
	[0, 0],
	[maxWidth - 1, 0],
	[maxWidth - 1, maxHeight - 1],
	[0, maxHeight - 1]], dtype = "float32")

M = cv2.getPerspectiveTransform(rect, dst)
warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
warp = exposure.rescale_intensity(warp, out_range=(0, 255))
warp_resized = cv2.resize(warp, (0, 0), fx=0.4, fy=0.4)

# (h, w) = warp.shape
# (dX, dY) = (int(w * 0.4), int(h * 0.45))
# crop = warp[10:dY, w - dX:w - 10]

section_1_1_10 = warp[742:1077, 250:410]
section_1_11_20 = warp[742:1077, 450:610]
section_1_21_30 = warp[742:1077, 650:810]
section_1_31_40 = warp[742:1077 , 850:1010]

# section_1_1_10 = cv2.resize(section_1_1_10, (0, 0), fx=2, fy=2)

# cv2.imshow("1", section_1_1_10)
# cv2.imshow("2", section_1_11_20)
# cv2.imshow("3", section_1_21_30)
# cv2.imshow("4", section_1_31_40)
# cv2.imshow("LOL", warp_resized)

section_1_1_10_Binary = cv2.threshold(section_1_1_10, 0, 225,
                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# cv2.imshow("1.1", section_1_1_10_Binary)

cnts_1 = cv2.findContours(section_1_1_10_Binary,
                          cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts_1 = cnts_1[0] if imutils.is_cv2() else cnts_1[1]
questionCnts_1 = []

for c in cnts_1:
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)

    if w >= 20 and h >= 20 and ar >= 0.8 and ar <= 1.2:
        questionCnts_1.append(c)

print(w, h, ar, questionCnts_1)
cv2.drawContours(section_1_1_10, questionCnts_1, -1, (0, 0, 255), 2)
cv2.imshow("1.1.1", section_1_1_10)

cv2.waitKey(0)
