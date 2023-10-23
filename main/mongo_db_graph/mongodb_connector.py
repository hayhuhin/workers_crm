
from pymongo.mongo_client import MongoClient


uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"

# # Create a new client and connect to the server
client = MongoClient(uri)
db = client["test"]

j = "gr"

# col = db[j]
# col.find({})
# # Send a ping to confirm a successful connection
# # try:
# #     client.admin.command('ping')
# #     print("Pinged your deployment. You successfully connected to MongoDB!")
# # except Exception as e:
# #     print(e)



# #in the future will be connected to the cloud or vps server

# #this is a simple beta test for handling the nosql data

# db = client["test"]

# #1.find the user

# result = db.gr.find({"user_name":"vala"})

# for res in result:
#     #getting the graph records
#     records = res["graph_records"]["records"]

#     #getting the last update of the graph
#     last = list(records)[-1]

#     #the last update:
#     last_record = records[last]




class mongodb_constructor:
    def __init__(self,uri:str,db_name:str):

        #this is the connection to the db server
        self.client = MongoClient(uri)

        self.db_name = db_name

        #this is the specific db 
        self.db = self.client[self.db_name]
        

    def write_data(self,collection_name:str,write_data):
        """ write method that creates collection if doesnt exists and writes 
            data into the collection
        """
        self.collection_name = collection_name
        self.db.get_collection(name=self.collection_name).insert_many(write_data)

        print("the data is inserted into the collection")

    
    def find_data(self,collection_name:str,data):
        self.collection_name = collection_name

        self.quered_data = self.db.get_collection(self.collection_name)

        find_result = self.quered_data.find(data)

        return find_result



test_class = mongodb_constructor(uri,"test")


my_data = [
    {
        "name":"vala",
        "l_name":"lev",
        "age":25,
        "data":{
            "1":[1,2,3,4],
            "2":[0,9,8,7]
        }
    }
]

# test_class.create_collection(collection_name="gaga",data=my_data)
r = {}
res22 = test_class.find_data(collection_name="gr",data=r)


my_new_data = [{
    "user_id":"2",
    "user_name":"ben",
    "graph_records" : {
        "records":{
            "1000":{
                "created_at":"YYYY-MM-DD",
                "x":[1,2,3,4,5],
                "y":["a","b","c","d","e"]
            },
            "1001":{
                "created_at":"YYYY-MM-DD",
                "x":[1,2,3,4,5],
                "y":["a","b","c","d","e"]
            },
            "1002":{
                "created_at":"YYYY-MM-DD",
                "x":[1,2,3,4,5],
                "y":["a","b","c","d","e"]
            }
        }
    }
}]



# test_class.write_data(collection_name="gr",write_data=my_new_data)

# res = test_class.find_data("gr",{})

# for i in res:
#     print(i)
# # for k in res22:
# #     print(k) 
