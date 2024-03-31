import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Function to preprocess and predict digits
def predict_digits(image, model):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Thresholding and contour detection
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a list to store recognized digits
    recognized_digits = []
    
    # Loop through detected contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Extract the digit region
        digit_roi = gray[y:y+h, x:x+w]
        # Resize the digit image to 28x28
        resized_digit = cv2.resize(digit_roi, (28, 28))
        # Normalize the pixel values
        resized_digit = resized_digit / 255.0
        # Reshape the image to match the input shape of the model
        resized_digit = np.reshape(resized_digit, (1, 28, 28, 1))
        # Make predictions using the model
        prediction = model.predict(resized_digit)
        # Get the predicted digit (index of the highest probability)
        predicted_digit = np.argmax(prediction)
        # Append the recognized digit to the list
        recognized_digits.append(predicted_digit)
    
    return recognized_digits

# Function to handle image upload
def upload_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        # Read the image file
        image = cv2.imread(file_path)
        if image is not None:
            # Predict digits in the image using the selected model
            recognized_digits = predict_digits(image, model)
            # Display recognized digits as text labels
            recognized_text = "Recognized digits: " + ''.join(str(digit) for digit in recognized_digits)
            label.config(text=recognized_text)
        else:
            label.config(text="Failed to load image.")
    else:
        label.config(text="No file selected.")

# Function to load model
def load_model_file():
    global model
    # Open a file dialog to select a model file
    file_path = filedialog.askopenfilename(filetypes=[("Model files", "*.h5")])
    if file_path:
        # Load the selected model file
        model = load_model(file_path)
        label.config(text="Model loaded successfully.")
    else:
        label.config(text="No model file selected.")

# Create the main window
window = tk.Tk()
window.title("Digit Recognizer")

# Create a label to display recognized digits
label = tk.Label(window, text="", font=("Arial", 14))
label.pack(pady=10)

# Create buttons to upload an image and load a model
upload_button = tk.Button(window, text="Upload Image", command=upload_image)
upload_button.pack(pady=5)

load_model_button = tk.Button(window, text="Load Model", command=load_model_file)
load_model_button.pack(pady=5)

# Run the Tkinter event loop
window.mainloop()
