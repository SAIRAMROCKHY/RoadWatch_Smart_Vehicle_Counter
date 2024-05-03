from google.colab.patches import cv2_imshow
import cv2
import numpy as np

min_width = 40  
min_height = 40  
offset = 10  
detection_line_height = 550  
detections = []
vehicle_count = 0

def calculate_centroid(x, y, w, h):
    x_center = int(w / 2)
    y_center = int(h / 2)
    cx = x + x_center
    cy = y + y_center
    return cx, cy

cap = cv2.VideoCapture('/content/drive/MyDrive/Video.mp4')
cap.set(3, 1920)
cap.set(4, 1080)

if cap.isOpened():
    ret, frame1 = cap.read()
else:
    ret = False

ret, frame1 = cap.read()
ret, frame2 = cap.read()

resize_factor = 0.5

while ret:
    frame_diff = cv2.absdiff(frame1, frame2)
    cv2_imshow(cv2.resize(frame_diff, None, fx=resize_factor, fy=resize_factor))
    grey = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    cv2_imshow(cv2.resize(grey, None, fx=resize_factor, fy=resize_factor))
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    cv2_imshow(cv2.resize(blur, None, fx=resize_factor, fy=resize_factor))
    ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    cv2_imshow(cv2.resize(th, None, fx=resize_factor, fy=resize_factor))
    dilated = cv2.dilate(th, np.ones((3, 3)))
    cv2_imshow(cv2.resize(dilated, None, fx=resize_factor, fy=resize_factor))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    cv2_imshow(cv2.resize(closing, None, fx=resize_factor, fy=resize_factor))
    contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    frame_with_contours = frame1.copy()
    cv2.drawContours(frame_with_contours, contours, -1, (0, 255, 0), 2)
    cv2_imshow(cv2.resize(frame_with_contours, None, fx=resize_factor, fy=resize_factor))
    for(i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        contour_valid = (w >= min_width) and (h >= min_height)
        if not contour_valid:
            continue
        cv2.rectangle(frame1, (x-10, y-10), (x+w+10, y+h+10), (255, 0, 0), 2)
        cv2.line(frame1, (0, detection_line_height), (1200, detection_line_height), (0, 255, 0), 2)
        centroid = calculate_centroid(x, y, w, h)
        detections.append(centroid)
        cv2.circle(frame1, centroid, 5, (0, 255, 0), -1)
        cv2_imshow(cv2.resize(frame1, None, fx=resize_factor, fy=resize_factor))
        cx, cy = calculate_centroid(x, y, w, h)
        for (x, y) in detections:
            if y < (detection_line_height+offset) and y > (detection_line_height-offset):
                vehicle_count += 1
                detections.remove((x, y))
    cv2.putText(frame1, "Total Vehicles Detected: " + str(vehicle_count), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 170, 0), 2)
    cv2_imshow(cv2.resize(frame1, None, fx=resize_factor, fy=resize_factor))
    if cv2.waitKey(1) == 27:
        break
    frame1 = frame2
    ret, frame2 = cap.read()

cap.release()
