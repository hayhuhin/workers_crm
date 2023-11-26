
from pymongo.mongo_client import MongoClient


uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"





class MongoDBConstructor:
    """class that connecting to the local mongodb and perform CRUD operations 
        with a help of methods that checking the users record permission
    """
    def __init__(self,uri:str,db_name:str):

        #this is the connection to the db server
        self.client = MongoClient(uri)

        self.db_name = db_name

        #this is the specific db 
        self.db = self.client[self.db_name]

        self.db_gr_query = self.db["gr"]
        

    def user_permission_records(self,user):
        #this method will check this users permission level and decide how much records the user can have


        #TODO add logic later to handle the permission records

        #testing phase - will return small number 
        return 7

    def switch_records(self,collection_name:str,user:str,current_graph_id,requested_position):
        """ this method gets the users current record position and id and switching the places of the records positions.
            example:user_ben :{
                                record_1:data,
                                record_2:data,
                                record_3:data,
                                }
            each record placed in the same order as it will be represented in the web so 
            to change the position we need to take for example record_3 and switch it with 1-
            record_3 puts himself like this:
            record_3:data,
            record_2:data,
            record_1:data
            and add another key and value of the graph position in the web
        """
        self.collection_name = collection_name
        query_filter = {"user_name":user} #query filter to get the data of the specific user

        #this is the current graph position and the current graph id
        src_graph_position_cursor = self.db.get_collection(self.collection_name).find(query_filter,{f"graph_records.records.{current_graph_id}.position":1})
        for graph_data in src_graph_position_cursor:
            src_graph_position = (graph_data["graph_records"]["records"][str(current_graph_id)]["position"])
        src_graph_id = current_graph_id

        user_collection_records = self.db.get_collection(self.collection_name).find(query_filter,{"graph_records.records":1})


        user_records_position = []
        for cursor in user_collection_records:

            for records in  cursor["graph_records"]["records"]:
                user_records_position.append(cursor["graph_records"]["records"][records]["position"])



        available_positions = user_records_position
        if requested_position not in available_positions:
            #! need to add some response to the user 
            raise Exception("invalid position requested ")

        else:
            #this changes the current graph id to the requested graph position
            src_record_change = {
            "$set": {
                f"graph_records.records.{src_graph_id}.position":requested_position
            }}
            # self.db.get_collection(self.collection_name).update_one(query_filter,src_record_change)


            #this changes the requested graph position to the current (switching the current and the requested places)
            dst_graph_position = requested_position
            dst_graph_id = self.find_graphID_by_position(collection_name=collection_name,user=user,position_value=requested_position)
            dst_record_change = {
                "$set":{
                    f"graph_records.records.{dst_graph_id}.position":int(src_graph_position)
                }
            }

            #this two lines are updating the database with the new positions
            self.db.get_collection(self.collection_name).update_one(query_filter,dst_record_change)
            self.db.get_collection(self.collection_name).update_one(query_filter,src_record_change)



    def find_graphID_by_position(self,collection_name:str,user:str,position_value):
        """this method will search the graph id by its position value inside each graph
            it does a loop that iterates over the graph records(max graph records for now is 7)
            the complexity is a o(n+1)
            the 2 because it have nested for loop tha iterates only once and then enters the second for loop 
        """
        self.collection_name = collection_name
        query_user_filter = {"user_name":user}
        
        # Construct the query
        query = {
            "graph_records.records":1
        }

        # Execute the query
        result = self.db_gr_query.find(query_user_filter,query)

        #first for loop loops only twice over the mongodb cursor object
        for items in result:

            #here it iterates over the dict and searching for the graph id by the matching position value
            for record_id in items["graph_records"]["records"]:
                if items["graph_records"]["records"][record_id]["position"] == position_value:
                    found_id = record_id
                    return found_id


                # else:
                #     print(items["graph_records"]["records"][record_id]["position"])
            

        # for i in aggregated_data:
        #     print(i)
    
    def export_csv_data(self,collection_name:str,user:str,graph_id):
        """this method returns the specific data needed to be exported the by the user """
        user_filter = {"user_name":user}
        projection = {f"graph_records.records.{graph_id}":1,"_id":0}

        records_projection = self.db_gr_query.find(user_filter,projection)

# [['Column 1', 'Column 2'], ['Value 1', 'Value 2']]

        titles = []
        content = []
        for data in records_projection:
            titles.append((data["graph_records"]["records"][str(graph_id)]).keys())
            content.append((data["graph_records"]["records"][str(graph_id)]).values())

        return list(titles[0]),list(content[0])
        # return titles,content


    # def import_csv_record(self,csv_data:dict):
    #     for keys in csv_data:



    def edit_record(self,collection_name:str,user,record_id:str,new_data:dict):
        self.collection_name = collection_name
        query = {"user_name": user}
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]
        query_filter = {"user_name":user} #query filter to get the data of the specific user


        #the format of the new data
        new_record_query = {
            "$set":{
                f"graph_records.records.{record_id}":new_data
            }
        }

        result = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)
        print(f"record: {record_id} is updated successfully")


    def add_record(self,max_record_amount,collection_name:str,new_record:dict,user:str,many_records=False):
        """ add method that creates collection if doesnt exists and writes 
            data into the collection
        """
        self.collection_name = collection_name

        query = {"user_name": user}
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]


        #this gives me the option to see the keys of the graph_records.records
        # print("*********************************")
        # print(list(self.db.get_collection(self.collection_name).find(query, projection).sort(sort))[0]["graph_records"]["records"])
        # print(len((list(self.db.get_collection(self.collection_name).find(query, projection).sort(sort))[0]["graph_records"]["records"])))
        # print("*********************************")
        records = list(self.db.get_collection(self.collection_name).find(query, projection).sort(sort))[0]["graph_records"]["records"]

        #this checking the users permission and its record capacity approved
        #and return integer of the records approved
        self.capacity_approved = max_record_amount


        if len(records) >= self.capacity_approved:
            max_record_exceded_message = f"you exceded the maximum records in the user. your maximum is: {self.capacity_approved}"
            # raise Exception()
            print(max_record_exceded_message)
            return max_record_exceded_message
        

        if len(records) ==  0:

            #the new record that will be created
            new_record_name = "0"
            

            #bellow section is responsible for formating the new record 


            query_filter = {"user_name":user} #query filter to get the data of the specific user



            #if its new record so its the first graph position
            position = 1

            #its the first time that the user dont have records it will create record number
            # and a graph_position that shows us where it represented in the web-page
            # position_data = {"$set":{"graph_records.position":position}}
            # #this is the query to the mongodb database to add the position key and value
            # self.db.get_collection(self.collection_name).update_one(query_filter,position_data)
            new_record['position'] = position



            #the format of the new data
            new_record_query = {
                "$set":{
                    f"graph_records.records.{new_record_name}":new_record,
                }
            }

            #the final result that will save the added record in the mongo db database
            final = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)

            print(f"the record is added successfully. record number : {new_record_name}")
 

        
        else:#this section is if the user already have records in the database 


            #the record that saved last in the db
            prev_record = list(records)[-1]

            #the new record that will be created
            new_record_name = str(int(prev_record)+1)

            #the position will always be len(records) + 1 besause the add graph will be added to the end
            #of the page by default
            position = len(records)+1
            # user_filter = {"user_name":user}
            # position_data = {"$set":{"graph_records.position":position}}
            # self.db.get_collection(self.collection_name).update_one(user_filter,position_data)
            new_record["position"] = position
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

            print(f"the record is added successfully. record number : {new_record_name}")



    def user_all_records(self,user,collection_name,return_int=True):
        self.collection_name = collection_name

        query = {"user_name": user}
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]
        if list(self.db.get_collection(self.collection_name).find(query,projection)):
            records = list(self.db.get_collection(self.collection_name).find(query, projection).sort(sort))[0]["graph_records"]["records"]

            if return_int:
                return len(records)
            
            else:
                return records
        else:
            records = []
            return records


    def remove_records(self,collection_name:str,user:str,record_number:str,delete_all=False):
        """this method can remove records with the record number"""

        self.collection_name = collection_name

        query_filter = {"user_name":user} #query filter to get the data of the specific user

        #this to see the amount of records and check if the record exists
        projection = {"graph_records.records": 1, "_id": 0}
        sort = [("graph_records.records", 1)]
        # [0]["graph_records"]["records"]
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
                        f"graph_records.records.{record_number}":1,
                    },

                }

            #the final result that will save the added record in the mongo db database
                final = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)
                

        if delete_all:

            for record_number in records:
                print(f"record deleted :{record_number}")

                new_record_query = {
                "$unset":{
                    # f"graph_records.records.{record_number}":1,
                    "graph_records":""
                },}

                final = self.db.get_collection(self.collection_name).delete_one({"user_name":user})
                # final = self.db.get_collection(self.collection_name).update_one(query_filter,new_record_query)
        
        


    def user_exists(self,collection_name:str,user:str):
        query_filter = {
            "user_name":user
        }
        user_found = list(self.db.get_collection(collection_name).find(query_filter))
        
        #if user exists
        #! important that ill add another validation that the users exists but without the record and it will add the record
        if user_found:
            #if user have the records

            # records_found = list(self.db.get_collection(collection_name).find(query_filter{"graph_records":""}))
            # print(records_found)
            # if records_found:
            return True
            # else:
            #     new_user_data = {
            #     "user_name":user,
            #     "graph_records" : {
                    
            #     }
            # }
            #     new_user_data_insertion = self.db.get_collection(collection_name).insert_one(new_user_data)
            #     new_user_data_insertion = f"{new_user_data} inserted into the mongodb"
            #     return new_user_data_insertion

        
        if not user_found:

            new_user_data = {
                "user_name":user,
                "graph_records" : {"records":{}
                    
                }
            }
            new_user_data_insertion = self.db.get_collection(collection_name).insert_one(new_user_data)
            new_user_data_insertion = f"{new_user_data} inserted into the mongodb"
            return new_user_data_insertion



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

        records_amount = 0

        # Execute the query
        
        if record_count == 0:
            return None

        records_amount = len(list(collection.find(query, projection).sort(sort))[0]["graph_records"]["records"])

 
        #validating that the record count is not higher or smaller then the amount of records
        if record_count > records_amount or record_count <= 0:

            print(f"you inserted {record_count} and this user has only {records_amount} records . please insert a valid number")
            return None

        else:

            #! need to add check statment that if the user trying to switch the current position to position that doesnt exists
            pipe_line = [
    {
        "$match": {"user_name": user_name}
    },
    {
        "$project": {
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
    },
    {
        "$unwind": "$lastrecords"
    },
    {
        "$sort": {
            "lastrecords.v.position": 1  # Sort by the keys (assuming they are strings representing numbers)
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "user_name": {"$first": "$user_name"},
            "lastrecords": {"$push": "$lastrecords"}
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



test_class = MongoDBConstructor(uri,"test")
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