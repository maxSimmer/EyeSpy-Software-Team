import os
import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import pickle

# Create necessary folders
if not os.path.exists('faces'):
    os.makedirs('faces')

def draw_bounding_boxes(frame, recognizer, face_cascade, labels):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45:  # Confidence threshold
            name = labels.get(id_, "Unknown")
            cv2.putText(frame, f"{name} {round(conf, 2)}%", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return frame

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    if not os.path.exists("trainer.yml"):
        print("Error: trainer.yml file not found.")
        return
    
    recognizer.read("trainer.yml")

    labels = {}
    try:
        with open("labels.pickle", "rb") as f:
            og_labels = pickle.load(f)
            labels = {v:k for k,v in og_labels.items()}
    except FileNotFoundError:
        print("Error: labels.pickle file not found.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    root = tk.Tk()
    root.title("Webcam Stream")
    label = Label(root)
    label.pack()

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = draw_bounding_boxes(frame, recognizer, face_cascade, labels)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(10, update_frame)

    update_frame()
    root.mainloop()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()