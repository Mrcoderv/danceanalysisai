import cv2
import mediapipe as mp
import csv
import time
import threading
from playsound import playsound
import numpy as np
import json
import os

frame_interval = 1/30  # 30 FPS
import json
import os

import dance_instructions as di
# ---- Load beat data ----
if not os.path.exists("beat_data.json"):
    print("No beat_data.json found. Please run beat_analyzer.py first.")
    exit()
with open("beat_data.json", "r") as f:
    beat_data = json.load(f)

SONG_FILE = beat_data["song"]
tempo = beat_data["tempo"]
beats = beat_data["beats"]
style = beat_data["style"]
print(f"Loaded beat data for style: {style}, song: {SONG_FILE}")
print(f"Detected Tempo: {tempo:.2f} BPM")
print(f"Total Beats: {len(beats)}")

# ---- Play music (using pygame) ----
import pygame
def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

music_thread = threading.Thread(target=play_music, args=(SONG_FILE,), daemon=True)
music_thread.start()

# ---- MediaPipe Pose ----
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# ---- Webcam ----
cap = cv2.VideoCapture(0)

# ---- CSV Save ----

# ---- Animation and tracking loop ----
with open("dance_tracking_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    headers = ["frame"]
    for i in range(33):
        headers += [f"x_{i}", f"y_{i}", f"z_{i}", f"visibility_{i}"]
    writer.writerow(headers)

    frame_count = 0
    start_time = time.time()
    beat_idx = 0
    last_beat_time = 0
    stickman_beat_pose = 0

    print(f"Press 1-5 to change dance style during session (visual only): bhajan, bollywood, bhojpuri, pop, hiphop")

    while True:
        loop_start = time.time()
        ret, frame = cap.read()
        if not ret:
            h, w = 480, 640
            frame = np.zeros((h, w, 3), dtype=np.uint8)

        frame_count += 1
        elapsed = time.time() - start_time

        # ---- Beat sync check ----
        on_beat = False
        if beat_idx < len(beats) and abs(elapsed - beats[beat_idx]) < 0.2:
            on_beat = True
            last_beat_time = elapsed
            stickman_beat_pose = (stickman_beat_pose + 1) % 4
            beat_idx += 1

        if on_beat:
            cv2.putText(frame, "🎵 On Beat! 🎵", (200, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        row = [frame_count]
        if ret and results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:
                row += [lm.x, lm.y, lm.z, lm.visibility]

            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=4, circle_radius=6),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=4),
            )

            frame, _, step_status = di.give_instructions(results, frame, style)
        else:
            row += [None] * (33 * 4)
            step_status = 'wrong'

        style_pose_cycles = {
            'bhajan': [
                ('bhajan_foot_tap_left', 'smile', False),
                ('bhajan_foot_tap_right', 'smile', False),
                ('bhajan_prayer', 'closed', False),
                ('bhajan_clap', 'smile', True)
            ],
            'bollywood': [
                ('hand_up', 'smile', False),
                ('step_left', 'smile', False),
                ('bend_knee', 'smile', False),
                ('rotate_hand', 'smile', False)
            ],
            'bhojpuri': [
                ('step_left', 'smile', False),
                ('bend_knee', 'smile', False),
                ('hand_up', 'smile', False),
                ('rotate_body', 'smile', False)
            ],
            'pop': [
                ('hand_up', 'smile', False),
                ('rotate_hand', 'smile', False),
                ('step_left', 'smile', False),
                ('neutral', 'smile', False)
            ],
            'hiphop': [
                ('bend_knee', 'smile', False),
                ('rotate_body', 'smile', False),
                ('hand_up', 'smile', False),
                ('neutral', 'smile', False)
            ]
        }
        poses = style_pose_cycles.get(style, [('neutral', 'smile', False)])
        pose_name, expression, cymbals = poses[stickman_beat_pose % len(poses)]
        stickman_img = di.draw_stickman(pose_name, expression=expression, cymbals=cymbals)
        h, w, _ = frame.shape
        stickman_img_resized = cv2.resize(stickman_img, (h, h))
        combined = cv2.hconcat([frame, stickman_img_resized])

        bulb_radius = 40
        bulb_color = (0, 255, 0) if step_status == 'right' else (0, 0, 255)
        bulb_center = (combined.shape[1] // 2, bulb_radius + 10)
        cv2.circle(combined, bulb_center, bulb_radius, bulb_color, -1)
        cv2.circle(combined, bulb_center, bulb_radius, (200, 200, 200), 4)
        cv2.circle(combined, (bulb_center[0] - 12, bulb_center[1] - 12), 10, (255,255,255), -1)

        import ctypes
        user32 = ctypes.windll.user32
        screen_w, screen_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        scale_width = screen_w / combined.shape[1]
        scale_height = screen_h / combined.shape[0]
        scale = min(scale_width, scale_height, 1.0)
        window_w = int(combined.shape[1] * scale)
        window_h = int(combined.shape[0] * scale)
        combined_resized = cv2.resize(combined, (window_w, window_h))

        bg = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
        y_offset = (screen_h - window_h) // 2
        x_offset = (screen_w - window_w) // 2
        bg[y_offset:y_offset+window_h, x_offset:x_offset+window_w] = combined_resized

        cv2.imshow("Dance Pose Tutor with Beat Sync", bg)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if 49 <= key <= 49 + 4:
            style_idx = key - 49
            style = ['bhajan', 'bollywood', 'bhojpuri', 'pop', 'hiphop'][style_idx]
            print(f"Switched to style: {style}")

        # Maintain frame rate
        elapsed_loop = time.time() - loop_start
        if elapsed_loop < frame_interval:
            time.sleep(frame_interval - elapsed_loop)

    cap.release()
    cv2.destroyAllWindows()
    # Do not stop or join music_thread; let it finish naturally

print(f"Tracking finished. Data saved in 'dance_tracking_data.csv'. Frames: {frame_count}")
