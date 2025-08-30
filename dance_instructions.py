import cv2
from utils import speak, calculate_angle
import numpy as np

# Helper to draw a stick man in a given pose
# pose: 'neutral', 'hand_up', 'bend_knee', 'step_left', 'rotate_hand', 'rotate_body'
def draw_stickman(pose='neutral', size=300, expression='neutral', cymbals=False):
    img = np.ones((size, size, 3), dtype=np.uint8) * 255  # white background
    # Proportions
    center_x = size // 2
    pelvis_y = size // 2 + 40
    head_radius = 28
    neck_len = 18
    body_len = 60
    shoulder_width = 54
    hip_width = 36
    upper_arm = 38
    lower_arm = 38
    upper_leg = 44
    lower_leg = 44
    # Keypoints
    head_center = (center_x, pelvis_y - body_len - neck_len - head_radius)
    neck = (center_x, pelvis_y - body_len - neck_len)
    left_shoulder = (center_x - shoulder_width//2, pelvis_y - body_len - neck_len)
    right_shoulder = (center_x + shoulder_width//2, pelvis_y - body_len - neck_len)
    left_hip = (center_x - hip_width//2, pelvis_y)
    right_hip = (center_x + hip_width//2, pelvis_y)
    pelvis = (center_x, pelvis_y)
    # Bhajan-specific poses
    if pose == 'bhajan_foot_tap_left':
        # Left foot tap, hands down
        right_elbow = (right_shoulder[0] + upper_arm//2, right_shoulder[1] + upper_arm)
        right_wrist = (right_elbow[0] + lower_arm//2, right_elbow[1] + lower_arm//2)
        left_elbow = (left_shoulder[0] - upper_arm//2, left_shoulder[1] + upper_arm)
        left_wrist = (left_elbow[0] - lower_arm//2, left_elbow[1] + lower_arm//2)
        right_knee = (right_hip[0], right_hip[1] + upper_leg)
        right_ankle = (right_knee[0], right_knee[1] + lower_leg)
        left_knee = (left_hip[0] - 10, left_hip[1] + upper_leg)
        left_ankle = (left_knee[0] - 10, left_knee[1] + lower_leg//2)
    elif pose == 'bhajan_foot_tap_right':
        # Right foot tap, hands down
        right_elbow = (right_shoulder[0] + upper_arm//2, right_shoulder[1] + upper_arm)
        right_wrist = (right_elbow[0] + lower_arm//2, right_elbow[1] + lower_arm//2)
        left_elbow = (left_shoulder[0] - upper_arm//2, left_shoulder[1] + upper_arm)
        left_wrist = (left_elbow[0] - lower_arm//2, left_elbow[1] + lower_arm//2)
        left_knee = (left_hip[0], left_hip[1] + upper_leg)
        left_ankle = (left_knee[0], left_knee[1] + lower_leg)
        right_knee = (right_hip[0] + 10, right_hip[1] + upper_leg)
        right_ankle = (right_knee[0] + 10, right_knee[1] + lower_leg//2)
    elif pose == 'bhajan_prayer':
        # Hands together in prayer, feet neutral
        right_elbow = (center_x + 10, neck[1] + 30)
        right_wrist = (center_x + 5, neck[1] + 60)
        left_elbow = (center_x - 10, neck[1] + 30)
        left_wrist = (center_x - 5, neck[1] + 60)
        right_knee = (right_hip[0], right_hip[1] + upper_leg)
        right_ankle = (right_knee[0], right_knee[1] + lower_leg)
        left_knee = (left_hip[0], left_hip[1] + upper_leg)
        left_ankle = (left_knee[0], left_knee[1] + lower_leg)
    elif pose == 'bhajan_clap':
        # Hands together, feet neutral, cymbals if True
        right_elbow = (center_x + 10, neck[1] + 30)
        right_wrist = (center_x + 5, neck[1] + 60)
        left_elbow = (center_x - 10, neck[1] + 30)
        left_wrist = (center_x - 5, neck[1] + 60)
        right_knee = (right_hip[0], right_hip[1] + upper_leg)
        right_ankle = (right_knee[0], right_knee[1] + lower_leg)
        left_knee = (left_hip[0], left_hip[1] + upper_leg)
        left_ankle = (left_knee[0], left_knee[1] + lower_leg)
    else:
        # Default neutral
        right_elbow = (right_shoulder[0] + upper_arm//2, right_shoulder[1] + upper_arm)
        right_wrist = (right_elbow[0] + lower_arm//2, right_elbow[1] + lower_arm//2)
        left_elbow = (left_shoulder[0] - upper_arm//2, left_shoulder[1] + upper_arm)
        left_wrist = (left_elbow[0] - lower_arm//2, left_elbow[1] + lower_arm//2)
        right_knee = (right_hip[0], right_hip[1] + upper_leg)
        right_ankle = (right_knee[0], right_knee[1] + lower_leg)
        left_knee = (left_hip[0], left_hip[1] + upper_leg)
        left_ankle = (left_knee[0], left_knee[1] + lower_leg)
    # For rotate_body, tilt torso
    if pose == 'rotate_body':
        torso_shift = 24
        neck = (neck[0] + torso_shift, neck[1])
        right_shoulder = (right_shoulder[0] + torso_shift, right_shoulder[1])
        left_shoulder = (left_shoulder[0] + torso_shift, left_shoulder[1])
        pelvis = (pelvis[0] + torso_shift, pelvis[1])
        right_hip = (right_hip[0] + torso_shift, right_hip[1])
        left_hip = (left_hip[0] + torso_shift, left_hip[1])
    # Draw head
    cv2.circle(img, head_center, head_radius, (0,0,0), 3)
    # Draw smile or serene face
    if expression == 'smile':
        cv2.ellipse(img, (head_center[0], head_center[1]+10), (12,6), 0, 0, 180, (0,0,0), 2)
    elif expression == 'closed':
        cv2.line(img, (head_center[0]-10, head_center[1]), (head_center[0]+10, head_center[1]), (0,0,0), 2)
    # Draw body
    cv2.line(img, neck, pelvis, (0,0,0), 4)
    # Draw shoulders and hips
    cv2.line(img, left_shoulder, right_shoulder, (0,0,0), 3)
    cv2.line(img, left_hip, right_hip, (0,0,0), 3)
    # Draw arms
    cv2.line(img, right_shoulder, right_elbow, (0,0,0), 4)
    cv2.line(img, right_elbow, right_wrist, (0,0,0), 4)
    cv2.line(img, left_shoulder, left_elbow, (0,0,0), 4)
    cv2.line(img, left_elbow, left_wrist, (0,0,0), 4)
    # Draw legs
    cv2.line(img, right_hip, right_knee, (0,0,0), 4)
    cv2.line(img, right_knee, right_ankle, (0,0,0), 4)
    cv2.line(img, left_hip, left_knee, (0,0,0), 4)
    cv2.line(img, left_knee, left_ankle, (0,0,0), 4)
    # Draw joints
    for pt in [neck, left_shoulder, right_shoulder, left_hip, right_hip, right_elbow, right_wrist, left_elbow, left_wrist, right_knee, right_ankle, left_knee, left_ankle]:
        cv2.circle(img, (int(pt[0]), int(pt[1])), 7, (80,80,80), -1)
    # Draw cymbals if needed
    if cymbals and pose == 'bhajan_clap':
        cv2.circle(img, (right_wrist[0], right_wrist[1]), 12, (0,215,255), -1)
        cv2.circle(img, (left_wrist[0], left_wrist[1]), 12, (0,215,255), -1)
    return img


def give_instructions(results, frame, style='default'):
    """
    Takes pose results and frame, checks moves,
    gives voice feedback only (no on-screen instructions).
    style: dance style (e.g., 'bhajan', 'bollywood', 'bhojpuri', 'pop', 'hiphop')
    Returns: (annotated_frame, stickman_img, step_status)
    step_status: 'right' if correct step, else 'wrong'
    """
    pose = 'neutral'
    step_status = 'wrong'
    if not results.pose_landmarks:
        return frame, draw_stickman(pose), step_status

    landmarks = results.pose_landmarks.landmark

    # Bhajan style: prioritize both hands up and rotate hand
    if style == 'bhajan':
        right_wrist = landmarks[16]
        right_shoulder = landmarks[12]
        right_elbow = landmarks[14]
        left_wrist = landmarks[15]
        left_shoulder = landmarks[11]
        left_elbow = landmarks[13]
        # Both hands up
        if right_wrist.y < right_shoulder.y and left_wrist.y < left_shoulder.y:
            speak(f"Bhajan: Raise both hands up")
            pose = 'hand_up'
            step_status = 'right'
        # Either hand rotates
        elif (right_wrist.y < right_elbow.y and abs(right_wrist.x - right_elbow.x) > 0.1) or (left_wrist.y < left_elbow.y and abs(left_wrist.x - left_elbow.x) > 0.1):
            speak(f"Bhajan: Rotate your hand")
            pose = 'rotate_hand'
            step_status = 'right'
        else:
            pose = 'neutral'
            step_status = 'wrong'
        return frame, draw_stickman(pose), step_status

    # ---- Step 1: Raise right hand ----
    right_wrist = landmarks[16]
    right_shoulder = landmarks[12]
    if right_wrist.y < right_shoulder.y:  # hand higher than shoulder
        speak(f"Step one, raise your hand up for {style}")
        pose = 'hand_up'
        step_status = 'right'

    # ---- Step 2: Bend right knee ----
    hip = landmarks[24]
    knee = landmarks[26]
    ankle = landmarks[28]
    knee_angle = calculate_angle(hip, knee, ankle)
    if knee_angle < 120:  # bent knee
        speak(f"Step two, bend your knee for {style}")
        pose = 'bend_knee'
        step_status = 'right'

    # ---- Step 3: Step left ----
    left_ankle = landmarks[27]
    left_hip = landmarks[23]
    if left_ankle.x < left_hip.x - 0.1:  # step left
        speak(f"Step three, step to the left for {style}")
        pose = 'step_left'
        step_status = 'right'

    # ---- Step 4: Rotate right hand ----
    right_elbow = landmarks[14]
    if right_wrist.y < right_elbow.y and abs(right_wrist.x - right_elbow.x) > 0.1:
        speak(f"Step four, rotate your hand for {style}")
        pose = 'rotate_hand'
        step_status = 'right'

    # ---- Step 5: Rotate body ----
    left_shoulder = landmarks[11]
    if abs(right_shoulder.x - left_shoulder.x) > 0.4:  # shoulders far apart horizontally
        speak(f"Step five, rotate your body for {style}")
        pose = 'rotate_body'
        step_status = 'right'

    return frame, draw_stickman(pose), step_status
