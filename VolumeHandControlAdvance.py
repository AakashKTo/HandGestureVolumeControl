import cv2
import numpy as np
import time
import math
from HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 1920, 1200
lock_duration = 5  # Time (in seconds) to lock volume adjustment after finalizing
################################

cap = cv2.VideoCapture(0)  # Use 0 for the default camera
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(detectionCon=0.7)

# Audio utilities setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

# Volume lock variables
volume_locked = False
lock_start_time = 0

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Failed to capture frame. Skipping...")
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        # Check if the palm is open and facing the camera
        fingers = detector.fingersUp()
        if fingers == [1, 1, 1, 1, 1]:  # All fingers open
            # Calculate distance between thumb and ring finger
            x1, y1 = lmList[4][1], lmList[4][2]  # Thumb
            x2, y2 = lmList[16][1], lmList[16][2]  # Ring finger
            length = math.hypot(x2 - x1, y2 - y1)

            # Calculate bounding box diagonal and set max range
            if bbox:
                bbox_diagonal = math.hypot(bbox[2] - bbox[0], bbox[3] - bbox[1])
                max_distance = bbox_diagonal / 1.3
            else:
                max_distance = 400  # Fallback to a default value if bbox isn't found

            # Map the length to volume range
            vol = np.interp(length, [50, max_distance], [minVol, maxVol])
            volBar = np.interp(length, [50, max_distance], [400, 150])
            volPer = np.interp(length, [50, max_distance], [0, 100])

            # Update volume if not locked
            if not volume_locked:
                volume.SetMasterVolumeLevel(vol, None)

            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        if fingers == [1, 1, 1, 1, 0]:
            if not volume_locked:
                volume_locked = True
                lock_start_time = time.time()

    if volume_locked and (time.time() - lock_start_time > lock_duration):
        volume_locked = False

    cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)  # Black border
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 0), cv2.FILLED)  # Black filled bar

    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)  # Black text


    if volume_locked:
        cv2.putText(img, "Volume Locked", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()