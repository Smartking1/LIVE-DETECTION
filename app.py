import streamlit as st
from Image_detect import extract_info_with_opencv, create_database
import cv2
import numpy as np


def main():
    st.title('ID Card Matching')

    # File uploader for ID card image
    st.subheader('Upload ID Card Image')
    id_card_image = st.file_uploader('Upload an image', type=['jpg', 'png'])
    conn, cursor = create_database()

    if id_card_image:
        # Extract text and photo from the uploaded ID card using OpenCV
        extracted_text, extracted_photo = extract_info_with_opencv(id_card_image,cursor, conn)
        
        # Display the extracted text
        st.subheader('Extracted Text:')
        st.write(extracted_text)

        # Display the extracted photo
        st.subheader('Extracted Photo:')
        st.image(extracted_photo, caption='Extracted Photo', use_column_width=True)
        extracted_face_encoding = face_recognition.face_encodings(extracted_photo)[0]


        # Start the camera
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
                    st.success('Ahoy! Faces match')
                else:
                    st.error('Faces don\'t match')

            # Display the resulting frame
            st.image(img, channels='BGR', use_column_width=True)

            # Break the loop when 'q' is pressed
            if st.button('Stop'):
                break

if __name__ == "__main__":
    main()
