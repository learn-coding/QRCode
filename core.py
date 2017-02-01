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

    def create_random(self):
        id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        #self.create_data_packet(id)
	return id
		
    #def create_data_packet(self, info):
        #self.write_to_db(info)

    def write_data_to_db(self, info):
        MongoDB().write_to_db(info)

		
    def read_data_from_db(self, data):
        flag = 0
        for data_entry in MongoDB().read_from_db():
            if data in data_entry.values():
                #return data_entry
                reqd_data = data_entry
                flag = 1
        if flag == 1:
            del reqd_data['_id']
            return reqd_data
        else:
            return 'Data not available'


