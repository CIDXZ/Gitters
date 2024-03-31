import cv2
import numpy as np

# Function to find the palm of the hand
def detect_palm(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding to segment the hand
    _, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with the largest area (the hand)
    max_contour = max(contours, key=cv2.contourArea)
    
    # Find the convex hull of the hand
    hull = cv2.convexHull(max_contour, returnPoints=False)
    
    # Find the defects in the convex hull
    defects = cv2.convexityDefects(max_contour, hull)
    
    # Draw the palm region
    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, _ = defects[i, 0]
            start = tuple(max_contour[s][0])
            end = tuple(max_contour[e][0])
            far = tuple(max_contour[f][0])
            cv2.line(frame, start, end, [0, 255, 0], 2)
            cv2.circle(frame, far, 5, [0, 0, 255], -1)
    
    return frame

# Function to capture video from camera
def capture_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect the palm of the hand
        frame = detect_palm(frame)
        
        # Display the frame
        cv2.imshow('Hand Detection', frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Run the function to capture video
capture_video()
