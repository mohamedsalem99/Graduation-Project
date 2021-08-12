import os
import threading
from threading import Lock
from math import hypot
from imutils import face_utils
from utils import *
import numpy as np
import pyautogui as pag
import imutils
import dlib
import cv2
from scipy.spatial import distance as dist
from imutils.video import VideoStream
import playsound
import argparse
import time
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2

# Thresholds and consecutive frame length for triggering the mouse action.
MOUTH_AR_THRESH = 0.6
#######
MOUTH_AR_CONSECUTIVE_FRAMES = 15
#########
EYE_AR_THRESH = 0.25
EYE_AR_CONSECUTIVE_FRAMES = 6
BROW_AR_CONSECUTIVE_FRAMES = 14.5
WINK_AR_DIFF_THRESH = 0.03
WINK_AR_CLOSE_THRESH = 0.1
WINK_CONSECUTIVE_FRAMES = 1
EYE_AR_CONSEC_FRAMES = 48
# Initialize the frame counters for each action as well as
# booleans used to indicate if action is performed or not
MOUTH_COUNTER = 0
EYE_COUNTER = 0
WINK_COUNTER = 0
COUNTER = 0
INPUT_MODE = False
EYE_CLICK = False
LEFT_WINK = False
RIGHT_WINK = False
SCROLL_MODE = False
ALARM_ON = False
ANCHOR_POINT = (0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)

# Initialize Dlib's face detector (HOG-based) and then create
# the facial landmark predictor
shape_predictor = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

# Grab the indexes of the facial landmarks for the left and
# right eye, nose and mouth respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
(reStart, reEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
(leStart, leEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]

# Video capture
vid = cv2.VideoCapture(0)
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--alarm", type=str, default="",
                help="TF010.WAV")
args = vars(ap.parse_args())

resolution_w = 1366
resolution_h = 768
cam_w = 640
cam_h = 480
unit_w = resolution_w / cam_w
unit_h = resolution_h / cam_h


def sound_alarm(path):
    # play an alarm sound
    playsound.playsound(path)


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear


def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def Mouth_action(eye_points, facial_landmarks):
    right_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    l_point = (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y)
    lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return lenght;


def eyebrow(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return lenght;


def face_line(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return lenght;


def brow_scroll(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return lenght;


def smile_V(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return lenght;


def smile_H(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return lenght;


def brow(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return lenght;


x1 = int(input(" Enter which click left  =  "))
x2 = int(input(" Enter which click right =  "))
x3 = int(input(" Enter which scroll mode =  "))
x4 = input(" do you want active alarm    =  ")


def choose_left_click(argument):
    switcher = {
        1: "right_eye",
        2: "left_eye",
        3: "smile",
        4: "brow"

    }
    # Get the function from switcher dictionary
    return switcher.get(argument, "invalid choise")


def choose_right_click(argument):
    switcher = {
        1: "right_eye",
        2: "left_eye",
        3: "smile",
        4: "brow"

    }
    # Get the function from switcher dictionary
    return switcher.get(argument, "invalid choise")


def choose_scroll_active(argument):
    switcher = {
        1: "smile",
        2: "brow",
        3: "blink"

    }
    # Get the function from switcher dictionary
    return switcher.get(argument, "invalid choise")


def choose_alarm_active(argument):
    switcher = {
        "yes": "on",
        "no": "off"
    }
    # Get the function from switcher dictionary
    return switcher.get(argument, "invalid choise")


a1 = choose_left_click(x1)
a2 = choose_right_click(x2)
a3 = choose_scroll_active(x3)
a4 = choose_alarm_active(x4)

print(a1, a2, a3, a4)

frames = 0
time.sleep(1.0)
sence_scroll = 70

while True:
    # ret, img = vid.read()  # ret: whether the image is successfully grabbed or read

    _, frame = vid.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

    frames += 1
    new_frame = np.zeros((500, 500, 3), np.uint8)
    _, frame = vid.read()
    frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=cam_w, height=cam_h)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    oo = 0
    length = 0
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        FACE_LINE = face_line([2, 16], landmarks)
        BROW_SCROLL = brow_scroll([20, 39], landmarks)

        l1 = smile_H([52, 58], landmarks)
        l2 = smile_V([49, 55], landmarks)
        # print(BROW_SCROLL / FACE_LINE)
        # print(l2/l1)
        oo = l2 / l1
        length = BROW_SCROLL / FACE_LINE
    # print(length)

    # Grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Loop over the face detections
    if len(rects) > 0:
        rect = rects[0]
    else:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        continue

    # Determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # Extract the left and right eye coordinates, then use the
    # coordinates to compute the eye aspect ratio for both eyes
    mouth = shape[mStart:mEnd]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    nose = shape[nStart:nEnd]
    right_eyebrow = shape[reStart:reEnd]
    left_eyebrow = shape[leStart:leEnd]

    # Because I flipped the frame, left is right, right is left.
    temp = leftEye
    leftEye = rightEye
    rightEye = temp

    # Average the mouth aspect ratio together for both eyes
    mar = mouth_aspect_ratio(mouth)
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0

    # ALARM انذار

    # check to see if the eye aspect ratio is below the blink
    # threshold, and if so, increment the blink frame counter

    if a4 == "on":
        if ear < EYE_AR_THRESH:
            print(COUNTER)
            COUNTER += 1

            # if the eyes were closed for a sufficient number of
            # then sound the alarm

            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                # if the alarm is not on, turn it on
                if not ALARM_ON:
                    ALARM_ON = True
                    # check to see if an alarm file was supplied,
                    # and if so, start a thread to have the alarm
                    # sound played in the background
                    if args["alarm"] != "":
                        t = Thread(target=sound_alarm, args=(args["alarm"],))
                        t.deamon = True
                        t.start()
                # draw an alarm on the frame
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                sound_alarm("TF010.WAV")
        # otherwise, the eye aspect ratio is not below the blink
        # threshold, so reset the counter and alarm
        else:
            COUNTER = 0
            ALARM_ON = False

    diff_ear = np.abs(leftEAR - rightEAR)
    nose_point = (nose[3, 0], nose[3, 1])

    # Compute the convex hull for the left and right eye, then
    # visualize each of the eyes
    mouthHull = cv2.convexHull(mouth)
    leftEyeHull = cv2.convexHull(leftEye)
    rightEyeHull = cv2.convexHull(rightEye)
    right_eyebrowHull = cv2.convexHull(right_eyebrow)
    left_eyebrowHull = cv2.convexHull(left_eyebrow)

    cv2.drawContours(frame, [right_eyebrowHull], -1, YELLOW_COLOR, 1)
    cv2.drawContours(frame, [left_eyebrowHull], -1, YELLOW_COLOR, 1)
    cv2.drawContours(frame, [mouthHull], -1, YELLOW_COLOR, 1)
    cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
    cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 1)

    for (x, y) in np.concatenate((mouth, leftEye, rightEye), axis=0):
        cv2.circle(frame, (x, y), 2, RED_COLOR, -1)

    # Check to see if the eye aspect ratio is below the blink
    # threshold, and if so, increment the blink frame counter
    ################################### Left Click

    # if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
    # SCROLL_MODE = not SCROLL_MODE
    # INPUT_MODE = not INPUT_MODE
    # EYE_COUNTER = 0

    # nose point to draw a bounding box around it

    # else:
    # EYE_COUNTER = 0
    # WINK_COUNTER = 0

    # if MOUTH_AR_THRESH < 0.26:
    # cv2.putText(frame, "Alert!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)

    if mar > MOUTH_AR_THRESH:
        MOUTH_COUNTER += 1
        if MOUTH_COUNTER >= MOUTH_AR_CONSECUTIVE_FRAMES:
            # if the alarm is not on, turn it on
            INPUT_MODE = not INPUT_MODE
            # SCROLL_MODE = not SCROLL_MODE
            MOUTH_COUNTER = 0
            ANCHOR_POINT = nose_point
    else:
        MOUTH_COUNTER = 0

    if INPUT_MODE:
        cv2.putText(frame, "READING INPUT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
        x, y = ANCHOR_POINT
        nx, ny = nose_point
        w, h = 30, 30
        w1, h1 = 30, 30
        R = 30
        multiple = 1
        xx = nx - x
        yy = ny - y
        a = yy / xx
        cv2.circle(frame, (x, y), R, GREEN_COLOR, 2)
        # nx, ny = pag.position()
        # print(x,y)

        # if nx*nx+ny*ny == R*R:
        # w = nx
        # h = ny

        if a4 == "on":
            if ear < EYE_AR_THRESH:
                print(COUNTER)
                COUNTER += 1

                # if the eyes were closed for a sufficient number of
                # then sound the alarm

                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    # if the alarm is not on, turn it on
                    if not ALARM_ON:
                        ALARM_ON = True
                        # check to see if an alarm file was supplied,
                        # and if so, start a thread to have the alarm
                        # sound played in the background
                        if args["alarm"] != "":
                            t = Thread(target=sound_alarm, args=(args["alarm"],))
                            t.deamon = True
                            t.start()
                    # draw an alarm on the frame
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    sound_alarm("R:/Graduation/Mouse_Cursor_Control_Handsfree-master/TF003.WAV")
            # otherwise, the eye aspect ratio is not below the blink
            # threshold, so reset the counter and alarm
            else:
                COUNTER = 0
                ALARM_ON = False

        diff_ear = np.abs(leftEAR - rightEAR)
        nose_point = (nose[3, 0], nose[3, 1])

        # Compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        mouthHull = cv2.convexHull(mouth)
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        right_eyebrowHull = cv2.convexHull(right_eyebrow)
        left_eyebrowHull = cv2.convexHull(left_eyebrow)

        cv2.drawContours(frame, [right_eyebrowHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(frame, [left_eyebrowHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(frame, [mouthHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 1)

        for (x, y) in np.concatenate((mouth, leftEye, rightEye), axis=0):
            cv2.circle(frame, (x, y), 2, RED_COLOR, -1)

        # Check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        ################################### Left Click

        if diff_ear > WINK_AR_DIFF_THRESH:
            if a1 == "left_eye":
                if leftEAR < rightEAR:
                    if leftEAR < EYE_AR_THRESH:
                        WINK_COUNTER += 1

                        if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                            pag.click(button='left')

                            WINK_COUNTER = 0
            elif a1 == "right_eye":
                if leftEAR > rightEAR:
                    if rightEAR < EYE_AR_THRESH:
                        WINK_COUNTER += 1

                        if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                            pag.click(button='left')

                            WINK_COUNTER = 0
            else:
                WINK_COUNTER = 0

        elif a1 == "smile":
            if oo > 1.7:
                pag.click(button='left')

        elif a1 == "brow":
            if length > 0.25:
                pag.click(button='left')

        ##############################  Right Click
        if diff_ear > WINK_AR_DIFF_THRESH:
            if a2 == "left_eye":
                if leftEAR < rightEAR:
                    if leftEAR < EYE_AR_THRESH:
                        WINK_COUNTER += 1

                        if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                            pag.click(button='right')

                            WINK_COUNTER = 0
            elif a2 == "right_eye":
                if leftEAR > rightEAR:
                    if rightEAR < EYE_AR_THRESH:
                        WINK_COUNTER += 1

                        if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                            pag.click(button='right')

                            WINK_COUNTER = 0
            else:
                WINK_COUNTER = 0
        elif a2 == "smile":
            if oo > 1.7:
                pag.click(button='right')

        elif a2 == "brow":
            if length > 0.25:
                pag.click(button='right')

        #########################################  Active scroll mode
        if a3 == "left_eye":
            if diff_ear < WINK_AR_DIFF_THRESH:
                if ear <= EYE_AR_THRESH:
                    EYE_COUNTER += 1

                    if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
                        SCROLL_MODE = not SCROLL_MODE
                        # INPUT_MODE = not INPUT_MODE
                        EYE_COUNTER = 0

                # nose point to draw a bounding box around it

                else:
                    EYE_COUNTER = 0
                    WINK_COUNTER = 0


        elif a3 == "right_eye":
            if diff_ear < WINK_AR_DIFF_THRESH:
                if ear <= EYE_AR_THRESH:
                    EYE_COUNTER += 1

                    if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
                        SCROLL_MODE = not SCROLL_MODE
                        # INPUT_MODE = not INPUT_MODE
                        EYE_COUNTER = 0

                # nose point to draw a bounding box around it

                else:
                    EYE_COUNTER = 0
                    WINK_COUNTER = 0
        elif a3 == "smile":
            if oo > 1.666:
                EYE_COUNTER += 1
                print(EYE_COUNTER)
                if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:

                    SCROLL_MODE = not SCROLL_MODE
                    # INPUT_MODE = not INPUT_MODE
                    EYE_COUNTER = 0

                # nose point to draw a bounding box around it

                else:
                    # EYE_COUNTER = 0
                    WINK_COUNTER = 0

        elif a3 == "brow":
            if length > 0.25:
                EYE_COUNTER += 1
                print(EYE_COUNTER)
                if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:

                    SCROLL_MODE = not SCROLL_MODE
                    # INPUT_MODE = not INPUT_MODE
                    EYE_COUNTER = 0

                # nose point to draw a bounding box around it

                else:
                    # EYE_COUNTER = 0
                    WINK_COUNTER = 0

        elif a3 == "blink":
            if diff_ear > WINK_AR_DIFF_THRESH:
                if ear <= EYE_AR_THRESH:
                    EYE_COUNTER += 1

                    if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
                        SCROLL_MODE = not SCROLL_MODE
                        # INPUT_MODE = not INPUT_MODE
                        EYE_COUNTER = 0

                # nose point to draw a bounding box around it

                else:
                    # EYE_COUNTER = 0
                    WINK_COUNTER = 0

        # if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
        # SCROLL_MODE = not SCROLL_MODE
        # INPUT_MODE = not INPUT_MODE
        # EYE_COUNTER = 0

        # nose point to draw a bounding box around it

        # else:
        # EYE_COUNTER = 0
        # WINK_COUNTER = 0

        # if MOUTH_AR_THRESH < 0.26:
        # cv2.putText(frame, "Alert!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)

        dir = direction(nose_point, ANCHOR_POINT, w, h)

        # cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
        cv2.line(frame, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)

        # dir = direction(nose_point , ANCHOR_POINT , w , h)
        cv2.putText(frame, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

        # xx, yy = pag.position()

        drag = hypot((x - nx), (y - ny)) - R

        if dir == 'right':
            # if ((nx-x)*(nx-x))+((ny-y)*(ny-y)) == R*R:
            # a = ny/nx
            pag.moveRel(drag, a * drag)

        # pag.moveRel(drag, 0)

        # pag.moveRel(drag, 0)
        # pag.moveTo(xx,yy)
        elif dir == 'left':
            pag.moveRel(-drag, -a * drag)
        # elif nx*nx+ny*ny == R*R:
        # pag.moveRel(drag, drag)
        elif dir == 'up':
            if SCROLL_MODE:
                pag.scroll(sence_scroll)
            else:
                pag.moveRel(0, -drag)
        elif dir == 'down':
            if SCROLL_MODE:
                pag.scroll(-sence_scroll)
            else:
                pag.moveRel(0, drag)

    # x, y = pag.position()
    # print(x, y)
    if SCROLL_MODE:
        cv2.putText(frame, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

    # cv2.putText(frame, "MAR: {:.2f}".format(mar), (500, 30),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
    # cv2.putText(frame, "Right EAR: {:.2f}".format(rightEAR), (460, 80),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
    # cv2.putText(frame, "Left EAR: {:.2f}".format(leftEAR), (460, 130),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
    # cv2.putText(frame, "Diff EAR: {:.2f}".format(np.abs(leftEAR - rightEAR)), (460, 80),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show the frame
    cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # If the `Esc` key was pressed, break from the loop
    if key == 1:
        break
    if key == ord("q"):
        break

# Do a bit of cleanup
cv2.destroyAllWindows()
vid.release()
