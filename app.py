from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            if image_file.filename != "":
                # Save the uploaded image
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
                image_file.save(image_path)
                
                # Perform OCR on the saved image
                with Image.open(image_path) as img:
                    text = pytesseract.image_to_string(img)
                
                # Optionally, delete the image after processing
                os.remove(image_path)
                
                # Return the extracted text as a JSON response
                return jsonify({"text": text})
    
    # Render the HTML template on GET request
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
