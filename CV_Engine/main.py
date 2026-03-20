import cv2
import numpy as np
from CV_Engine.detection.face_detector import FaceDetector

detector = FaceDetector()

# Session state stored in memory
session_data = {
    "total_frames": 0,
    "eye_contact_frames": 0,
    "forward_count": 0,
    "left_count": 0,
    "right_count": 0
}

def reset_session():
    session_data["total_frames"] = 0
    session_data["eye_contact_frames"] = 0
    session_data["forward_count"] = 0
    session_data["left_count"] = 0
    session_data["right_count"] = 0

def get_eye_centers(eyes):
    centers = []
    for (ex, ey, ew, eh) in eyes:
        cx = ex + ew // 2
        cy = ey + eh // 2
        centers.append((cx, cy))
    return centers

def analyze_frame(frame_bytes: bytes):
    """Analyze a single frame sent from the browser."""
    np_arr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"error": "Invalid frame"}

    frame = cv2.resize(frame, (640, 480))
    gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces, gray = detector.detect_faces(frame)

    eye_detected = False
    eye_contact = False
    contact_count = 0
    forward_count = 0
    left_count = 0
    right_count = 0

    for (x, y, w, h) in faces:
        face_gray = gray[y:y+h, x:x+w]
        face_color = frame[y:y+h, x:x+w]

        eyes = detector.detect_eyes(face_gray)
        centers = get_eye_centers(eyes)

        if len(centers) == 2:
            eye_mid = (centers[0][0] + centers[1][0]) // 2
            face_center_x = w // 2
            diff = eye_mid - face_center_x

            if diff > 15:
                right_count += 1
            elif diff < -15:
                left_count += 1
            else:
                forward_count += 1

        if len(eyes) > 0:
            eye_detected = True

        contact_count = 0
        for (ex, ey, ew, eh) in eyes:
            eye_region = face_gray[ey:ey+eh, ex:ex+ew]
            eye_region = cv2.equalizeHist(eye_region)
            blur = cv2.GaussianBlur(eye_region, (7, 7), 0)
            _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = None
                max_area = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if 30 < area < (ew * eh * 0.3):
                        if area > max_area:
                            max_area = area
                            largest_contour = cnt

                if largest_contour is not None:
                    if cv2.contourArea(largest_contour) > 50:
                        (px, py, pw, ph) = cv2.boundingRect(largest_contour)
                        pupil_center_x = px + pw // 2
                        pupil_center_y = py + ph // 2
                        eye_center_x = ew // 2
                        eye_center_y = eh // 2

                        if abs(pupil_center_x - eye_center_x) < ew * 0.15 and \
                           abs(pupil_center_y - eye_center_y) < eh * 0.15:
                            contact_count += 1

    if contact_count >= 1:
        eye_contact = True

    if not eye_detected:
        eye_contact = False

    # Update session
    session_data["total_frames"] += 1
    if eye_contact:
        session_data["eye_contact_frames"] += 1
    session_data["forward_count"] += forward_count
    session_data["left_count"] += left_count
    session_data["right_count"] += right_count

    return {"ok": True}

def get_final_scores():
    """Calculate final scores from session data."""
    total = session_data["total_frames"]
    eye_frames = session_data["eye_contact_frames"]
    forward = session_data["forward_count"]
    total_posture = forward + session_data["left_count"] + session_data["right_count"]

    ratio = (eye_frames / total) * 100 if total else 0
    forward_pct = (forward / total_posture) * 100 if total_posture else 0
    confidence = 0.7 * ratio + 0.3 * forward_pct

    return {
        "eye_contact_score": ratio,
        "head_posture_score": forward_pct,
        "confidence_score": confidence
    }