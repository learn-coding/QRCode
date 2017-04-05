from flask import *
from flask_restful import reqparse, Resource
#import werkzeug

from core import Core


class DropTable(Resource):
    # curl cmd : curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8888/qrcode/droptable
    def __init__(self):
        pass

    def get(self):
        Core.get_instance().drop_product_table()
        Core.get_instance().drop_coupon_table()
        return 200
