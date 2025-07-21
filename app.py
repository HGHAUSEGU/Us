import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Configuration for the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads/'
UPLOAD_FOLDER_BTS = 'static/uploadsbts/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_BTS'] = UPLOAD_FOLDER_BTS

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/main')
def main():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('mainpage.html', images=images)
@app.route('/main2')
def main2():
    images = os.listdir(app.config['UPLOAD_FOLDER_BTS'])
    return render_template('mainpage copy.html', images=images)
@app.route('/')
def index():
    # Get the list of images from the uploads folder
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty part without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main'))
    return render_template('upload.html')


@app.route('/upload2', methods=['GET', 'POST'])
def upload_file2():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty part without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER_BTS'], filename))
            return redirect(url_for('main2'))
    return render_template('upload copy.html')
@app.route('/uploads/<filename>')

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploadsbts/<filename>')
def uploaded_file2(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_BTS'], filename)


@app.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('main'))
@app.route('/delete2/<filename>', methods=['POST'])
def delete_image2(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER_BTS'],filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('main2'))
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('static/uploadsbts', exist_ok=True)
if __name__ == '__main__':
    app.run(debug=True)