import cv2
from CV_Engine.detection.face_detector import FaceDetector

def get_eye_centers(eyes):
    centers = []
    for (ex, ey, ew, eh) in eyes:
        cx = ex + ew // 2
        cy = ey + eh // 2
        centers.append((cx, cy))
    return centers

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    detector = FaceDetector()

    total_frames = 0
    eye_contact_frames = 0

    prev_centers = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))

        faces, gray = detector.detect_faces(frame)

        eye_contact = False

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            face_gray = gray[y:y+h, x:x+w]
            face_color = frame[y:y+h, x:x+w]

            eyes = detector.detect_eyes(face_gray)

            if len(eyes) >= 2:
                centers = get_eye_centers(eyes)

                if prev_centers is not None and len(prev_centers) == len(centers):
                    movement = 0
                    for (cx, cy), (px, py) in zip(centers, prev_centers):
                        movement += abs(cx - px) + abs(cy - py)

                    # Threshold for gaze stability
                    if movement < 20:
                        eye_contact = True

                prev_centers = centers

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

        total_frames += 1
        if eye_contact:
            eye_contact_frames += 1

        ratio = eye_contact_frames / total_frames if total_frames else 0

        status = f"Eye Contact Score: {int(ratio * 100)}%"
        state = "Eye Contact" if eye_contact else "Looking Away"

        cv2.putText(frame, status, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, state, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

        cv2.imshow("Interview Monitor", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()