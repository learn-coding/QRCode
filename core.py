import random
from database import MongoDB


class Core(object):

    instance = None

    def __init__(self):
        pass
		
    @staticmethod	
    def get_instance():
        if not Core.instance:
            Core.instance = Core()
        return Core.instance

    def create_random(self, number):
        id = ''.join(random.choice('0123456789ABCDEF') for i in range(number))
        #self.create_data_packet(id)
        return id

    #def create_data_packet(self, info):
        #self.write_to_db(info)        

    def write_data_to_product_db(self, info):
        MongoDB().write_to_product_collection(info)

    def read_data_from_product_db(self, id=None):
        flag = 0
        print "id = ",id
        if not id:
            return MongoDB().read_from_product_collection()
        else:
            for data_entry in MongoDB().read_from_product_collection():
                if id in data_entry.values():
                    print "data_entry = ", data_entry
                    reqd_data = data_entry
                    flag = 1
            if flag == 1:
                del reqd_data['_id']
                return reqd_data
            else:
                return 'Data not available'

    def drop_product_table(self):
        MongoDB().drop_product_collection()

    def write_data_to_coupon_db(self, info):
        MongoDB().write_to_coupon_collection(info)

    def read_data_from_coupon_db(self, id=None):
        flag = 0
        print "id = ",id
        if not id:
            return MongoDB().read_from_coupon_collection()
        else:
            for data_entry in MongoDB().read_from_coupon_collection():
                if id in data_entry.values():
                    print "data_entry = ", data_entry
                    reqd_data = data_entry
                    flag = 1
            if flag == 1:
                del reqd_data['_id']
                return reqd_data
            else:
                return 'Data not available'

    def drop_coupon_table(self):
        MongoDB().drop_coupon_collection()
'''		
    def read_data_from_product_db(self, data):
        flag = 0
        for data_entry in MongoDB().read_from_product_collection():
            if data in data_entry.values():
                #return data_entry
                reqd_data = data_entry
                flag = 1
        if flag == 1:
            del reqd_data['_id']
            return reqd_data
        else:
            return 'Data not available'
'''

