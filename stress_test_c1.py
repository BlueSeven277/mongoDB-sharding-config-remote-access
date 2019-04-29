import dbtest
import datetime
import random
import pymongo
from multiprocessing.dummy import Pool as ThreadPool 
import time
from bson import ObjectId

record = 1
thread = 50

def bulk_operation(robotid):
    # testdata = [{"a":"a", "b":"b","c":"c","d":"d","e":"e","f":"f","g":"g", "h":"h", "i":"i","j":"j","k":"k","l":"l","m":"m", "n":"n","o":"o",
    # "p":"p","q":"q", "r":"r","s":"s","t":"t", "u":robotid }]  # 102 byte
    db = dbtest.dbOperator().db
    for i in range(record):
        #testdata = [{"date": datetime.datetime.now(),"a": "b","t":"t", "u":robotid}]
        testdata = [{"_id": ObjectId(), "robotId": robotid, "task":"T003", "date": datetime.datetime.now()}]
        # testdata[0]["_id"] = ObjectId()
        db["stressTest2"].insert_many(testdata)

        # try:
        #     db.insert_to_collection("stressTest2", testdata)
        # except pymongo.errors.BulkWriteError as bwe:
        #     print(bwe.details)
        #     print(i)
        #     break
        


if __name__ == '__main__':
    pool = ThreadPool(thread) 
    my = ["ri" ,"r2","r3","r4"]
    my_array = ["r1","r2","r3","r4","r5","r6","r7","r8","r9","r10",
    "r11","r12","r13","r14","r15","r16","r17","r18","r19","r20",
    "r21","r22","r23","r24","r25","r26","r27","r28","r29","r30",
    "r31","r32","r33","r34","r35","r36","r37","r38","r39","r40",
    "r41","r42","r43","r44","r45","r46","r47","r48","r49","r50"
    ]
    curr_time = time.time()
    results = pool.map(bulk_operation, my_array)
    print(time.time()-curr_time)
    print("when using " + str(thread) + " threads and " + str(record) + " record for each")
    # op = dbtest.dbOperator()
    # collection = "stressTest2"
    # mylist = [{ "date":str( datetime.datetime.now()) + str(random.randint(0,10000)),"name": "Lily", "address": "Mountain 21"},
    # {"date":str(datetime.datetime.now())  + str(random.randint(0,10000)),"name": "Liz", "address": "Mountain 22"}
   
    # ]
    testdata = [{"a":"a", "b":"b","c":"c","d":"d","e":"e","f":"f","g":"g", "h":"h", "i":"i","j":"j","k":"k","l":"l","m":"m", "n":"n","o":"o",
    "p":"p","q":"q", "r":"r","s":"s","t":"t", "u":"u", "v":"v"}]  # 102 byte
    # for i in range(25):
    #     try: 
    #         #print(op.insert_to_collection(collection, mylist))
    #         print(op.insert_to_collection("stressTest2", [{ "data": str(i)}]))
    #     except pymongo.errors.BulkWriteError as bwe:
    #         print(bwe.details)
    #         continue
    #     print(op.update_from_collection(collection,  { "data": "1"}, { "$set": { "data": "Testname" } } ))
    #     print(op.query_from_collection(collection,  { "data": { "$regex": "^T" } }))
    #     print(op.delete_from_collection(collection, { "data": { "$regex": "^T" }}))

    
    