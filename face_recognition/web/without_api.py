from flask import Flask, render_template, Response
import os
import requests
import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime



app = Flask(__name__)


# Images for training
image_list = ['image3.png','image4.png','image5.jpeg']

# Names for Labeling
name_list = ['Nahid','Salman','Rubayet']


# Student List for attendance
attendance  = []

# attendance In time list
times = []


# reload the browser when app starts .. It would open camera
if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    video_capture = cv2.VideoCapture(2)

# Taking the face landmark (encoding)
known_face_encodings = []

for i in image_list:
    loaded_img = face_recognition.load_image_file(i)
    encode = face_recognition.face_encodings(loaded_img)[0]
    known_face_encodings.append(encode)


known_face_names = name_list

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():  
    while True:
        success, frame = video_capture.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                if name != 'Unknown' and name not in attendance:
                    attendance.append(name)
                    times.append(datetime.now().strftime("%H:%M:%S"))

                # file for attendance
                file = open('attendance.csv', 'w', newline ='')
                with file:
                    # identifying header  
                    header = ['Roll','Name', 'Time']
                    writer = csv.DictWriter(file, fieldnames = header)
                      
                    # writing data row-wise into the csv file
                    writer.writeheader()

                    for i in range(len(attendance)):
                        writer.writerow({
                            'Roll': i+1,
                            'Name' : attendance[i], 
                            'Time': times[i]})

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)

