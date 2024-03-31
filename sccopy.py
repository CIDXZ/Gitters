import pytesseract
import pyautogui

# Set the path to Tesseract executable (you may need to change this)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Take a screenshot of the entire screen
screenshot = pyautogui.screenshot()

# Use pytesseract to extract text from the screenshot
extracted_text = pytesseract.image_to_string(screenshot)

# Specify the file path where you want to save the extracted text
output_file = 'extracted_text.txt'

# Write the extracted text to a text file
with open(output_file, 'w') as file:
    file.write(extracted_text)

print("Text extracted from the screen has been saved to", output_file)
