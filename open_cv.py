import cv2
import mediapipe as mp
import utility
import pyautogui


screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False, #capturing video
    model_complexity=1,
    min_detection_confidence=0.7 ,
    min_tracking_confidence=0.7,
    max_num_hands=1 # change to 2 and start testing
)
print(cv2.__version__)

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height) #actual position of index finger

        pyautogui.moveTo(x, y)

def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list)>=21:
        #index finger is the position of the mouse

        index_finger_tip = find_finger_tip(processed)
        print(index_finger_tip)
        thumb_index_distance = utility.get_distance([landmarks_list[4], landmarks_list[5]])

        if thumb_index_distance < 50 and utility.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])>90: #thumb is close to index and index is upright
            move_mouse(index_finger_tip)

        #left click

def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils

    try:
        while cap.isOpened():
            ret, frame = cap.read() #ret is a boolean value, if able to read frame it will be True

            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmarks_list = []

            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))

            
            #detecting gestures and code for moving the mouse
            detect_gestures(frame, landmarks_list, processed)


            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



# z coordinate is for how far the finger is from the camera