import os

from flask import *
from flask_restful import Api

from qr_code import QRCode
from werkzeug.utils import secure_filename

qrc = Flask(__name__)
api = Api(qrc)
qrc.config['ERROR_404_HELP'] = False
UPLOAD_FOLDER = '/home/msys/'
qrc.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

qrc.secret_key = "amvobyul$%#!@"

api.add_resource(QRCode, '/qrcode') #, '/qrcode/upload')

@qrc.route("/")
def hello():
    return "Hello World!"
	
'''
@qrc.route('/qrcode/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "file not found"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "no selected file"
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(qrc.config['UPLOAD_FOLDER'], filename))
            return "FIle successfully uploaded"
    return 200
'''

if __name__ == "__main__":
    qrc.run("10.0.2.15", port=8888, debug=True)


