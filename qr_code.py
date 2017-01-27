import qrcode
import qrtools
import os

from flask import *
from flask_restful import reqparse, Resource
#import werkzeug
from werkzeug.utils import secure_filename


postargs = reqparse.RequestParser()

postargs.add_argument('id', type=int, default=1)
postargs.add_argument('name', type=str, required=True)

class QRCode(Resource):

  def __init__(self):
    pass
	
  def get(self):
    #curl cmd : curl -i -X GET -H "Content-Type: multipart/form-data" -F "file=@F:/QR_code/filename.png" http://127.0.0.1:8888/qrcode/upload
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
        return qr.data


  def post(self):
    #curl cmd : curl --data "id=98742&name='niladri'" http://127.0.0.1:8888/qrcode
    qr_info = postargs.parse_args()
    input = 'name: ' + 	qr_info['name'] + '\n ID: ' + str(qr_info['id'])
    img = qrcode.make(input)
    img.save("filename.png")
    msg = 'QR code created successfully' #% (poolName)
    return {'status': "true", 'message': msg}, 201





