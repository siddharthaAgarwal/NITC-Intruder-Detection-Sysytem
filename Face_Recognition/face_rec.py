import csv
from datetime import datetime
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np

Path = os.path.abspath(os.path.dirname(__file__))

def get_encoded_faces():
    encoded = {}
    #to store images and encodings in a temporary array
    for dirpath, dnames, fnames in os.walk(os.path.join(Path,'faces')):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg"):
                face = fr.load_image_file(os.path.join(Path,'faces',f))
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    face = fr.load_image_file(os.path.join(Path, 'faces', img))
    encoding = fr.face_encodings(face)[0]
    return encoding

class Face(object):

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.faces = get_encoded_faces()
        self.faces_encoded = list(self.faces.values())
        self.known_face_names = list(self.faces.keys())

    def __del__(self):
        cv2.destroyAllWindows()
        self.cap.release()

    def get_frame(self):
        if not os.path.exists("Data.csv"):
            file = open("Data.csv", "a+", newline='')
            writer = csv.writer(file)
            writer.writerow(["Role", "Name", "Time"])
            file.close()
        _, frame = self.cap.read()
        face_locations = face_recognition.face_locations(frame)
        unknown_face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.faces_encoded, face_encoding)
            name = "U-OUTSIDER"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw a box around the face
                cv2.rectangle(frame, (left - 20, top - 20), (right + 20, bottom + 20), (0, 0, 0), 2)

                role = name.split('-')[0]
                if role == 'f':
                    role = 'Faculty'
                elif role == 's':
                    role = 'Student'
                else:
                    role = 'Other'
                name = name.split('-')[1]
                file = open("Data.csv", "a+", newline='')
                writer = csv.writer(file)
                writer.writerow([role, name, datetime.now()])
                file.close()
                # print('Role: {}\nName: {}'.format(role, name))
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left - 20, bottom), (right + 20, bottom + 50), (255, 255, 255), cv2.FILLED)
                font = cv2.QT_FONT_NORMAL
                cv2.putText(frame, role, (left-15, bottom+20), font, .6, (0, 0, 0))
                cv2.putText(frame, name, (left-15, bottom+40), font, .6, (0, 0, 0))

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
