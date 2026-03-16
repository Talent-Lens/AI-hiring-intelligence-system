import cv2
import time
from CV_Engine.detection.face_detector import FaceDetector

def get_eye_centers(eyes):
    centers = []
    for (ex, ey, ew, eh) in eyes:
        cx = ex + ew // 2
        cy = ey + eh // 2
        centers.append((cx, cy))
    return centers

def analyze_camera(question,duration=20):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    detector = FaceDetector()

    total_frames = 0
    eye_contact_frames = 0
    correct_predictions=0

    prev_centers = None
    start_time = time.time()
    while True:
        if time.time() - start_time > duration:
            break
        ret, frame = cap.read()
        eye_detected = False
        frame = cv2.resize(frame, (640, 480))

        faces, gray = detector.detect_faces(frame)

        eye_contact = False
        contact_count=0
        forward_count = 0
        left_count = 0
        right_count = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            eye_mid = 0
            face_gray = gray[y:y+h, x:x+w]
            face_color = frame[y:y+h, x:x+w]

            eyes = detector.detect_eyes(face_gray)
            centers=get_eye_centers(eyes)

            if len(centers) == 2:

                eye_mid = (centers[0][0] + centers[1][0]) // 2
                face_center_x = w // 2

                diff = eye_mid - face_center_x

                if diff>15:
                    posture = "Looking Right"
                    right_count+=1
                elif diff<-15:
                    posture = "Looking Left"
                    left_count+=1
                else:
                    posture = "Forward"
                    forward_count+=1
                cv2.putText(frame, posture, (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if len(eyes) > 0:
                eye_detected = True


            eye_contact=False
            contact_count = 0
            for(ex,ey,ew,eh) in eyes:
                
                eye_region=face_gray[ey:ey+eh, ex:ex+ew]
                eye_color_region=face_color[ey:ey+eh, ex:ex+ew]

                
                # Improve contrast
                eye_region = cv2.equalizeHist(eye_region)
                
                #preprocess blur
                blur= cv2.GaussianBlur(eye_region, (7,7), 0)

                #Threshold for dark pupil
                _, thresh=cv2.threshold(blur,40,255, cv2.THRESH_BINARY_INV)

                contours,_= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                if contours:
                    largest_contour= None
                    max_area=0

                    for cnt in contours:
                        area=cv2.contourArea(cnt)

                        if 30<area<(ew*eh*0.3):
                            if area>max_area:
                                max_area=area
                                largest_contour=cnt
                    if largest_contour is not None:
                        if cv2.contourArea(largest_contour)>50:
                            (px,py,pw,ph)=cv2.boundingRect(largest_contour)

                            pupil_center_x=px+pw//2
                            pupil_center_y=py+ph//2
                            #draw pupil box
                            cv2.rectangle(eye_color_region,(px,py),
                                        (px+pw, py+ph), (0,0,255),1)
                            
                            #Eye center
                            eye_center_x=ew//2
                            eye_center_y=eh//2

                            #Check horizontal position
                            if abs(pupil_center_x - eye_center_x)<ew * 0.15 and abs(pupil_center_y - eye_center_y)<eh * 0.15:
                                contact_count += 1
        if contact_count >=1:
            eye_contact = True
        else:
            eye_contact = False
        
        
        total_frames+=1
        
        if not eye_detected:
            eye_contact=False
        
        if eye_contact:
            eye_contact_frames += 1

        
        ratio = (eye_contact_frames / total_frames)*100 if total_frames else 0
        total_count=forward_count+left_count+right_count
        forward_posture_percentage = (forward_count / total_count) * 100 if total_count else 0
        
        status = f"Eye Contact Score: {int(ratio)}%"
        state = "Eye Contact" if eye_contact else "Looking Away"

        cv2.putText(frame, status, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, state, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

        cv2.putText(frame, f"Question: {question}", (20, 440),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        
        cv2.imshow("Interview Monitor", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    confidence_score = (
        0.7 * ratio +
        0.3 * forward_posture_percentage
)

    cap.release()
    cv2.destroyAllWindows()

    return {
    "eye_contact_score": ratio,
    "head_posture_score": forward_posture_percentage,
    "confidence_score": confidence_score
}

if __name__ == "__main__":
    result= analyze_camera()
    print(result)