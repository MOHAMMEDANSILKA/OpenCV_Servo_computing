import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import serial
import time
import numpy as np

# Initialize serial connection.
ser = serial.Serial('COM11', 115200)
time.sleep(2)

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Initialize face detector
detector = FaceDetector(minDetectionCon=0.75, modelSelection=1)

# Servo parameters for responsive tracking
pan_center = 90
pan_range = 45
pan_min = 45
pan_max = 135
tilt_min, tilt_max = 30, 120

pan_angle = pan_center
tilt_angle = 90

# Responsive control parameters
pan_kp = 0.25  # Direct response gain
tilt_kp = 0.3
deadzone = 15    # Small deadzone for immediate response
max_step = 5     # Larger maximum step size

# Minimal smoothing
angle_buffer_size = 2
pan_buffer = [pan_center] * angle_buffer_size
tilt_buffer = [90] * angle_buffer_size

def constrain(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def map_angle(error, max_error=320):
    """Direct mapping from pixel error to angle change"""
    return (error / max_error) * 180

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip image for mirror effect
    img = cv2.flip(img, 1)
    
    # Detect faces
    img, bboxs = detector.findFaces(img, draw=True)

    if bboxs:
        # Track largest face
        bbox = bboxs[0]['bbox']
        x, y, w, h = bbox
        cx = x + w//2
        cy = y + h//2

        # Immediate error calculation
        pan_error = cx - 320
        tilt_error = cy - 240

        # Direct proportional control
        pan_delta = -pan_error * pan_kp
        tilt_delta = tilt_error * tilt_kp

        # Apply constraints
        pan_delta = constrain(pan_delta, -max_step, max_step)
        tilt_delta = constrain(tilt_delta, -max_step, max_step)

        # Update angles
        pan_angle += pan_delta
        tilt_angle += tilt_delta

        # Constrain angles
        pan_angle = constrain(pan_angle, pan_min, pan_max)
        tilt_angle = constrain(tilt_angle, tilt_min, tilt_max)

        # Minimal smoothing
        smooth_pan = int(np.mean([pan_buffer[-1], pan_angle]))
        smooth_tilt = int(np.mean([tilt_buffer[-1], tilt_angle]))
        pan_buffer.append(pan_angle)
        tilt_buffer.append(tilt_angle)
        pan_buffer.pop(0)
        tilt_buffer.pop(0)

        # Send commands immediately
        command = f"PAN:{smooth_pan}\nTILT:{smooth_tilt}\n"
        ser.write(command.encode())

        # Visual feedback
        cv2.line(img, (320, 240), (cx, cy), (0, 255, 0), 2)
        cv2.putText(img, f"Pan: {smooth_pan}°", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.putText(img, f"Tilt: {smooth_tilt}°", (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Face Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
