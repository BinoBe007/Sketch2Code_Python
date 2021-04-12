from flask import Flask, render_template, Response,  request, session, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from data import Articles
from resize_for_detection import crop
from pathlib import Path
import glob
import os
import cv2
import json
app = Flask(__name__)


Articles = Articles()

app.config["IMAGE_UPLOADS"] = "F:/Bino/Tensorflow/models/research/object_detection/static/uploads/"



@app.route('/', methods=["GET", "POST"])
def index():

    if request.method =="POST":
        if request.files:
            image = request.files["image"]
            #image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['IMAGE_UPLOADS'], filename)
            image.save(filepath)
            image = cv2.imread(filepath)
            #print(filename)
            flash('Generated Successfully!','success')
            #return redirect(request.url)
            #resizer(filepath, filename, image)
            crop(filepath, filename, image)
            html_file = Path(filename).stem
            html_file = html_file+".html"

            output_file_path = "static/output/"+html_file

            if os.path.exists(output_file_path):
                f = open(output_file_path, "r")
                code = f.read()
                
                #print(code)
            else:
                print("The file does not exists")

            return render_template('home.html', display_detection = filename, fname = filename, code = code, html_file=html_file)
    


    return render_template('home.html')



@app.route('/about')    
def about():
    return render_template('about.html')

@app.route('/output')    
def output():
    cc=0
    '''f = open('static/json/sorted/sorted_data.json')
    data = json.load(f)
    f.close()
    print(len(data))
    return render_template('output.html', len = len(data), data = data)'''
    #return render_template('static/output/output.html', )

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
