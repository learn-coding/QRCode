import qrcode
import qrtools
import os
import StringIO

from flask import *
from flask_restful import reqparse, Resource
#import werkzeug
from login import loginRequired
from werkzeug.utils import secure_filename

from core import Core

postargs = reqparse.RequestParser()

postargs.add_argument('product_id', type=str, required=True)

class Coupon(Resource):

  def __init__(self):
    pass
	
  #@loginRequired
  def get(self):
    #curl cmd : curl -i -X GET -H "Content-Type: multipart/form-data" -F "file=@F:/QRCode/filename_BBDA9.png" http://127.0.0.1:8888/qrcode/coupon
    #curl cmd : curl -i -X GET -H "Content-Type: multipart/form-data" -F "file=@F:/QRCode/filename_46821.png" --cookie "token=WyJcIjQ2MDg2NzlGQTBBODdBMkRcIiJd.C38kOw.Q8_VfKndp2WTuLWIjT93lzTHAJY" http://127.0.0.1:8888/qrcode/coupon
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
        id_complete_data = Core.get_instance().read_data_from_coupon_db(qr.data)
        return id_complete_data


  def post(self):
    #curl cmd : curl -i -H "Content-Type: application/json" -X POST -d "{\"product_id\" : \"BBDA9\"}" http://127.0.0.1:8888/qrcode/coupon
    qr_info = postargs.parse_args()
    qr_info['coupon_id'] = Core.get_instance().create_random(16)
    #input = 'name: ' + 	qr_info['name'] + '\n ID: ' + str(qr_info['id'])
    #print qr_info['user_id']
    img = qrcode.make(qr_info['coupon_id'])
    #Core.get_instance().write_data_to_product_db(qr_info)
    qrcode_fn = "filename_" + qr_info['product_id'] + '.png'
    img.save(qrcode_fn)
    product_data = Core.get_instance().read_data_from_product_db(qr_info['product_id'])
    product_data['coupon_id'] = qr_info['coupon_id']
    #return product_data
    Core.get_instance().write_data_to_coupon_db(product_data)
    msg = 'Coupon information posted successfully' #% (poolName)
    return {'status': "true", 'message': msg}, 201
    #filepath = os.path.join(os.getcwd(),qrcode_fn)
    #print filepath
    #strIO = StringIO.StringIO()
    #with open(filepath, 'rb') as image_file:
        #strIO.write(image_file.read())
    #strIO.seek(0)
    #return Response(strIO,mimetype='image/png')
    #response = make_response(csv)
    #response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    #msg = 'QR code created successfully' #% (poolName)
    #return send_file(os.path.join(os.getcwd(),qrcode_fn), as_attachment=True, attachment_filename=qrcode_fn, mimetype='image/png')
    #response = make_response(os.path.join(os.getcwd(),qrcode_fn)
    #cd = 'attachment; filename=%s' %qrcode_fn
    #response.headers['Content-Disposition'] = cd 
    #response.mimetype='image/png'





