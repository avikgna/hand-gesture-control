import mediapipe as mp
import cv2
import math

# How often (in seconds) we print the distance
printer_timer = 1

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    x1 = x2 = y1 = y2 = 0
    count = 0
    while True:
        ret_val, frame = cam.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for palms in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, palms, mp_hands.HAND_CONNECTIONS)
                hand_landmarks = palms.landmark
                for id, landmark in enumerate(hand_landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    if id == 8:
                        cv2.circle(img=frame, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                        x1 = x
                        y1 = y
                    if id == 4:
                        cv2.circle(img=frame, center=(x, y), radius=8, color=(255, 255, 0), thickness=3)
                        x2 = x
                        y2 = y
                    cv2.line(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 0, 0), thickness=5)

                    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                    max_dist = 160
                    min_dist = 25

                    normalised_dist = ((dist - min_dist) / (max_dist - min_dist))
                    if normalised_dist < 0:
                        normalised_dist = 0
                    elif normalised_dist > 1:
                        normalised_dist = 1

                    mapped_vol = int((normalised_dist // 0.1) * 10)

                    # just in case, not needed though
                    if mapped_vol > 100:
                        mapped_vol = 100
                    elif mapped_vol < 0:
                        mapped_vol = 0

        else:
            mapped_vol = 0

        if count % (printer_timer * 20) == 0:
            print(mapped_vol, end='\n')

        count += 1

        cv2.imshow('my webcam', frame)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()