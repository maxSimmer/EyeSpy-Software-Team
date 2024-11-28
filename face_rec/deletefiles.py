import os
import shutil

# Define the paths to the files and folder
labels_pickle_path = 'labels.pickle'
trainer_yml_path = 'trainer.yml'
faces_folder_path = 'faces'

# Delete labels.pickle if it exists
if os.path.exists(labels_pickle_path):
    os.remove(labels_pickle_path)
    print(f"Deleted {labels_pickle_path}")

# Delete trainer.yml if it exists
if os.path.exists(trainer_yml_path):
    os.remove(trainer_yml_path)
    print(f"Deleted {trainer_yml_path}")

# Delete all folders in faces
if os.path.exists(faces_folder_path) and os.path.isdir(faces_folder_path):
    for item in os.listdir(faces_folder_path):
        item_path = os.path.join(faces_folder_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted folder {item_path}")