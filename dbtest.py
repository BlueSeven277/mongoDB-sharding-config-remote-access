from pymongo import MongoClient
import datetime
class dbOperator:

    def __init__(self):
        #connect to database 
        # client = MongoClient("mongodb://{user}:{password}@{host}:{port}/{database}")
        self.client = MongoClient("mongodb://rosie:mypwd@10.10.10.xx:27017/test")
        self.db = self.client.test
        try: self.db.command("serverStatus")
        except Exception as e: print(e)
        else: print("You are connected!")

    # def create_collection(self, collection_name):
    #     collection = self.db.collection_name
    #     collist = self.db.list_collection_names()
    #     if collection_name in collist:
    #         print("The collection exists.")
    #         print(collist)
    #     return collection_name
    def create_collection(self, collection_name):
        collection = self.db[collection_name]
        collist = self.db.list_collection_names()
        if collection_name in collist:
            print("The collection exists.")
            print(collist)
        return collection_name

    def insert_to_collection(self, collestion_name, data):
        return self.db[collestion_name].insert_many(data).acknowledged
    def delete_from_collection(self, collection_name, query):
        return self.db[collection_name].delete_many(query).acknowledged
    def query_from_collection(self, collection_name, query):
        return self.db[collection_name].find(query)
    def update_from_collection(self, collection_name, query, newvalue):
        return self.db[collection_name].update_many(query, newvalue).acknowledged


if __name__ == '__main__':
    operator = dbOperator()
    mycollection = "stressTest"
    operator.create_collection(mycollection)
    
    mylist = [
  { "date": datetime.datetime.now(),"name": "Amy", "address": "Apple st 652"},
  { "date": datetime.datetime.now(),"name": "Hannah", "address": "Mountain 21"},
  { "date": datetime.datetime.now(),"name": "Michael", "address": "Valley 345"},
  { "date": datetime.datetime.now(),"name": "Sandy", "address": "Ocean blvd 2"},
  { "date": datetime.datetime.now(),"name": "Betty", "address": "Green Grass 1"},
  { "date": datetime.datetime.now(),"name": "Richard", "address": "Sky st 331"},
  { "date": datetime.datetime.now(),"name": "Susan", "address": "One way 98"},
  { "date": datetime.datetime.now(),"name": "Vicky", "address": "Yellow Garden 2"},
  { "date": datetime.datetime.now(),"name": "Ben", "address": "Park Lane 38"},
  { "date": datetime.datetime.now(),"name": "William", "address": "Central st 954"},
  { "date": datetime.datetime.now(),"name": "Chuck", "address": "Main Road 989"},
  { "date": datetime.datetime.now(),"name": "Viola", "address": "Sideway 1633"}
]
    data = [{"date": datetime.datetime.now(),"name": "Lisaadaa", "address": "Sideway 1690"}]
    
    # insert
    result = operator.insert_to_collection(mycollection, data)
    print(result)
    
    '''
    # delete
    myquery = { "address": {"$regex": "^S"} }
    operator.delete_from_collection(mycollection, myquery)
    mydoc = operator.db.test_collection.find(myquery)
    '''

    '''
    # update
    updatequery = { "address": { "$regex": "^O" } }
    newvalues = { "$set": { "name": "Minnie" } }
    operator.update_from_collection(mycollection, updatequery, newvalues)
    

    # query
    queryc = { "name": { "$gt": "M" } }
    mydoc = operator.query_from_collection(mycollection, queryc)

    for x in mydoc:
        print(x)
    '''
    operator.client.close()
   



