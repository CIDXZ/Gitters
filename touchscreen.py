import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe drawing utilities
mp_drawing = mp.solutions.drawing_utils

# Function to perform mouse actions based on hand gestures
def perform_mouse_actions(hand_landmarks, screen_width, screen_height):
    # Get coordinates of index finger tip
    index_finger_tip = hand_landmarks.landmark[8]
    index_finger_x = int(index_finger_tip.x * screen_width)
    index_finger_y = int(index_finger_tip.y * screen_height)

    # Move the mouse cursor to the index finger tip position
    pyautogui.moveTo(index_finger_x, index_finger_y, duration=0.1)

    # Check for gesture to perform actions
    # For example, you can check if the index finger is close to the thumb to simulate a click

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from webcam.")
        break

    # Convert the image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands model
    results = hands.process(frame_rgb)

    # Inside the loop where hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the width and height of the frame
            h, w, _ = frame.shape

            # Perform mouse actions based on hand gestures
            perform_mouse_actions(hand_landmarks, w, h)

            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the resulting frame
    cv2.imshow('Hand Gesture Control', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
