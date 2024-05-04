import cv2
import pytesseract
import re
<<<<<<< HEAD
#from google.colab.patches import cv2_imshow
=======
>>>>>>> f10216bad00a86ae02d7e94d9ff958b1d1ebcbff

def extract_info_from_id_card(image_path):
    image = cv2.imread(image_path)

    # Perform OCR on the entire image
    text = pytesseract.image_to_string(image)

    return text

def extract_info_from_id_card(image_path):
    image = cv2.imread(image_path)
    # Preprocessing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Face extraction
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) > 0:
        # Assuming there's only one face in the image
        (x, y, w, h) = faces[0]
        face_image = image[y:y+h, x:x+w]
    else:
        face_image = None

    return face_image


<<<<<<< HEAD
image_path = 'C:/Users/hp/Live Detection/LIVE-DETECTION/ID_Storage/photo_2024-05-03_22-18-29.jpg'
extracted_info = extract_info_from_id_card(image_path)
print(extracted_info['name'])
cv2_imshow( extracted_info['face'])
=======
image_path = r'C:\Users\Laptop\Downloads\OCRA\LIVE-DETECTION\testcard.jpeg'
extracted_image = extract_info_from_id_card(image_path)
cv2.imshow('Extracted Face', extracted_image)
>>>>>>> f10216bad00a86ae02d7e94d9ff958b1d1ebcbff
cv2.waitKey(0)
cv2.destroyAllWindows()

def extract_info_from_id_card(image_path):
    image = cv2.imread(image_path)

    # Perform OCR on the entire image
    text = pytesseract.image_to_string(image)

    return text

def extract_info_from_text(text):
    # Initialize variables to store extracted information
    extracted_info = {}

    # Split the text into lines
    lines = text.split('\n')

    # Extract name
    for line in lines:
        if 'NAME' in line:
            extracted_info['Name'] = line.split('NAME')[-1].strip()

    # Extract date of birth
    for line in lines:
        if 'DATE OF BIRTH' in line or 'DOB' in line:
            extracted_info['Date of Birth'] = line.split(':')[-1].strip()

    # Extract gender
    for line in lines:
        if 'GENDER' in line or 'SEX' in line:
            extracted_info['Gender'] = line.split(':')[-1].strip()

    # Extract occupation
    for line in lines:
        if 'OCCUPATION' in line:
            extracted_info['Occupation'] = line.split(':')[-1].strip()

    # Extract address
    address_start_index = text.find('DELIM')
    if address_start_index != -1:
        address_lines = text[address_start_index:].split('\n')[1:]
        extracted_info['Address'] = ' '.join(address_lines)

    return extracted_info

text = extract_info_from_id_card(image_path)

ttext = extract_info_from_text(text)
print(ttext)



