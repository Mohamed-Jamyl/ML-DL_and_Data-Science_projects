import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_gesture = None  
font = cv2.FONT_HERSHEY_SIMPLEX

def fingers_up(hand_landmarks):
    fingers = []

    fingers.append(0)

    for tip in [8, 12, 16, 20]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def get_gesture(fingers):
    if fingers == [0, 1, 0, 0, 0]:  
        return 'jump'
    elif fingers == [0, 1, 1, 1, 1]:  
        return 'slide'
    elif fingers == [0, 0, 0, 0, 0]: 
        return 'none'
    else:
        return 'none' 

def perform_action(gesture):
    if gesture == 'jump':
        pyautogui.press('up')
        print("JUMP")
    elif gesture == 'slide':
        pyautogui.press('down')
        print("SLIDE")

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    gesture_text = ""

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = fingers_up(handLms)
            gesture = get_gesture(fingers)

            if gesture != prev_gesture and gesture != 'none':
                perform_action(gesture)
                prev_gesture = gesture
                gesture_text = gesture.upper()
            elif gesture == 'none':
                prev_gesture = 'none'
                gesture_text = "REST"

    if gesture_text:
        cv2.putText(img, f"Gesture: {gesture_text}", (10, 50), font, 1, (0, 255, 0), 2)

    cv2.imshow("Dino Game - Hand Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
