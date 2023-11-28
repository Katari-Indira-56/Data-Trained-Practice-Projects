import mediapipe as mp
# Customization of live and streaming data
import cv2
# To process the images through webcam
import numpy as np
from mediapipe.framework.formats import landmark_pb2
# landmark_pb2 is a class used to find finger tips ,indexes
import time
from math import sqrt
import win32api
# to control cursor movements
import pyautogui
# to utilise the functions of mouse
from win32con import MOUSEEVENTF_WHEEL

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# class to find all 21 points in the single hand
click = 0

video = cv2.VideoCapture(0)
# starting the webcam

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = cv2.flip(image, 1)

        imageHeight, imageWidth, _ = image.shape
        # Setting size of the popup window used for mouse

        results = hands.process(image)


        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Processing the raw image through source of webcam

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )
# Simply connecting all the finger with thei geometric points using mp_drawing class
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:

                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                           normalizedLandmark.y,
                                                                                           imageWidth, imageHeight)

                    point = str(point)

                    if point == 'HandLandmark.INDEX_FINGER_TIP':
                        try:
                            indexfingertip_x = pixelCoordinatesLandmark[0]
                            indexfingertip_y = pixelCoordinatesLandmark[1]
                            win32api.SetCursorPos((indexfingertip_x * 4, indexfingertip_y * 5))
                            # Detecting the finger tips and finger movements

                        except:
                            pass

                    elif point == 'HandLandmark.THUMB_TIP':
                        try:
                            thumbfingertip_x = pixelCoordinatesLandmark[0]
                            thumbfingertip_y = pixelCoordinatesLandmark[1]
                            # print("thumb",thumbfingertip_x)
                            # win32api.SetCursorPos((thumbfingertip_x * 4, thumbfingertip_y * 5))

                        except:
                            pass
                    elif point == 'HandLandmark.MIDDLE_FINGER_TIP':
                        try:
                            middlefingertip_x = pixelCoordinatesLandmark[0]
                            middlefingertip_y = pixelCoordinatesLandmark[1]
                            # win32api.SetCursorPos((middlefingertip_x * 4, middlefingertip_y * 5))
                        except:
                            pass
                    elif point=='HandLandmark.SMALL_FINGER_TIP':
                        try :
                            x=pixelCoordinatesLandmark[0]
                            y=pixelCoordinatesLandmark[1]
                            # win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, 1, 0)

                        except:
                            pass




                    try:
                        # pyautogui.moveTo(indexfingertip_x,indexfingertip_y)
                        Distance_x = sqrt(
                            (indexfingertip_x - thumbfingertip_x) ** 2 + (indexfingertip_x - thumbfingertip_x) ** 2)
                        Distance_y = sqrt(
                            (indexfingertip_y - thumbfingertip_y) ** 2 + (indexfingertip_y - thumbfingertip_y) ** 2)
                        if Distance_x < 25 or Distance_x < -25 :
                            if Distance_y < 25 or Distance_y < -25 :
                                click = click + 1
                                if click % 25 == 0:
                                    print("Clicked")
                                    # Click event is initiate
                                    pyautogui.click()
                                    # Click event is completed

                    except:

                       pass
                    try:
                        # pyautogui.moveTo(indexfingertip_x,indexfingertip_y)
                        Distance_x = sqrt(
                            (middlefingertip_x - thumbfingertip_x) ** 2 + (middlefingertip_x - thumbfingertip_x) ** 2)
                        Distance_y = sqrt(
                            (middlefingertip_y - thumbfingertip_y) ** 2 + (middlefingertip_y - thumbfingertip_y) ** 2)
                        if Distance_x < 50 or Distance_x < -50:
                            if Distance_y < 50 or Distance_y < -50 :
                                click = click + 1
                                if click % 25 == 0:
                                    print("Right Clicked")
                                    # Click event is initiate
                                    pyautogui.rightClick()
                                    # Click event is completed

                    except :
                        pass
                    try:

                        Distance_x = sqrt(
                            (middlefingertip_x - indexfingertip_x) ** 2 + (middlefingertip_x - indexfingertip_x) ** 2)
                        Distance_y = sqrt(
                            (middlefingertip_y - indexfingertip_y) ** 2 + (middlefingertip_y - indexfingertip_y) ** 2)
                        if Distance_x == Distance_y:
                            pyautogui.scroll(50)
                    except :
                        pass
        cv2.imshow('Virtual mouse', image)

        if cv2.waitKey(10) & 0xFF == ord(' '):
            break

video.release()
