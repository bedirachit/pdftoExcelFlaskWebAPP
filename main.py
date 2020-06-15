from flask import Flask, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
import converter
import os

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = r"C:\Users\rachit.bedi\PycharmProjects\berbardProject\uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PDF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(float(filesize)) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["file"]
                password = request.form['password']

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)

                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    print("Image saved")

                    converted_file = converter.pdf_to_csv(os.path.join(app.config["IMAGE_UPLOADS"], filename), password, (filename).split(".")[0], app.config["IMAGE_UPLOADS"])

                    return send_from_directory(app.config["IMAGE_UPLOADS"], converted_file, as_attachment=True)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

    return render_template("/public/upload_image.html")


if __name__ == "__main__":
    app.run()