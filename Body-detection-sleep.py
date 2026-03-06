import cv2
import mediapipe as mp

url = "http://172.20.10.2"

cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ Cannot connect ESP32-CAM")
    exit()

print("✅ ESP32 Connected")

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def detect_sleep_pose(landmarks, image_h):

    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    y_left = left_shoulder.y * image_h
    y_right = right_shoulder.y * image_h

    diff = abs(y_left - y_right)

    if diff < 20:
        return "Face Up/Down"
    else:
        return "Lie on Side"

while True:
    ret, frame = cap.read()

    if not ret:
        print("⚠️ Frame not received")
        break

    sleep_pose = "No detection"

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        sleep_pose = detect_sleep_pose(
            results.pose_landmarks.landmark,
            frame.shape[0]
        )

        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.putText(
        frame,
        f"Pose: {sleep_pose}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Sleep Pose Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()