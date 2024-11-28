import cv2
import os
import time

def capture_faces(name):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    if not os.path.exists(f'faces/{name}'):
        os.makedirs(f'faces/{name}')

    count = 0
    while count < 10:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            cv2.imwrite(f'faces/{name}/{count}.jpg', roi_gray)
            count += 1

        cv2.imshow('Capturing Faces', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(2.5)  # Wait for 5 seconds before capturing the next image

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    name = input("Enter the name of the person: ")
    capture_faces(name)