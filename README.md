# EyeSpy-Software-Team
Repository for EyeSpy software team. 

### Dependencies
 - Python
 - Flask
 - opencv
 - pymongo 

 "pip install ___"

### Project Description

 - Drone built fully from scratch with facial recognition capabilities.
 -- ESP32 Camera - > RTSP Stream - > Facial Recognition 
 - Web application to notify system/user when the facial recognition software sees an intruder.
 - User database for web application.
 - Secondary database for intruder faces. Quick comparison to faces on stream.

 ###
 - 11/26 work on facial recognition scripts, pushed 11/27
 - 11/17 implement buttons to run scripts on web app
    -- intended flow:
    -- login -> click capture images -> enter name of face on app -> create/train model -> run facial recognition on camera
    -- current flow: click capture image -> user is prompted to enter name on the terminal? -> create/train model -> run facial recognition
- need to organize the facial data. images are being dumped in faces/name as #.jpg (0.jpg) where as we want name1.jpg and so on. the yml and pickle files are also being dumped in the app directory. need to figure out how to dump them all in the faces folder.


 
