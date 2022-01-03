import os
import os.path
import random
import string
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'files/'
HOST = 'https://upload.tuxli.ch'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_filename(secure):
    if secure:
        digits = 50
    else:
        digits = 4
    random_name = ''.join(random.choices(string.ascii_letters, k=digits))
    if os.path.exists(f'{UPLOAD_FOLDER}{random_name}'):
        print("duplicate detected!")
        return generate_filename(secure)
    return random_name


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        generated_name = generate_filename(request.form.get('secure'))
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{generated_name}{extension}'))
        return f'{HOST}/files/{generated_name}{extension}/{filename}\n'


@app.route('/', methods=['GET'])
def upload_form():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post action=/upload enctype=multipart/form-data>
    Secure Filename?  <input type="checkbox" value="true" name="secure"><br>
      <input type=file name=file><br>
      <input type=submit value=Upload>
    </form>
    '''
