
Hi, I’m @TALHA0238

Hand-Tracking Virtual Whiteboard Project

Project Overview

This project allows users to draw on a virtual whiteboard using their index finger. The whiteboard is displayed in a window, and the drawing is based on real-time hand tracking and gesture recognition.

Features:
Hand detection and tracking using Mediapipe.
Drawing activation when one finger is extended.
Smooth drawing with a distance threshold to reduce jitter.
Option to reset the whiteboard with a key press.
Ability to quit the application with a key press.

Workflow and Steps

1.Installation:
Before running the project, ensure you have the required libraries installed:
```bash
pip install opencv-python mediapipe numpy


 2.How It Works:
This project enables users to draw on a virtual canvas by using their index finger. The drawing begins when only one finger is detected and tracks the finger's movement, creating a line between previous and current positions.

 Key Features:
-Hand Detection: Detects the user's hand using Mediapipe’s hand landmarks model.
-Drawing Mode: Activated when exactly one finger is extended. The finger’s movement is used to draw lines on the canvas.
- Jitter Reduction: A minimum distance threshold is applied to ensure smooth drawing without unwanted jitter.
- Clear Canvas: The whiteboard can be cleared by pressing the 'r' key.
- Exit: The application can be closed by pressing the 'q' key.

Code Workflow

1.Initialize Mediapipe: Hand tracking is initialized to detect and track the landmarks of the hand.
2.Video Capture: A webcam feed is captured using OpenCV.
3. Hand Detection & Finger Counting: The program detects whether one or more fingers are extended.
4. Drawing Mechanism: If exactly one finger is shown, the program draws lines based on fingertip movement.
5. Canvas Reset: Pressing 'r' will clear the whiteboard.
6. Exit the Application: Press 'q' to close the application.

Usage Instructions

1. Run the Python script to open the webcam feed.
2. Show one finger to start drawing.
3. Move your finger across the screen to draw lines.
4. Press 'r' to reset the canvas.
5. Press 'q' to quit the application.

Requirements

- Python 3.x (Latest version)
- OpenCV
- Mediapipe
- NumPy

Installation

Install the required packages:
```bash
pip install opencv-python mediapipe numpy
