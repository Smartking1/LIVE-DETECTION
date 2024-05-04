import cv2
import numpy as np
import face_recognition
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('faces.db')
cursor = conn.cursor()

# Retrieve stored face images from the database
cursor.execute("SELECT image FROM face_images")
known_faces_data = cursor.fetchall()
known_face_encodings = [np.frombuffer(data[0], dtype=np.uint8) for data in known_faces_data]
conn.close()

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Find face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(img_rgb)
    face_encodings = face_recognition.face_encodings(img_rgb, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Compare face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)

        if any(matches):
            # Draw rectangle around the face region
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            # Print message if faces match
            print("Ahoy! The faces matched")

    # Display the resulting frame
    cv2.imshow('Face Recognition', img)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()

