def Recognise(file_name):
    # print(file_name)
    import cv2
    import face_recognition
    import numpy as np
    # Images for training
    image_list = [
        'faces/nahid.png',
        'faces/fahim.png',
        'faces/jisan.png',
        'faces/rubayet.jpeg',
        'faces/salman.jpeg',
        'faces/rahat.jpg',
    ]

    # Names for Labeling
    name_list = ['Nahid','Fahim','Jisan','Rubayet','Salman','Rahat']

    # Taking the face landmark (encoding)
    known_face_encodings = []

    for i in image_list:
        loaded_img = face_recognition.load_image_file(i)
        encode = face_recognition.face_encodings(loaded_img)[0]
        known_face_encodings.append(encode)


    known_face_names = name_list
    
    try:
        video_capture = cv2.VideoCapture(file_name)
    except Exception as e:
        print(e)

    name = None

    while True:
        ret, frame = video_capture.read()
        
        try:
            rgb_frame = frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    break
        except:
            pass
        
        if name is not None:
          break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    if name is not None:
      return name
    else:
      return "Failed"
