import cv2
import mediapipe as mp
import numpy as np
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

                # Draw hand landmarks and gesture label on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Record Gestures', frame)

        if all(len(gestures[gesture]) > 0 for gesture in gestures):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    return gestures

# Function to classify gesture during the game
def classify_gesture(hand_landmarks, recorded_gestures):
    min_distance = float('inf')
    classified_gesture = None

    for gesture, samples in recorded_gestures.items():
        for sample in samples:
            # Calculate the distance between each landmark of the sample and the current hand landmarks
            distance = sum(np.linalg.norm(np.subtract([lm.x, lm.y, lm.z], [sample.landmark[i].x, sample.landmark[i].y, sample.landmark[i].z])) for i, lm in enumerate(hand_landmarks.landmark))
            # Update the minimum distance and classified gesture if this sample is closer
            if distance < min_distance:
                min_distance = distance
                classified_gesture = gesture

    return classified_gesture

# Function to play the game
def play_game(recorded_gestures):
    # Initialize OpenCV VideoCapture
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
                # Classify the gesture
                gesture = classify_gesture(hand_landmarks, recorded_gestures)

                # Draw hand landmarks and gesture label on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f"Your Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Display the updated frame
                cv2.imshow('Rock Paper Scissors Game', frame)

        # Check for a press
        
        if cv2.waitKey(1) == ord('a'):
            # Get the computer's gesture (randomly selected for now)
            computer_gesture = np.random.choice(['rock', 'paper', 'scissors'])

            # Determine the winner
            if gesture == computer_gesture:
                result = "It's a tie!"
            elif (gesture == 'rock' and computer_gesture == 'scissors') or \
                 (gesture == 'paper' and computer_gesture == 'rock') or \
                 (gesture == 'scissors' and computer_gesture == 'paper'):
                result = "You win!"
            else:
                result = "Computer wins!"

            # Draw the computer's gesture and result on the frame
            cv2.putText(frame, f"Computer's Gesture: {computer_gesture}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Result: {result}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            print("Your Gesture:",gesture)
            print("Computer's Gesture:",computer_gesture)
            print("Result:",result)
            

            # Display the updated frame
            cv2.imshow('Rock Paper Scissors Game', frame)
            

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Record gestures
recorded_gestures = record_gestures()
print("Recorded gestures:", recorded_gestures)

# Play the game
play_game(recorded_gestures)