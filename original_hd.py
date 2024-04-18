# https://www.youtube.com/watch?v=QekxFU0YDqM&list=PLLjn4BxzcNKtUwWeHsGyAkhfRHU32trL5
# Thanks to Rocket Data Science YouTube channel for this easy solution

import cv2
import pyautogui
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=.5, min_tracking_confidence=.5)

mp_drawing = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]


            is_hand_closed = (
                index_finger_tip.y > thumb_tip.y and
                middle_finger_tip.y > thumb_tip.y and
                ring_finger_tip.y > thumb_tip.y and
                pinky_tip.y > thumb_tip.y
            )

            two_fingers_close = (
                
            )
            if is_hand_closed:
                print('Hand Closed')
            else:
                print('Hand not closed')
                pyautogui.press('space')
    cv2.imshow('CV', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()