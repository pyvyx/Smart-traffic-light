# Import necessary libraries
import cv2
import numpy as np

# Load the pre-trained YOLOv3 model and its configuration files
net = cv2.dnn.readNetFromDarknet("vendor/yolov3.cfg", "vendor/yolov3.weights")

# Set the backend and target of the network to run on CPU
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load the names of the classes the model can detect
classes = []
with open("vendor/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Define a list of colors for the bounding boxes of each class
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load the input image
img = cv2.imread("img/traffic.jpg")

# Get the dimensions of the image
height, width, channels = img.shape

# Create a blob from the input image to feed into the model
blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), swapRB=True, crop=False)

# Set the input blob as the input for the model
net.setInput(blob)

# Get the output layer names of the model
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Forward pass through the model to get the output predictions
outputs = net.forward(output_layers)

# Initialize lists to store the bounding boxes, confidences, and class IDs
boxes = []
confidences = []
class_ids = []

# Loop through each output prediction
for output in outputs:
    # Loop through each detection in the output
    for detection in output:
        # Get the class probabilities and class ID
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        # Filter out weak detections with low confidence scores
        if confidence > 0.5:
            # Scale the bounding box coordinates to match the original image size
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            # Add the bounding box, confidence, and class ID to their respective lists
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply non-maximum suppression to eliminate redundant overlapping bounding boxes
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Check if any of the detected classes are related to traffic jam
traffic_classes = ['car', 'truck', 'bus', 'motorbike', 'bicycle']
traffic_detected = False
for i in range(len(boxes)):
    if i in indexes and classes[class_ids[i]] in traffic_classes:
        x, y, w, h = boxes[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255, 255), 2)

cv2.imwrite("output.jpg", img)
# Print the result of whether a traffic jam was detected or not
if len(indexes) > 5:
    print("Traffic jam detected in the image.")
else:
    print("No traffic jam detected in the image.")
