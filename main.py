import copy
import itertools
import time

import cv2 as cv
import mediapipe as mp
import os
from utils.utils import *
from google.cloud import storage
from firebase import firebase
from model import KeyPointClassifier


labels = ["Normal", "Capture"]

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
keypoint_classifier = KeyPointClassifier()

# For video stream :
cap = cv.VideoCapture(0)

# For FPS computation
prevTime = 0

# To avoid unwanted captures
time_between_captures = 1

nbImagesCaptured = 0
previousSign = 0
lastCapture = 0

# Firebase storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="rake-3517c-firebase-adminsdk-uw5u6-98882a59de.json"
firebase = firebase.FirebaseApplication('https://rake-3517c-default-rtdb.firebaseio.com/')
client = storage.Client()
bucket = client.get_bucket('rake-3517c.appspot.com')

# Main loop
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5, # Detection Sensitivity
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        image = cv.flip(image, 1)
        if not success:
            print("Ignoring empty camera frame")
            continue

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        # To improve performance, mark image as not writeable to pass by reference
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                brect = calc_bounding_rect(image, hand_landmarks)
                landmark_list = calc_landmark_list(image, hand_landmarks)

                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)
		
		# Classify gesture
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                # Capture image
                if hand_sign_id == 1 and previousSign != 1 and time.time() - lastCapture >= time_between_captures:
		    # Flip image vertically and horizontally before saving
                    cv.imwrite("images/{}.png".format(nbImagesCaptured), cv.flip(image, 0))
                    
		    # Send to firebase
                    imageBlob = bucket.blob("/")
                    imagePath = "images/{}.png".format(nbImagesCaptured)
                    imageBlob = bucket.blob("{}.png".format(nbImagesCaptured))
                    imageBlob.upload_from_filename(imagePath)
                    nbImagesCaptured += 1
                    lastCapture = time.time()
                    print("Capture")

                image = draw_bounding_rect(True, image, brect)
                image = draw_landmarks(image, landmark_list)
                image = draw_info_text(
                    image,
                    brect,
                    handedness,
                    labels[hand_sign_id],
                    ""
                )
                previousSign = hand_sign_id
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime
        cv.putText(image, f'FPS: {int(fps)}', (20, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
        cv.imshow('Rake', image)
        if cv.waitKey(5) & 0xFF == 27:
            break
cap.release()
