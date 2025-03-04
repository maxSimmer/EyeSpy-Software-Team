
import os
import cv2
import numpy as np
from PIL import Image
import pickle

def train_recognizer():
    base_dir = 'faces'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace(" ", "-").lower()
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]

                pil_image = Image.open(path).convert("L")
                image_array = np.array(pil_image, "uint8")
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)

    with open("labels.pickle", "wb") as f:
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainer.yml")

if __name__ == "__main__":
    train_recognizer()