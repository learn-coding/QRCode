import os
import sys

from flask import *
from flask_restful import Api
from flask_login import current_user
from flask_login import LoginManager

from users import User

from qr_code import QRCode
from login import Login
from logout import Logout
from products import Products
from drop_table import DropTable
from coupon import Coupon

from werkzeug.utils import secure_filename

qrc = Flask(__name__)
api = Api(qrc)
qrc.config['ERROR_404_HELP'] = False
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
qrc.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

qrc.secret_key = "amvobyul$%#!@"

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(qrc)

api.add_resource(QRCode, '/qrcode') #, '/qrcode/upload')
api.add_resource(Login, '/qrcode/login')
api.add_resource(Logout, '/qrcode/logout')
api.add_resource(Products, '/qrcode/products')
api.add_resource(DropTable, '/qrcode/droptable')
api.add_resource(Coupon, '/qrcode/coupon')


@login_manager.user_loader
def load_user(qr_id):
  return User.get(qr_id)


@qrc.before_request
def before_request():
  g.user = current_user

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
    address = sys.argv[1] if len(sys.argv) > 1 else "10.0.2.15"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8888
    qrc.run(address, port=port, debug=True)


