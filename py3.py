import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import serial
import time
import numpy as np


ser = serial.Serial('COM11', 115200)
time.sleep(2)
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Initialize face detector
detector = FaceDetector(minDetectionCon=0.75)

# Servo parameters with reduced sensitivity
pan_center = 90
pan_range = 45  # ±45° from center
pan_min = 45
pan_max = 135
tilt_min, tilt_max = 30, 120

pan_angle = pan_center
tilt_angle = 90

# Sensitivity controls
pan_kp = 0.15  # Reduced from 0.2
tilt_kp = 0.2   # Reduced from 0.25
deadzone = 60    # Increased from 40
max_step = 3     # Maximum angle change per frame

# Smoothing buffer (moving average)
angle_buffer_size = 5
pan_buffer = [pan_center] * angle_buffer_size
tilt_buffer = [90] * angle_buffer_size

def constrain(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def smooth_angle(current_angle, buffer):
    buffer.pop(0)
    buffer.append(current_angle)
    return int(np.mean(buffer))

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img, bboxs = detector.findFaces(img, draw=True)

    if bboxs:
        bbox = bboxs[0]['bbox']
        x, y, w, h = bbox
        cx = x + w//2
        cy = y + h//2

        pan_error = cx - 320
        tilt_error = cy - 240

        # Calculate raw angle changes
        pan_delta = -pan_error * pan_kp
        tilt_delta = tilt_error * tilt_kp

        # Apply maximum step constraint
        pan_delta = constrain(pan_delta, -max_step, max_step)
        tilt_delta = constrain(tilt_delta, -max_step, max_step)

        # Update angles with multiple constraints
        if abs(pan_error) > deadzone:
            pan_angle += pan_delta
            pan_angle = constrain(pan_angle, pan_min, pan_max)

        if abs(tilt_error) > deadzone:
            tilt_angle += tilt_delta
            tilt_angle = constrain(tilt_angle, tilt_min, tilt_max)

        # Apply smoothing
        smooth_pan = smooth_angle(pan_angle, pan_buffer)
        smooth_tilt = smooth_angle(tilt_angle, tilt_buffer)

        
        cv2.putText(img, f"Pan: {smooth_pan}°", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.putText(img, f"Tilt: {smooth_tilt}°", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        # Send smoothed commands
        command = f"PAN:{smooth_pan}\nTILT:{smooth_tilt}\n"
        ser.write(command.encode())

    cv2.imshow("Face Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
