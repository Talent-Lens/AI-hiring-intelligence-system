import cv2
from CV_Engine.detection.face_detector import FaceDetector

def main():
    cap = cv2.VideoCapture(0)

    
    cap.set(3, 640)
    cap.set(4, 480)

    detector = FaceDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detector.detect_faces(frame)

        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Face Detection Base", frame)

        if cv2.waitKey(1) & 0xFF == 27:  
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()