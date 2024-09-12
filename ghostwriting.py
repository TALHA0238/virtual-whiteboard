import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# OpenCV video capture
cap = cv2.VideoCapture(0)

# Create a whiteboard canvas
canvas = np.zeros((480, 640, 3), dtype="uint8") + 255  # Whiteboard size

# Variables to store the previous fingertip position and drawing state
prev_x, prev_y = 0, 0
drawing_active = False

# Define a minimum distance threshold for drawing (to avoid jitter)
draw_threshold = 10


def distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def count_fingers(hand_landmarks):
    """Count the number of fingers being shown based on hand landmarks."""
    finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                   mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    extended_fingers = 0
    for finger_tip in finger_tips:
        tip_landmark = hand_landmarks.landmark[finger_tip]
        if tip_landmark.y < hand_landmarks.landmark[
            mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y:  # Compare against middle finger base
            extended_fingers += 1
    return extended_fingers


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the image horizontally for a selfie-view display
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert BGR to RGB for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Count the number of fingers being shown
            num_fingers = count_fingers(hand_landmarks)

            # Get the index fingertip (landmark 8) coordinates
            index_finger_tip = hand_landmarks.landmark[8]
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)

            if num_fingers == 1:
                # Only enable drawing if exactly one finger is shown
                if not drawing_active:
                    # Start a new drawing segment
                    drawing_active = True
                    prev_x, prev_y = x, y  # Initialize first point
                else:
                    # Check if the finger has moved enough to draw
                    dist = distance(prev_x, prev_y, x, y)
                    if dist > draw_threshold:
                        # Draw line between previous point and current point
                        cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 0), thickness=4)
                        prev_x, prev_y = x, y  # Update previous coordinates
            else:
                # Disable drawing if not exactly one finger is shown
                if drawing_active:
                    drawing_active = False
                    prev_x, prev_y = 0, 0  # Reset previous coordinates when drawing stops

            # Draw hand landmarks (optional for visual feedback)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        # Reset previous coordinates when the hand is not detected
        if drawing_active:
            drawing_active = False
            prev_x, prev_y = 0, 0

    # Display the whiteboard (canvas)
    cv2.imshow("Whiteboard", canvas)

    # Display the webcam frame
    cv2.imshow("Frame", frame)

    # Reset when 'r' is pressed to clear the board
    if cv2.waitKey(1) & 0xFF == ord('r'):
        canvas[:] = 255  # Clear the whiteboard

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
