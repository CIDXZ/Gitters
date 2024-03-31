import os
import time
import pyautogui

def get_lesson_info():
    num_lessons = int(input("Enter the number of lessons: "))
    lesson_durations = []
    for i in range(num_lessons):
        duration_min = int(input(f"Enter the duration of lesson {i+1} (in minutes): "))
        duration_sec = duration_min * 60  # Convert minutes to seconds
        lesson_durations.append(duration_sec)
    return lesson_durations

def watch_lessons(folder_path, lesson_durations):
    # Get a list of all image files in the specified folder
    lesson_images = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    # Sort the lesson images alphabetically
    lesson_images.sort()
    
    # Iterate through each lesson image and its corresponding duration
    for i in range(len(lesson_images)):
        # Get the full path to the lesson image and its duration text
        image_path = os.path.join(folder_path, lesson_images[i])
        next_image_path = os.path.join(folder_path, lesson_images[i + 1]) if i + 1 < len(lesson_images) else None
        
        # Click on the current lesson image
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)  # Adjust confidence as needed
        if location is not None:
            # Wait for the lesson image to fully appear on the screen
            time.sleep(2)  # Adjust the delay as needed
            
            # Click on the current lesson image
            pyautogui.click(location)
            
            time.sleep(2)
            
            # Press the 'k' key after clicking on the lesson image
            pyautogui.press('k')
        
        # Wait for the duration of the current lesson
        if i < len(lesson_durations):
            duration = lesson_durations[i]
            time.sleep(duration)  # Wait for the specified duration
        
        # Move to the next lesson's duration
        if next_image_path is not None:
            next_location = pyautogui.locateCenterOnScreen(next_image_path, confidence=0.8)  # Adjust confidence as needed
            if next_location is not None:
                # Click to select the next lesson
                pyautogui.click(next_location)

# Specify the folder path containing lesson images
folder_path = r'D:\Course'

# Get lesson durations from the user
lesson_durations = get_lesson_info()

# Grace period to switch tabs
print("Switch to the browser tab where you want to start watching the lessons.")
time.sleep(5)

# Call the function to watch the lessons
watch_lessons(folder_path, lesson_durations)













