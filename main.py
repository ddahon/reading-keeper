import time
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For video stream :
cap = cv2.VideoCapture(0)
# 1080p
cap.set(3, 1920)
cap.set(4, 1080)

prevTime = 0
with mp_hands.Hands(
    min_detection_confidence=0.5, # Detection Sensitivity
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame")
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # To improve performance, mark image as not writeable to pass by reference
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
             for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime
        flippedImage = cv2.flip(image, 1)
        cv2.putText(flippedImage, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
        cv2.imshow('MediaPipe Hands', flippedImage)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()