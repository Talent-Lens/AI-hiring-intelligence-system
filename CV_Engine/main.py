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
    correct_predictions=0

    prev_centers = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        eye_detected = False
        frame = cv2.resize(frame, (640, 480))

        faces, gray = detector.detect_faces(frame)

        eye_contact = False

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            face_gray = gray[y:y+h, x:x+w]
            face_color = frame[y:y+h, x:x+w]

            eyes = detector.detect_eyes(face_gray)

            if len(eyes) > 0:
                eye_detected = True


            eye_contact=False
            
            for(ex,ey,ew,eh) in eyes:
                contact_count = 0
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
                            if abs(pupil_center_x - eye_center_x)<ew * 0.12 and abs(pupil_center_y - eye_center_y)<eh * 0.12:
                                contact_count += 1
        if contact_count >=1:
            eye_contact = True
        else:
            eye_contact = False
        
        ground_truth = True

        total_frames+=1
        
        if not eye_detected:
            eye_contact=False

        if eye_contact == ground_truth:
                correct_predictions += 1
        
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
    if total_frames > 0:
        accuracy = (correct_predictions / total_frames) * 100
        print("Final Accuracy:", accuracy)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()