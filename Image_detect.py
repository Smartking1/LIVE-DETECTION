import cv2
from PIL import Image
import pytesseract
import sqlite3
import os

# Connect to the SQLite database
conn = sqlite3.connect('extracted_info.db')
cursor = conn.cursor()

# Create a table to store the extracted text
cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_text (
                    id INTEGER PRIMARY KEY,
                    text TEXT
                )''')

def extract_info_with_opencv(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    x, y, w, h = cv2.boundingRect(contours[0])
    photo = image[y:y+h, x:x+w]
    photo_image = Image.fromarray(cv2.cvtColor(photo, cv2.COLOR_BGR2RGB))
    save_folder = 'extracted_photos'
    os.makedirs(save_folder, exist_ok=True)
    photo_filename = os.path.join(save_folder, 'extracted_photo.jpg')
    photo_image.save(photo_filename)
    text = pytesseract.image_to_string(image)

    # Store the extracted text in the database
    cursor.execute("INSERT INTO extracted_text (text) VALUES (?)", (text,))
    conn.commit()
    
    return text, photo_image




# Example usage:
image_path = r"C:\Users\Laptop\Downloads\OCRA\LIVE-DETECTION\testcard.jpeg"
text_opencv, photo_opencv = extract_info_with_opencv(image_path)


# Print extracted text and display photo
print("Text extracted using OpenCV:", text_opencv)
photo_opencv.show()
