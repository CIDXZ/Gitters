import cv2
import numpy as np

# Define the camera capture device
cap = cv2.VideoCapture(0)

# Define the threshold for detecting motion
threshold = 10000

# Initialize the background frame for motion detection
_, bg_frame = cap.read()
bg_frame = cv2.cvtColor(bg_frame, cv2.COLOR_BGR2GRAY)
bg_frame = cv2.GaussianBlur(bg_frame, (21, 21), 0)

# Loop over the frames from the camera
while True:
    # Read a frame from the camera
    _, frame = cap.read()
    
    # Convert the frame to grayscale and blur it
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    
    # Compute the absolute difference between the current frame and the background frame
    frame_diff = cv2.absdiff(bg_frame, gray_frame)
    
    # Threshold the frame difference to identify areas of motion
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop over the contours and check for motion
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > threshold:
            motion_detected = True
            break
    
    # If motion is detected, save a snapshot
    if motion_detected:
        cv2.imwrite('motion_detected.jpg', frame)
        print('Motion detected! Saving snapshot...')
        
        # Reset the background frame to the current frame
        bg_frame = gray_frame
    
    # Display the current frame
    cv2.imshow('frame', frame)
    
    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

