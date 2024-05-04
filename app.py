import streamlit as st
from Image_detect import extract_info_with_opencv
import cv2
import numpy as np
from faced import FaceDetector

def main():
    st.title('ID Card Extraction and Matching')

    # File uploader for ID card image
    st.subheader('Upload ID Card Image')
    id_card_image = st.file_uploader('Upload an image', type=['jpg', 'png'])

    if id_card_image:
        # Extract text and photo from the uploaded ID card using OpenCV
        extracted_text, extracted_photo = extract_info_with_opencv(id_card_image)
        
        # Display the extracted text
        st.subheader('Extracted Text:')
        st.write(extracted_text)

        # Display the extracted photo
        st.subheader('Extracted Photo:')
        st.image(extracted_photo, caption='Extracted Photo', use_column_width=True)

        # Initialize the face detector
        face_detector = FaceDetector()

        # Start the camera
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, img = cap.read()

            # Detect faces in the frame
            faces = face_detector.predict(img)

            # Draw rectangles around the faces
            for x, y, w, h, p in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Compare face detection with the extracted face from the ID card
                extracted_image = np.array(extracted_photo)
                extracted_face_encoding = face_detector.extract_face_features(extracted_image)
                detected_face_encoding = face_detector.extract_face_features(img[y:y+h, x:x+w])
                match = np.array_equal(extracted_face_encoding, detected_face_encoding)

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
