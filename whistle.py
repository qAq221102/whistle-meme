import cv2
import mediapipe as mp
import pygame
import pyautogui
import FFP

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose                      # mediapipe 姿勢偵測
frame_rate = 30
delay = 1.0/frame_rate
Width, Height = pyautogui.size()  # current screen size
pygame.mixer.init()
print(cap.get(cv2.CAP_PROP_FPS))

def middle(width, height):
    return (Width-width)//2, (Height-height)//2


# 啟用姿勢偵測
with mp_pose.Pose(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.4) as pose:

    ret, img = cap.read()
    cv2.namedWindow('CAMERA', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('CAMERA', img.shape[1], img.shape[0])
    x, y = middle(img.shape[1], img.shape[0])
    cv2.moveWindow('CAMERA', x, y)
    while True:
        start_time = cv2.getTickCount()
        ret, img = cap.read()

        if not ret:
            print("Cannot receive frame")
            break

        img = cv2.resize(img, (520, 300))               # 縮小尺寸，加快演算速度
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
        results = pose.process(img2)                  # 取得姿勢偵測結果
        # 根據姿勢偵測結果，標記身體節點和骨架
        mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        cv2.imshow('CAMERA', img)

        # 判斷左右手腕是否停在頭部位置上
        if results.pose_landmarks:
            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_eye = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
            right_eye = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]
            shoulder_range = [right_shoulder.x, left_shoulder.x]
            left_eye2shoulder = [left_eye.y, left_shoulder.y]
            right_eye2shoulder = [right_eye.y, right_shoulder.y]
            if shoulder_range[0] <= right_wrist.x <= shoulder_range[1] and shoulder_range[0] <= left_wrist.x <= shoulder_range[1] and right_wrist.x < left_wrist.x:
                if right_eye2shoulder[0] <= right_wrist.y <= right_eye2shoulder[1] and left_eye2shoulder[0] <= left_wrist.y <= left_eye2shoulder[1]:

                    # process the video
                    cap_path = FFP.FBW('Josh Hutcherson whistle.mp4')
                    meme_cap = cv2.VideoCapture(cap_path)
                    ret, mimg = meme_cap.read()
                    cv2.namedWindow('WHISTLE MEME', cv2.WINDOW_NORMAL)
                    x, y = middle(mimg.shape[1], mimg.shape[0])
                    cv2.resizeWindow(
                        'WHISTLE MEME', mimg.shape[1], mimg.shape[0])
                    cv2.moveWindow('WHISTLE MEME', x, y)

                    # process the music
                    music_path = FFP.FBW('Josh Hutcherson whistle.mp3')
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play()

                    while True:
                        m_start_time = cv2.getTickCount()
                        ret, video_img = meme_cap.read()
                        if ret:
                            cv2.imshow('WHISTLE MEME', video_img)
                        else:
                            cv2.destroyWindow('WHISTLE MEME')
                            pygame.mixer.music.stop()
                            break

                        # fixed period
                        m_end_time = cv2.getTickCount()
                        elapse_time = (m_end_time-m_start_time) / \
                            cv2.getTickFrequency()
                        if elapse_time < delay:
                            # transfer to millisecond
                            cv2.waitKey(int((delay-elapse_time)*1000))

        if pygame.mixer.music.get_busy():
            print('00000')

        pressed_key = cv2.waitKey(3)
        if pressed_key == ord('q') or pressed_key == ord('Q') or pressed_key == 27:
            break     # 按下q鍵或ESC停止

        # fixed period
        end_time = cv2.getTickCount()
        elapse_time = (end_time-start_time)/cv2.getTickFrequency()
        if elapse_time < delay:
            # transfer to millisecond
            cv2.waitKey(int((delay-elapse_time)*1000))


cap.release()
pygame.quit()
cv2.destroyAllWindows()
