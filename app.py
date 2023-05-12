from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import cv2
from resize_for_detection import crop
import json

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "F:/Bino/Tensorflow/models/research/object_detection/static/uploads/"
app.secret_key = 'secret123'

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'image' in request.files:
            image = request.files["image"]
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['IMAGE_UPLOADS'], filename)
            image.save(filepath)
            image = cv2.imread(filepath)
            flash('Generated Successfully!', 'success')
            crop(filepath, filename, image)
            html_file = Path(filename).stem + ".html"
            output_file_path = os.path.join("static/output", html_file)
            
            if os.path.exists(output_file_path):
                with open(output_file_path, "r") as f:
                    code = f.read()
            else:
                code = "The file does not exist"

            return render_template('home.html', display_detection=filename, fname=filename, code=code, html_file=html_file)

    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/output')
def output():
    data = []
    with open('static/json/sorted/sorted_data.json') as f:
        data = json.load(f)
    
    return render_template('output.html', len=len(data), data=data)

if __name__ == '__main__':
    app.run(debug=True)
