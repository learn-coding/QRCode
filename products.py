from flask import *
from flask_restful import reqparse, Resource
#import werkzeug
from login import loginRequired
from werkzeug.utils import secure_filename

from core import Core

postargs = reqparse.RequestParser()

postargs.add_argument('name', type=str, required=True)
postargs.add_argument('amount', type=int, required=True)
postargs.add_argument('quantity', type=int, required=True)

class Products(Resource):
  
    def __init__(self):
        pass
	  
    def post(self):
        #curl cmd : curl -i -H "Content-Type: application/json" -X POST -d "{\"name\" : \"Coca Cola 500 mL\", \"amount\" : 60, \"quantity\" : 10}" http://127.0.0.1:8888/qrcode/products
        prdct_info = postargs.parse_args()
        prdct_info['product_id'] = Core.get_instance().create_random(5)
        Core.get_instance().write_data_to_product_db(prdct_info)
        msg = 'Product information posted successfully' #% (poolName)
        return {'status': "true", 'message': msg}, 201

    def get(self):
        #curl cmd : curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8888/qrcode/products
        product_data = Core.get_instance().read_data_from_product_db()
        datadict = {}
        datalist = []
        for data in product_data:
            #print '%s' %data
            #print data['name'],data['quantity'],data['amount'],data['product_id']
            datadict["Product name"] = data['name']
            datadict["Quantity"] = data['quantity']
            datadict["Amount"] = data['amount']
            datadict["Product_id"] = data['product_id']
            datalist.append(datadict.copy())
        return datalist


 
