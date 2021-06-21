from flask import Flask, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import pytesseract
import pyttsx3


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("basic.html")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.files:
            if request.files['file'].filename != "":
                print(1)
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    print(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    text = pytesseract.image_to_string(img)
                    print(text)
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[0].id)
                    engine.setProperty('rate', 150)
                    engine.say(text)
                    engine.runAndWait()
    return render_template('ab.html',text=text)

if __name__== '__main__':
    app.debug = True
    app.run()