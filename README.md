# Hand-Gesture-controlling-System
A Python-based application that allows you to control system volume, mute, play/pause, and swipe between media using just hand gestures detected through your webcam. Built with OpenCV, MediaPipe, and PyAutoGUI.


PROJECT DESCRIPTION

Audio and Video Control Using Hand Gestures is a real-time computer vision project that allows users to interact with their system’s media controls using simple hand gestures. This eliminates the need for physical input devices such as a keyboard or remote when adjusting volume, muting audio, or navigating media content.

The application captures video feed from the webcam, detects and tracks hand landmarks using MediaPipe, and maps specific gestures to system-level media control actions using PyAutoGUI. The entire process runs in real time, offering a hands-free and intuitive way to manage your multimedia experience.

FEATURES

🔊 Volume Up/Down – Adjusted using the distance between your thumb and index finger.

🔇 Mute/Unmute – Triggered when fingers pinch (very close).

⏯ Play/Pause – Detected when thumb and middle finger are spread apart.

⬅️➡️ Swipe Navigation – Move hand left/right to simulate swiping to previous/next media tab.



Libraries used

| Library        | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| opencv-python  | To capture real-time video from the webcam and display visual output.   |
| mediapipe      | For real-time hand tracking and landmark detection.                     |
| pyautogui      | To send simulated key presses for controlling system functions.         |
| time (builtin) | For handling gesture cooldown timing.                                   |





WORKING EXPLANATION

This project uses a combination of computer vision, hand tracking, and keyboard automation to control system media functions through hand gestures. Here's a step-by-step breakdown of how the application works:

1. Webcam Initialization
   
     The webcam is accessed using OpenCV (cv2.VideoCapture(0)), which continuously captures video frames.

     Each frame is horizontally flipped (cv2.flip) to mimic a mirror view, making hand movements intuitive.

2. Hand Detection
   
     Each frame is converted from BGR to RGB and passed to MediaPipe’s Hand Detection module.

     MediaPipe detects one or two hands and returns 21 hand landmarks per hand.

     Landmarks include fingertips, knuckles, and wrist positions.

3. Gesture Analysis
   
     Once the landmarks are detected, the system calculates distances and movements to recognize specific gestures:

     📶 Volume Control
     Measures the distance between the thumb (ID 4) and index finger (ID 8).

     If the distance increases: volume up.

     If the distance decreases: volume down.

     🔇 Mute
     If thumb and index finger touch each other (distance very small), it triggers a mute action using pyautogui.press('volumemute').

     ⏸ Pause/Play
     Measures the distance between thumb (ID 4) and middle finger (ID 12).

     If the hand is fully open, the distance increases, which indicates a pause/play command using pyautogui.press('space').

     👉 Swipe Gestures
     Uses the movement of the index finger (ID 8) across consecutive frames.

     Detects horizontal swipes:

     Right swipe → Shift + N (Next tab or slide)

     Left swipe → Shift + P (Previous tab or slide)

4. Action Execution
   
     Based on the recognized gesture, the system uses pyautogui to simulate keyboard key presses.

     This allows the gestures to control media, change tabs, or mute/unmute the system.

5. Cooldown Timers
   
     To avoid repeated unintentional triggers, cooldown timers are used for:

     Mute

     Pause/Play

     Swipe gestures

     These timers ensure gestures are only recognized after a short wait period (e.g., 0.5s – 2s).

6. Display & Exit
   
     The processed video with drawn landmarks and gesture visuals is shown in a window titled "Hand Gesture Recognition".

     Press ESC key to exit and release the webcam.




Install Requirements

<pre lang="markdown"> pip install opencv-python mediapipe pyautogui  </pre>






