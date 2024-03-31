import cv2
import numpy as np
from tkinter import Tk, filedialog

def select_files():
    root = Tk()
    root.withdraw()  # Hide the main window
    weights_path = filedialog.askopenfilename(title="Select weights file", filetypes=(("Weights files", "*.weights"), ("All files", "*.*")))
    cfg_path = filedialog.askopenfilename(title="Select config file", filetypes=(("Config files", "*.cfg"), ("All files", "*.*")))
    root.destroy()
    return weights_path, cfg_path

def detect_objects(image, weights_path, cfg_path):
    net = cv2.dnn.readNet(weights_path, cfg_path)
    # Convert image to blob and set it as input to the network
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())
    # Get information about detected objects
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    # Non-maximum suppression to remove redundant bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in indices:
        i = i[0]
        x, y, w, h = boxes[i]
        label = str(class_ids[i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

def select_image():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select image file", filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))
    root.destroy()
    if file_path:
        image = cv2.imread(file_path)
        weights_path, cfg_path = select_files()
        if weights_path and cfg_path:
            result_image = detect_objects(image, weights_path, cfg_path)
            cv2.imshow("Object Detection", result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

# Example usage
select_image()
