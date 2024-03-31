import cv2
import mediapipe as mp
import os

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe drawing utilities
mp_drawing = mp.solutions.drawing_utils

# Create a directory to store the recorded gestures
output_dir = "recorded_gestures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to record hand gestures for each alphabet letter
def record_gestures():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    for letter in alphabet:
        letter_dir = os.path.join(output_dir, letter)
        if not os.path.exists(letter_dir):
            os.makedirs(letter_dir)
        
        print(f"Recording gestures for letter '{letter}'...")
        print("Press 'q' to finish recording.")
        
        # Initialize OpenCV VideoCapture
        cap = cv2.VideoCapture(0)
        
        # Initialize variables to store landmarks
        landmarks_list = []
        count = 0
        
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
                    # Get landmark coordinates and append to the list
                    landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                    landmarks_list.append(landmarks)

                    # Draw hand landmarks on the frame
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Increment count
                    count += 1

            # Display the resulting frame
            cv2.imshow('Record Gestures', frame)

            # Check for 'q' key press to finish recording
            key = cv2.waitKey(1)
            if key == ord('q'):
                # Save the landmarks to a text file
                with open(os.path.join(letter_dir, f"{letter}.txt"), "w") as f:
                    for landmarks in landmarks_list:
                        for landmark in landmarks:
                            f.write(','.join(map(str, landmark)) + '\n')
                        f.write('\n')
                
                print(f"Gestures for letter '{letter}' saved.")
                break
        
        # Release resources
        cap.release()
        cv2.destroyAllWindows()

# Record gestures for each alphabet letter
record_gestures()
