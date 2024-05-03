from flask import Flask, request, render_template, flash, redirect
from PassportEye import read_mrz
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_info(image_path):
    # Read MRZ (Machine Readable Zone) from the ID card
    mrz = read_mrz(image_path)
    
    # Extract photo from ID card
    photo = mrz.visual_data()['photo']

    # Convert the photo to a PIL Image object
    photo_image = Image.fromarray(photo)

    # Extract text using tesseract-ocr
    text = pytesseract.image_to_string(photo_image)
    
    return text, photo_image

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extracted_text, extracted_photo = extract_info(file_path)
            return render_template('result.html', text=extracted_text, photo=extracted_photo)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
