import mediapipe as mp
import cv2
import screen_brightness_control as sbc

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

video = cv2.VideoCapture(0)

def main_brightness():
    while video.isOpened():
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for palms in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, palms, mp_hands.HAND_CONNECTIONS)
                hand_landmarks = palms.landmark
                handedness = results.multi_handedness

            finger_count = {'right': 0, 'left': 0}

            finger_tip_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                          mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]

            thumb_tip_id = mp_hands.HandLandmark.THUMB_TIP

            finger_open_status = {'left_thumb': False, 'left_index': False, 'left_middle': False, 'left_ring': False,
            'left_pinky': False, 'right_thumb': False, 'right_index': False, 'right_middle': False, 'right_ring': False,
            'right_pinky': False}

            for hand_index, hand_info in enumerate(handedness):
                hand_label = hand_info.classification[0].label
                hand_landmarks = results.multi_hand_landmarks[hand_index]

                for tip_index in finger_tip_ids:
                    finger_name = tip_index.name.split('_')[0]
                    finger_tip = hand_landmarks.landmark[tip_index]
                    mid_knuckle = hand_landmarks.landmark[tip_index-2]

                    if finger_tip.y < mid_knuckle.y:
                        finger_open_status[f'{hand_label.lower()}_{finger_name.lower()}'] = True
                        finger_count[hand_label.lower()] += 1

                thumb_name = thumb_tip_id.name.split('_')[0]
                thumb_tip = hand_landmarks.landmark[thumb_tip_id]
                mid_thumb = hand_landmarks.landmark[thumb_tip_id-1]

                if hand_label.lower() == 'right':
                    if thumb_tip.x < mid_thumb.x:
                        finger_open_status[f'{hand_label.lower()}_{thumb_name.lower()}'] = True
                        finger_count[hand_label.lower()] += 1
                elif hand_label.lower() == 'left':
                    if thumb_tip.x > mid_thumb.x:
                        finger_open_status[f'{hand_label.lower()}_{thumb_name.lower()}'] = True
                        finger_count[hand_label.lower()] += 1

            total_finger_count = finger_count['right'] + finger_count['left']

            current_brightness = sbc.get_brightness()

            if total_finger_count == 0:
                sbc.set_brightness(10)
            else:
                new_brightness = sbc.set_brightness(total_finger_count * 10)

                print(total_finger_count*10)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('Gesture Brightness Control', frame)


