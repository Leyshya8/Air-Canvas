# Air-Canvas Real-Time Gesture-Based Drawing
Air Canvas is a computer vision application that allows users to draw in a virtual space using hand gestures. By leveraging MediaPipe for high-fidelity hand tracking and OpenCV for real-time image processing, this project transforms a standard webcam into a digital canvas.

Key Features
Hand Gesture Recognition: Uses MediaPipe to detect hand landmarks and interpret finger positions.
Dynamic Drawing Modes:

Selection Mode (2 Fingers Up): Hover over the toolbar to select colors (Blue, Green, Red, Yellow), switch to the Eraser, or Clear the canvas.

Drawing Mode (1 Finger Up): Draw smooth lines in the selected color or erase existing strokes.

Live Canvas Overlay: Uses bitwise operations to merge a persistent drawing canvas onto the live webcam feed.

Visual HUD: Provides real-time feedback on the current color, mode, and control instructions.

Technical Stack
Language: Python
Computer Vision: OpenCV (cv2)
Hand Tracking: MediaPipe (Hands module)
Data Structures: Deques and Dictionaries for state management and stroke history.

How to Use
Run the script: python air-canvas.py

Select a Tool: Raise both your index and middle fingers and move the cursor over the buttons in the top toolbar.

Draw: Raise only your index finger and move it across the screen (below the toolbar area).

Erase: Select the "Eraser" from the toolbar using two fingers, then use one finger to "paint" over mistakes.

Clear: Hover over the "Clear" button with two fingers to reset the entire canvas.

Exit: Press 'Q' on your keyboard to close the application.
