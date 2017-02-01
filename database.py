from pymongo import MongoClient

# Client to communicate with database
client = MongoClient()
# db refers to 'qrdb' database
db = client.qrdb



class MongoDB(object):

    def __init__(self):
        pass

    def write_to_db(self, data):
        """ Write document to collection in database"""
        try:
            #print data
            result = db.qr_collection.insert(data)
        except Exception as e:
            raise e

        return result


    def read_from_db(self):
        """ Read document information from collection in database"""
        try:
            result = db.qr_collection.find()
        except Exception as e:
            raise e
    
        return result

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
