# Import necessary libraries
import cv2
import numpy as np
import serial
import time
import matplotlib.pyplot as plt

board = serial.Serial(port="COM5", baudrate=9600, timeout=.1)

def send_data(data):
    board.write(bytes(data, "utf-8"))
    print("Send data: " + data)
def convert_data(index_data):
    data = ""
    

    for i in range(0,4):
        if i == index_data:
            data += "1"
        else:
            data += "0"
    
    return data
    
net = cv2.dnn.readNetFromDarknet("vendor/yolov3.cfg", "vendor/yolov3.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
classes = []
with open("vendor/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

indexes_list = []

src = input("# ")

for i in range(0,4):
    img = cv2.imread("input/"+src+"/traffic" + str(i) + ".jpg")

    height, width, channels = img.shape
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
    cars = 0
    # Loop through each output prediction
    for output in outputs:
        # Loop through each detection in the output
        for detection in output:
            # Get the class probabilities and class ID
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                cars += 1
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    traffic_classes = ['car', 'truck', 'bus', 'motorbike', 'bicycle']
    traffic_detected = False
    for i in range(len(boxes)):
        if i in indexes and classes[class_ids[i]] in traffic_classes:
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255, 255), 2)
    
    if src == "t1":
        cv2.imwrite("output/t1_output/output"+str(i) + ".jpeg", img)
    if src == "t2":
        cv2.imwrite("output/t2_output/output"+str(i) + ".jpeg", img)

    if len(indexes) > 5:
        print("traffic jam")
        
    else:
        print("no traffic jam")

    indexes_list.append(len(indexes))



to_send_data = convert_data(indexes_list.index(max(indexes_list)))
#print(to_send_data)
#print(type(to_send_data))
send_data(to_send_data)

#image = cv2.imread('output/t1_output/output44.jpeg')
#if src == "t2":
#    image = cv2.imread('output/t2_output/output32.jpeg')
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#plt.imshow(image)
#plt.axis('off')
#plt.show()