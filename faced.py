import cv2
import numpy as np
import face_recognition
import os

# Load the image extracted from the ID card
extracted_image_path = r'C:\Users\hp\Live Detection\LIVE-DETECTION\extracted_photos\extracted_photo.jpg'
extracted_image = face_recognition.load_image_file(extracted_image_path)
extracted_face_encoding = face_recognition.face_encodings(extracted_image)[0]

# Initialize the VideoCapture object for the laptop camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    # Convert the frame to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Find face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(img_rgb)
    face_encodings = face_recognition.face_encodings(img_rgb, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Compare face encoding with the extracted face encoding
        match = face_recognition.compare_faces([extracted_face_encoding], face_encoding)[0]

        # If a match is found, display a message
        if match:
            cv2.putText(img, 'Ahoy! Faces match', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(img, 'Faces don\'t match', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Draw a rectangle around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0) if match else (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', img)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
