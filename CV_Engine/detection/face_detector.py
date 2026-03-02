import cv2
import os

class FaceDetector:
    def __init__(self):
        base_path = os.path.dirname(__file__)

        face_path = os.path.join(base_path, "haarcascade_frontalface_default.xml")
        eye_path = os.path.join(base_path, "haarcascade_eye.xml")

        self.face_cascade = cv2.CascadeClassifier(face_path)
        self.eye_cascade = cv2.CascadeClassifier(eye_path)

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        return faces, gray

    def detect_eyes(self, gray_face_region):
        eyes = self.eye_cascade.detectMultiScale(
            gray_face_region,
            scaleFactor=1.1,
            minNeighbors=5
        )

        return eyes