from pymongo import MongoClient


# Client to communicate with database
client = MongoClient()
# db refers to 'qrdb' database
db = client.qrdb


class MongoDB(object):

    def __init__(self):
        pass

    def write_to_product_collection(self, data):
        """ Write document to collection in database"""
        try:
            #print data
            result = db.collection_product.insert(data)
        except Exception as e:
            raise e

        return result


    def read_from_product_collection(self):
        """ Read document information from collection in database"""
        try:
            result = db.collection_product.find()
        except Exception as e:
            raise e
    
        return result

    def drop_product_collection(self):
        try:
            db.collection_product.drop()
        except Exception as e:
            raise e        

    def write_to_coupon_collection(self, data):
        """ Write document to collection in database"""
        try:
            #print data
            result = db.collection_coupon.insert(data)
        except Exception as e:
            raise e

        return result

    def read_from_coupon_collection(self):
        """ Read document information from collection in database"""
        try:
            result = db.collection_coupon.find()
        except Exception as e:
            raise e
    
        return result
		
    def drop_coupon_collection(self):
        try:
            db.collection_coupon.drop()
        except Exception as e:
            raise e
'''
if __name__ == "__main__":
    data = { "name": "Paras",
        "surname" : "Rajput",
        "location" : "Pune",
        "age" : "28"}
    result = write_to_db(data)
    print "Sucessfully inserted document with Object ID : %s" %result
    print "Documents in 'tutorialspoint' collection are :"
    documents = read_from_db()
    for document in documents:
        print "%s" %document

'''
