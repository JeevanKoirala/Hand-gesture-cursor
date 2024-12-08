import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Set up the webcam
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Camera not accessible!")
    exit()

# Get screen width and height (adjust this based on your screen resolution)
screen_width, screen_height = pyautogui.size()  # Get the screen resolution

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera.")
        break

    
    frame = cv2.resize(frame, (640, 480))

    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    results = hands.process(rgb_frame)

    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])

            
            thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * frame.shape[1]
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * frame.shape[0]

            
            screen_x = x * screen_width / frame.shape[1]
            screen_y = y * screen_height / frame.shape[0]

            
            pyautogui.moveTo(screen_x, screen_y)

            
            
            if abs(x - thumb_x) < 25 and abs(y - thumb_y) < 25:  
                pyautogui.click()  

            
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)  

            
            cv2.circle(frame, (int(thumb_x), int(thumb_y)), 10, (255, 0, 0), -1)  

            
            cv2.circle(frame, (x, y), 15, (0, 255, 255), -1) 

    
    cv2.imshow('Hand Cursor', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break


cap.release()
cv2.destroyAllWindows()

