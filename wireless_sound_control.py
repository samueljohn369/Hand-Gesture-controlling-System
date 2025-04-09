import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize variables
x1 = y1 = x2 = y2 = x3 = y3 = x4 = y4 = prev_x = prev_y = 0
volume_change_threshold = 25  # Adjust as needed
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Initialize cooldown timers
pause_cooldown_start_time = mute_cooldown_start_time =  swipe_cooldown_start_time = time.time()
cooldown_duration = 2  # Cooldown duration in seconds
cooldown_duration1 = 0.5

while True:
    _, image = webcam.read()
    image = cv2.flip(image, 1)
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    # Check if cooldown time has passed for pause, mute, and swipe gestures
    if time.time() - pause_cooldown_start_time >= cooldown_duration:
        can_pause = True
    else:
        can_pause = False

    if time.time() - mute_cooldown_start_time >= cooldown_duration:
        can_mute = True
    else:
        can_mute = False

    if time.time() - swipe_cooldown_start_time >= cooldown_duration1:
        can_swipe = True
    else:
        can_swipe = False

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 4:  # Thumb landmark
                    x1 = x
                    y1 = y
                elif id == 8:  # Index finger landmark
                    x2 = x
                    y2 = y
                elif id == 12:  # Middle finger landmark
                    x3 = x
                    y3 = y
                elif id == 16:  # Ring finger landmark
                    x4 = x
                    y4 = y

        # Draw line between thumb and index finger
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

        # Calculate distances between fingers
        dist_thumb_index = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        dist_thumb_middle = ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5

        # Adjust volume based on distance between thumb and index finger
        if dist_thumb_index > volume_change_threshold:
            pyautogui.press("volumeup")
        elif dist_thumb_index < volume_change_threshold:
            pyautogui.press("volumedown")
        if dist_thumb_index < 10:
            pyautogui.press("volumemute")
            mute_cooldown_start_time = time.time()

        # Pause if the hand is fully open (distance between thumb and middle finger is large) and cooldown time has passed
        if dist_thumb_middle > 100 and can_pause:
            pyautogui.press("space")
            # Start pause cooldown timer
            pause_cooldown_start_time = time.time()

        # Detect swipe gesture
        if prev_x != 0 and prev_y != 0:
            # Calculate the direction of movement
            dx = x2 - prev_x
            dy = y2 - prev_y

            # Determine if it's a horizontal or vertical swipe
            if abs(dx) > abs(dy):
                if dx > 20 and can_swipe:  # Right swipe
                    pyautogui.hotkey('shift', 'n')  # Switch to the next tab
                    swipe_cooldown_start_time = time.time()  # Start swipe cooldown timer
                elif dx < -20 and can_swipe:  # Left swipe
                    pyautogui.hotkey( 'shift', 'p')  # Switch to the previous tab
                    swipe_cooldown_start_time = time.time()  # Start swipe cooldown timer
           # else:
             #   if dy > 20 and can_swipe:  # Down swipe
              #      pyautogui.press('pagedown')  # Scroll down or switch to the next page
              #      swipe_cooldown_start_time = time.time()  # Start swipe cooldown timer
               # elif dy < -20 and can_swipe:  # Up swipe
               #     pyautogui.press('pageup')  # Scroll up or switch to the previous page
               #     swipe_cooldown_start_time = time.time()  # Start swipe cooldown timer

        # Update previous hand position
        prev_x = x2
        prev_y = y2

    # Display the frame
    cv2.imshow("Hand Gesture Recognition", image)

    # Check for exit key
    key = cv2.waitKey(10)
    if key == 27:
        break

# Release the webcam and close all windows
webcam.release()
cv2.destroyAllWindows()
