import cv2
import mediapipe as mp
from flask import Response
from fer import FER

# Inisialisasi detector FER dan MediaPipe Pose
detector = FER()
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Variabel global untuk menyimpan emosi dan status duduk terakhir
last_emotion = None
is_sitting = False

def generate_frames():
    global last_emotion, is_sitting  # Akses variabel global
    camera = cv2.VideoCapture(0)  # Ganti 0 dengan path video jika menggunakan file video
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Deteksi ekspresi wajah
            emotions = detector.detect_emotions(frame)
            if emotions:
                # Ambil emosi yang paling dominan
                last_emotion = max(emotions[0]['emotions'], key=emotions[0]['emotions'].get)

            # Pose Detection
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                # Logika sederhana untuk deteksi duduk (berdasarkan posisi pinggul dan lutut)
                hip_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
                knee_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y
                if hip_y < knee_y:
                    is_sitting = True
                else:
                    is_sitting = False

                # Tampilkan status duduk di video
                status = "Sitting" if is_sitting else "Not Sitting"
                cv2.putText(frame, f"Status: {status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Tampilkan emosi di video
            cv2.putText(frame, f"Emotion: {last_emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Mengubah gambar ke format JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Mengembalikan frame sebagai streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
