import mediapipe as mp
import cv2
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# python module for capturing and processing video and image input
# cv2 is used in this project to capture feedback from webcam
speakers = AudioUtilities.GetSpeakers()
speakers_interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                                      )
volume = cast(speakers_interface, POINTER(IAudioEndpointVolume))

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


video = cv2.VideoCapture(0)
# capturing video using default webcam
def main_volume():
    x1 = x2 = y1 = y2 = 0
    while video.isOpened():
        ret, frame = video.read()
        frame_height, frame_width, _ = frame.shape
# reading/capturing frame from webcam, ret used to determine if frame was read sucessfully
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for palms in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, palms, mp_hands.HAND_CONNECTIONS)
                hand_landmarks = palms.landmark
                for id, landmark in enumerate(hand_landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                # converting normalised landmark coordinates into pixel coordinates
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=8, color=(0,255,255), thickness=3)
                        x1 = x
                        y1 = y
                    # BGR color (B,G,R)
                    if id == 4:
                        cv2.circle(img=frame, center=(x,y),radius=8, color=(255,255,0), thickness=3)
                        x2 = x
                        y2 = y
                    cv2.line(img=frame, pt1=(x1,y1), pt2=(x2,y2), color = (0,0,0), thickness=5)

                    dist = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))
                    max_dist = 160
                    min_dist = 25
                    max_vol = 100
                    min_vol = 0

                    normalised_dist = ((dist-min_dist)/(max_dist-min_dist))
                    if normalised_dist < 0:
                        normalised_dist = 0
                    elif normalised_dist > 1:
                        normalised_dist = 1

                    mapped_vol = int(normalised_dist * max_vol)/100

                    volume.SetMasterVolumeLevelScalar(mapped_vol, None)

    # processing the image read from the webcam

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('Gesture Volume Control', frame)
# displaying the image

    video.release()
    cv2.destroyAllWindows()

