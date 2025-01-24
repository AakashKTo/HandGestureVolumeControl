# Hand Gesture Volume Control

This project allows you to control your system's volume using hand gestures detected via a webcam. It uses OpenCV, MediaPipe, and Pycaw to track hand landmarks and control the audio output.

---

## Features
- Real-time hand tracking with MediaPipe.
- Detects gestures for controlling volume:
  - **Index and Thumb Distance**: Adjusts the volume.
  - **Pinky Finger Down**: Sets the volume.
- Displays:
  - Volume bar and percentage on the screen.
  - Current system volume.
  - Frames per second (FPS).

---

## Requirements

To run this project, you need the following:
- Python 3.x
- A webcam (internal or external)

---

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies by running:

   ```bash
   pip install -r requirements.txt
