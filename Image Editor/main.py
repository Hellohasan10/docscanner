from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory,  jsonify
from your_image_processing_module import remove_background
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'processed/'


# video bg remover route 
@app.route('/remove-video-bg', methods=['GET', 'POST'])
def remove_video_background():
    if request.method == 'POST':
        return jsonify({'status': 'processing', 'message': 'Video is being processed'})
    return render_template('remove_video_background.html')


# routes
@app.route('/remove-background', methods=['GET', 'POST'])
def remove_background_view():
    if request.method == 'POST':

        if 'imageFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['imageFile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            output_filename = remove_background(file_path)

            return send_from_directory(app.config['PROCESSED_FOLDER'], output_filename, as_attachment=True)

    return render_template('remove_background.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# feedback. 
from feedback import feedback_bp

app = Flask(__name__)

app.register_blueprint(feedback_bp)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/remove_bg")
def remove_bg():
    return render_template("remove_bg.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/how")
def how():
    return render_template("how.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        operation = request.form.get("operation")

        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
        
    return render_template("index.html")

app.run(debug=True, port=5001)