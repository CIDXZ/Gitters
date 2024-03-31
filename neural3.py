import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import random
import time

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe drawing utilities
mp_drawing = mp.solutions.drawing_utils

# Function to record gestures
def record_gestures():
    gestures = {'rock': [], 'paper': [], 'scissors': []}
    # Initialize OpenCV VideoCapture
    cap = cv2.VideoCapture(0)

    while True:
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
                # Get landmark coordinates
                landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]

                # Extract specific landmarks for fingertips and fingers base
                thumb_tip = landmarks[4]  # Thumb tip landmark
                index_tip = landmarks[8]  # Index finger tip landmark
                middle_tip = landmarks[12]  # Middle finger tip landmark

                index_base = landmarks[5]  # Index finger base landmark
                middle_base = landmarks[9]  # Middle finger base landmark

                # Calculate distances between thumb tip and index/middle finger tips
                dist_thumb_index = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5
                dist_thumb_middle = ((thumb_tip[0] - middle_tip[0]) ** 2 + (thumb_tip[1] - middle_tip[1]) ** 2) ** 0.5

                # Calculate distances between index and middle finger bases
                dist_index_middle = ((index_base[0] - middle_base[0]) ** 2 + (index_base[1] - middle_base[1]) ** 2) ** 0.5

                # Define thresholds for gesture classification
                threshold_thumb_index = 0.05  # Threshold for thumb tip distance from index finger tip
                threshold_thumb_middle = 0.05  # Threshold for thumb tip distance from middle finger tip
                threshold_index_middle = 0.05  # Threshold for distance between index and middle finger bases

                # Classify hand gesture based on distances and thresholds
                if dist_thumb_index < threshold_thumb_index and dist_thumb_middle < threshold_thumb_middle:
                    gesture = 'rock'
                elif dist_index_middle < threshold_index_middle:
                    gesture = 'scissors'
                else:
                    gesture = 'paper'

                key_pressed = cv2.waitKey(1) & 0xFF
                if key_pressed == ord('q'):
                    break

                if key_pressed == ord('w'):
                    gestures['rock'].append(hand_landmarks)
                    print("Rock sign saved!")
                elif key_pressed == ord('e'):
                    gestures['paper'].append(hand_landmarks)
                    print("Paper sign saved!")
                elif key_pressed == ord('r'):
                    gestures['scissors'].append(hand_landmarks)
                    print("Scissors sign saved!")

        # Display the resulting frame
        cv2.imshow('Record Gestures', frame)

        if all(len(gestures[gesture]) > 0 for gesture in gestures):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    return gestures

# Function to play the game
def play_game(recorded_gestures):
    # Initialize OpenCV VideoCapture
    cap = cv2.VideoCapture(0)

    # Create a Tkinter root window
    root = tk.Tk()
    root.title("Computer Gesture")

    # Create a Canvas widget for displaying the computer's gesture
    computer_gesture_canvas = tk.Canvas(root, width=300, height=300)
    computer_gesture_canvas.pack()

    # Function to update computer gesture image
    def update_computer_gesture():
        # Get the computer's gesture (randomly selected for now)
        computer_gesture = np.random.choice(['rock', 'paper', 'scissors'])

        # Load the computer's gesture image
        computer_gesture_image_path = f"{computer_gesture}.jpg"  # Assuming you have images named 'rock.jpg', 'paper.jpg', and 'scissors.jpg'
        computer_gesture_image = Image.open(computer_gesture_image_path)
        computer_gesture_image = computer_gesture_image.resize((300, 300), Image.ANTIALIAS)
        computer_gesture_image = ImageTk.PhotoImage(computer_gesture_image)

        # Clear the canvas
        computer_gesture_canvas.delete("all")

        # Display the computer's gesture image in the computer gesture window
        computer_gesture_canvas.create_image(0, 0, anchor=tk.NW, image=computer_gesture_image)

        # Schedule the next update after 10 seconds
        root.after(10000, update_computer_gesture)

    # Start updating computer gesture image
    update_computer_gesture()

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
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the resulting frame
        cv2.imshow('Rock Paper Scissors Game', frame)

        # Check for a press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    root.mainloop()

# Record gestures
recorded_gestures = record_gestures()
print("Recorded gestures:", recorded_gestures)

# Play the game
play_game(recorded_gestures)
