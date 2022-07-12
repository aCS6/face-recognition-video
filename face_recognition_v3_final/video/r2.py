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

            face_names = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    break
                
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
            
                # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(e)
            break
        
        if name is not None:
          break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    if name is not None:
      return name
    else:
      return "Failed"

print(Recognise('11_45_48am'))
