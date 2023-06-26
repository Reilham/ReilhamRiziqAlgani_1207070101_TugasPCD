import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.Hands
hands = mpHands.Hands()

while True:
    success, img = cap.read()

    cv2.imshow("image", img)
    cv2.waitKey(1)  # Wait for 1 millisecond for a key press (use a small delay to allow OpenCV to handle events)

    if cv2.waitKey(1) == 27:  # Exit when "Esc" key is pressed
        break

cap.release()
cv2.destroyAllWindows()