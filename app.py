from flask import Flask, request, render_template
import os
import face_recognition

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')

@app.post("/upload")
def upload_images():
    # Create an images folder if it does not exist
    path = "images"
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir(os.path.join(os.curdir, path))
   
    unknownImage = request.files.get('unknownImage')
    knownImage = request.files.get('knownImage')

    # Save images to images folder
    unknownImage.save(os.path.join(os.curdir, 'images/unknownImage.jpg'))
    knownImage.save(os.path.join(os.curdir, 'images/knownImage.jpg'))

    # Face recognition
    unknown_image = face_recognition.load_image_file("images/unknownImage.jpg")
    known_image = face_recognition.load_image_file("images/knownImage.jpg")
    initial_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces([initial_encoding], unknown_encoding)

    # Delete image files after
    os.remove(os.path.join(os.curdir, 'images/unknownImage.jpg'))
    os.remove(os.path.join(os.curdir, 'images/knownImage.jpg'))

    # results = [True] or [False]
    if results[0] == True:
        return "Same person"
    else:
        return "Different person"