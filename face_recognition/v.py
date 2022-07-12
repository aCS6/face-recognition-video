# https://www.youtube.com/playlist?list=PLUm4moMlPhOqjuKECVdSCJqLHHkD32K7k

import face_recognition
import cv2
import numpy as np

import requests
response = requests.get("http://192.168.1.100:2023/node/face")
# print(response.json())

image_list = []
name_list = []

for i in response.json():
    image_list.append(i['imgfile'])
    name_list.append(i['name'])

video_capture = cv2.VideoCapture(2)

known_face_encodings = []

for i in image_list:
    loaded_img = face_recognition.load_image_file(i)
    encode = face_recognition.face_encodings(loaded_img)[0]
    known_face_encodings.append(encode)

'''
img1 = face_recognition.load_image_file("s2.jpeg")
img1_encode = face_recognition.face_encodings(img1)[0]


img2 = face_recognition.load_image_file("h2.jpg")
img2_encode = face_recognition.face_encodings(img2)[0]


known_face_encodings = [
    img1_encode,
    img2_encode
]
'''

known_face_names = name_list



while True:
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    print(face_locations)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
