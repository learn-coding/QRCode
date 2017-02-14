import qrcode
import qrtools
import os

from flask import *
from flask_restful import reqparse, Resource
#import werkzeug
from login import loginRequired
from werkzeug.utils import secure_filename

from core import Core

postargs = reqparse.RequestParser()

postargs.add_argument('sex', type=str, required=True)
postargs.add_argument('name', type=str, required=True)
postargs.add_argument('age', type=int, required=True)

class QRCode(Resource):

  def __init__(self):
    pass
	
  @loginRequired
  def get(self):
    #curl cmd : curl -i -X GET -H "Content-Type: multipart/form-data" -F "file=@F:/QRCode/filename.png" http://127.0.0.1:8888/qrcode
    #curl cmd : curl -i -X GET -H "Content-Type: multipart/form-data" -F "file=@F:/QRCode/filename.png" --cookie "token=WyJcIjQ2MDg2NzlGQTBBODdBMkRcIiJd.C38kOw.Q8_VfKndp2WTuLWIjT93lzTHAJY" http://127.0.0.1:8888/qrcode
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
        from server import qrc
        filepath = os.path.join(qrc.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        #return "FIle successfully uploaded"
        qr = qrtools.QR()
        qr.decode(filepath)
        id_complete_data = Core.get_instance().read_data_from_db(qr.data)
        return id_complete_data


  def post(self):
    #curl cmd : curl -i -H "Content-Type: application/json" -X POST -d "{\"name\" : \"Niladri\", \"sex\" : \"M\", \"age\" : 31}" http://127.0.0.1:8888/qrcode
    qr_info = postargs.parse_args()
    qr_info['user_id'] = Core.get_instance().create_random()
    #input = 'name: ' + 	qr_info['name'] + '\n ID: ' + str(qr_info['id'])
    #print qr_info['user_id']
    img = qrcode.make(qr_info['user_id'])
    Core.get_instance().write_data_to_db(qr_info)
    img.save("filename.png")
    msg = 'QR code created successfully' #% (poolName)
    return {'status': "true", 'message': msg}, 201





