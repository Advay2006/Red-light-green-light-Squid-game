import mediapipe as mp
import cv2
import random
import time
from playsound import playsound

y = 0
x = 0
h = 320
w = 480
cposl = 0
cposr = 0
startT = 0
endT = 0
winner = 0
lsum = 0
rsum = 0
dur = 0
endx, endy = 30, 425
startxl, startxr = 30, 30
startx, starty = 30, 400
cStart, cEnd = 0, 0
initial_zl, initial_zr = None, None
final_pos = 55
isInit = False
isCinit = False
inFramecheck = False


def detect(frm, pose, drawing):
    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
    res = pose.process(rgb)
    frm = cv2.blur(frm, (5, 5))
    drawing.draw_landmarks(frm, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return frm, res


def isVisible(landmarkList):
    if (landmarkList[28].visibility > 0.7) and (landmarkList[24].visibility > 0.7):
        return True
    return False


def calc_sum(landmarkList):
    tsum = 0
    for i in range(11, 33):
        tsum += (landmarkList[i].x * 480)

    return tsum


cap = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
drawing = mp.solutions.drawing_utils
mp_pose1 = mp.solutions.pose
pose1 = mp_pose1.Pose()
drawing1 = mp.solutions.drawing_utils

im1 = cv2.imread('im1.png')
im2 = cv2.imread('im2.png')

while cap.isOpened():
    ret, frame = cap.read()
    crop_right = frame[x:w, y:h]
    crop_left = frame[x:w, h:640]
    crop_left = crop_right

    left, resl = detect(crop_left, pose, drawing)
    right, resr = detect(crop_right, pose1, drawing1)

    if not (inFramecheck):
        try:
            lvis = isVisible(resl.pose_landmarks.landmark)
            rvis = isVisible(resr.pose_landmarks.landmark)
            if not lvis:
                cv2.putText(left, "Please Make sure you", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 255, 0), 4)
                cv2.putText(left, "are fully in frame", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 255, 0), 4)
            if not rvis:
                cv2.putText(right, "Please Make sure you", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 255, 0), 4)
                cv2.putText(right, "are fully in frame", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 255, 0), 4)
            if lvis and rvis:
                inFramecheck = True
                print("OK GO")
        except:
            pass

    else:
        if not (isInit):
            dur = random.randint(3, 6)
            startT = time.time()
            endT = startT
            playsound('greenLight.mp3')
            isInit = True
        if resl.pose_landmarks and resr.pose_landmarks is not None:
            if (endT - startT) <= dur:

                nposl = abs(int(resl.pose_landmarks.landmark[28].y * 200))
                print('original:', nposl)
                nposr = abs(int(resr.pose_landmarks.landmark[28].y * 200))
                if initial_zl is None:
                    initial_zr = nposr
                    initial_zl = nposl
                    print('initial:', initial_zl)
                    continue
                else:
                    nposl = abs(nposl - initial_zl)
                    print('subtracted:', nposl)
                    nposr = abs(nposr - initial_zr)
                if nposl > cposl:
                    cposl = nposl
                    if cposl >= final_pos:
                        startxl = 280
                        print("LEFT WON!")
                        winner = 1
                        break
                    startxl = 30 + int(cposl/final_pos*250)
                    #print(cposl)

                if nposr > cposr:
                    cposr = nposr
                    if cposr >= final_pos:
                        startxl = 280
                        print("RIGHT WON!")
                        winner = 2
                        break
                    startxr = 30 + int(cposr / final_pos * 250)

                endT = time.time()
            else:
                if not isCinit and resl.pose_landmarks is not None and resr.pose_landmarks is not None:
                    isCinit = True
                    cStart = time.time()
                    cEnd = cStart
                    playsound('redLight.mp3')
                    lsum = calc_sum(resl.pose_landmarks.landmark)
                    rsum = calc_sum(resr.pose_landmarks.landmark)

                if (cEnd - cStart) <= 3:
                    lsumt = calc_sum(resl.pose_landmarks.landmark)
                    rsumt = calc_sum(resr.pose_landmarks.landmark)
                    cEnd = time.time()
                    if abs(lsumt - lsum) > 300:
                        print("DEAD! Right WON!")
                        break
                    if abs(rsumt - rsum) > 300:
                        print("DEAD! Left WON!")
                        break
                else:
                    isInit = False
                    isCinit = False

    left = cv2.rectangle(left, (startxl, starty), (endx, endy), (68, 36, 132), -1)  # PINK COLOR PROGRESS
    left = cv2.rectangle(left, (startx, starty), (280, endy), (0, 0, 0), 5)  # BLACK COLOR OUTLINE
    right = cv2.rectangle(right, (startxr, starty), (endx, endy), (68, 36, 132), -1)  # PINK COLOR PROGRESS
    right = cv2.rectangle(right, (startx, starty), (280, endy), (0, 0, 0), 5)  # BLACK COLOR OUTLINE
    cv2.imshow('left', left)
    cv2.imshow('right', right)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break