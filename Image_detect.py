import cv2
from PIL import Image
import pytesseract

def extract_info_with_opencv(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    x, y, w, h = cv2.boundingRect(contours[0])
    photo = image[y:y+h, x:x+w]
    photo_image = Image.fromarray(photo)
    text = pytesseract.image_to_string(photo_image)
    return text, photo_image

# Example usage:
image_path = "ID_Storage/photo_2024-05-03_22-18-29.jpg"
text_opencv, photo_opencv = extract_info_with_opencv(image_path)

# Print extracted text and display photo
print("Text extracted using OpenCV:", text_opencv)
photo_opencv.show()
