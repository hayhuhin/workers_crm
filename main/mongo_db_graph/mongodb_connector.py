
from pymongo.mongo_client import MongoClient


uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"





class mongodb_constructor:
    """class that connecting to the local mongodb and perform CRUD operations 
        with a help of methods that checking the users record permission
    """
    def __init__(self,uri:str,db_name:str):

        #this is the connection to the db server
        self.client = MongoClient(uri)

        self.db_name = db_name

        #this is the specific db 
        self.db = self.client[self.db_name]

        

    def user_permission_records(self,user):
        #this method will check this users permission level and decide how much records the user can have


        #TODO add logic later to handle the permission records

        #testing phase - will return small number 
        return 7


    def add_record(self,max_record_amount,collection_name:str,new_record:dict,user:str,many_records=False):
        """ add method that creates collection if doesnt exists and writes 
            data into the collection
        """
        self.collection_name = collection_name



        query = {"user_name": user}
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]


        #this gives me the option to see the keys of the graph_records.records
        records = list(self.db.get_collection(self.collection_name).find(query, projection).sort(sort))[0]["graph_records"]["records"]

        #this checking the users permission and its record capacity approved
        #and return integer of the records approved
        self.capacity_approved = max_record_amount
        print(len(records))


        if len(records) >= self.capacity_approved:
            max_record_exceded_message = f"you exceded the maximum records in the user. your maximum is: {self.capacity_approved}"
            # raise Exception()
            print(max_record_exceded_message)
            return max_record_exceded_message
        

        if len(records) ==  0:

            #the new record that will be created
            new_record_name = "000"

            #bellow section is responsible for formating the new record 

            query_filter = {"user_name":user} #query filter to get the data of the specific user

            #the format of the new data
            new_record_query = {
                "$set":{
                    f"graph_records.records.{new_record_name}":new_record
                }
            }

            #the final result that will save the added record in the mongo db database
            final = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)
            print(new_record_query)
            print(f"the record is added successfully. record number : {new_record_name}")
 

        else:


            #the record that saved last in the db
            prev_record = list(records)[-1]

            #the new record that will be created
            new_record_name = str(int(prev_record)+1)



            #bellow section is responsible for formating the new record 

            query_filter = {"user_name":user} #query filter to get the data of the specific user

            #the format of the new data
            new_record_query = {
                "$set":{
                    f"graph_records.records.{new_record_name}":new_record
                }
            }

            #the final result that will save the added record in the mongo db database
            final = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)
            print(new_record_query)
            print(f"the record is added successfully. record number : {new_record_name}")



    def user_all_records(self,user,collection_name,return_int=True):
        self.collection_name = collection_name

        query = {"user_name": user}
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]

        records = list(self.db.get_collection(self.collection_name).find(query, projection).sort(sort))[0]["graph_records"]["records"]

        if return_int:
            return len(records)
        else:
            return records

    def remove_records(self,collection_name:str,user:str,record_number:str,delete_all=False):
        """this method can remove records with the record number"""

        self.collection_name = collection_name

        query_filter = {"user_name":user} #query filter to get the data of the specific user

        #this to see the amount of records and check if the record exists
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]
        records = list(self.db.get_collection(self.collection_name).find(query_filter, projection).sort(sort))[0]["graph_records"]["records"]

        if delete_all == False:
        #this checking if the records exists or not        
            if record_number not in records.keys():
                print("this record is wrong ")
                print(f"this is the records : {records.keys()}")

            else:

            #the format of the new data
                new_record_query = {
                    "$unset":{
                        f"graph_records.records.{record_number}":1
                    },

                }

            #the final result that will save the added record in the mongo db database
                final = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)

        if delete_all:

            for record_number in records:
                print(f"record deleted :{record_number}")

                new_record_query = {
                "$unset":{
                    f"graph_records.records.{record_number}":1
                },}

                final = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)
        
        




    def find_data(self,collection_name:str,data):
        """thid method is for testing or checking the data 
            the syntax is the same as with pymongo querying
        """

        self.collection_name = collection_name

        self.quered_data = self.db.get_collection(self.collection_name)

        find_result = self.quered_data.find(data)

        print("\n\nfind result ******************")
        print("\n{}".format(find_result[0]))
        print("\nfind result ********************")

    


    def get_record(self,collection_name:str,user_name:str,record_count=2):
        """method should return specific users x,y records of the graph
            ARGS:
                collection_name:the mongo db collection name as a string
                user_name:the specific user that we want to extract record from
                record_count:how many records to extract from the new to old .

            return:
                returns list of dicts with the records number as a key and the x and y as a value
                with a date data.
        """

        collection = self.db[collection_name]

        # Define the query, projection, and sort
        query = {"user_name": user_name}
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]

        # Execute the query
        records_amount = len(list(collection.find(query, projection).sort(sort))[0]["graph_records"]["records"])

        #validating that the record count is not higher or smaller then the amount of records
        if record_count > records_amount or record_count <= 0:
            print(f"you inserted {record_count} and this user has only {records_amount} records . please insert a valid number")
            return None

        else:
            pipe_line = [
                        {
                            "$match": {"user_name": user_name}},
                            {"$project": {
                                "user_name": 1,
                                "lastrecords": {
                                    "$slice": [
                                        {
                                            "$map": {
                                                "input": {"$objectToArray": "$graph_records.records"},
                                                "as": "record",
                                                "in": {
                                                    "k": "$$record.k",
                                                    "v": "$$record.v"
                                                }
                                            }
                                        },
                                        -record_count
                                    ]
                                }
                            }
                        }
                        ]
            

            aggregated_data = self.db.gr.aggregate(pipeline=pipe_line)

            # return aggregated_data
            for items in aggregated_data:
                return items["lastrecords"]






################### testing stages below ######################


my_new_data = [{
    "user_id":"3",
    "user_name":"david",
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



test_class = mongodb_constructor(uri,"test")
# add_record_test = test_class.extract_record("gr","david",2)



test_dict = {
    "created_at":"YYYY-MM-DD",
    "x":[1,1,1,1],
    "y":["q","w","e","r"]
}


#checking if the add record working - done
# add_record_test = test_class.add_record(collection_name="gr",user="ben",new_record=test_dict,many_records=False)

#checking the delete record method - done
# del_record_test = test_class.remove_records(collection_name="gr",user="david",record_number="1006")

#checking the get_record method - done
# get_record_test = test_class.get_record(collection_name="gr",user_name="david",record_count=1)

#checking the find_record method - done
# test_class.find_data(collection_name="gr",data={"user_name":"david"})





# test_class.remove_records(collection_name="gr",user="ben",record_number="1")