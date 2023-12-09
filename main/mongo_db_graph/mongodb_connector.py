
from pymongo.mongo_client import MongoClient
from dataclasses import dataclass,field
import json
from random import randint


@dataclass
class RecordContent:
    graph_title : str
    graph_description :str
    graph_type : str
    created_at: str
    start_date : str
    end_date : str 
    position : int 
    x : list[str,int] = field(default_factory=list)
    y : list[int] = field(default_factory=list)
    y_2 :[str,int] = field(default_factory=list)



@dataclass
class GraphRecords:
    records_id : str = field(default="0")
    records_content : RecordContent = field(default_factory=dict)



@dataclass
class UserConfig:
    name : str
    db : str
    collection : str
    graph_permited : bool
    graph_db_type : str
    graph_Records : GraphRecords = field(default_factory=dict)
    graph_repr : str = field(default="1_row")

    def to_json(self):
        return json.dumps(self.__dict__,default=lambda x:x.__dict__,indent=4)





class MongoDBConstructor:
    """
    class that connecting to the local mongo database and performing CRUD operations 
    with a help of methods and checking methods
    """
    def __init__(self,uri:str,db:str,collection:str,user:str,max_records:int):
        """
        Attributes:
            uri (str): uri to connect to the mongodb database.
            db (str) : database name.
            collection (str) : collection name.
            user (str):user name that we will query 
        Methods:
            user_exists(self) -> boolean :
                queries the mongodb database and checking if any record exists with this username
            create_basic_record(self) -> True or raises Value error:
                adding simple first record to the mongo database and returns True.
                if there is already user exists it will raise ValueError.
            drop_user_data(self) - None :
                drops the specific users data
            graph_records(self) -> dict:
                queries the database and searching for user specific records.
                if no records it will return empty list
            dump_test_records(self) - > None:
                FOR TESTING ONLY-- adds two random records to the users records database.
            remove_record(self,required_record,delete_all) -> None
                this method removes specific record or deleting all records.
            

        """

        #this is the connection to the db server
        self.client = MongoClient(uri)
        #string repr of the args
        self.str_db = db
        self.str_collection = collection


        #the classes of the pymongo client
        self.db = self.client[self.str_db]
        self.collection = self.db[self.str_collection]

        #the user name
        self.user = {"name":user}
        self.max_records = max_records


    def user_exists(self) ->bool:
        """
        checking if the user ixists in the database
        
        Returns:
            if user exists returns True
            if not exists return False
        """
        
        #query to find the user
        records = self.collection.find_one(self.user)
        
        if not records:
            return False

        if records:
            return True


    def create_basic_record(self) -> bool:
        if self.user_exists():
            return False

        else:
            data = {
                    'name': self.user["name"],
                    'db': self.str_db,
                    'collection': self.str_collection,
                    'graph_permited': True,
                    'graph_db_type': 'general_graph',
                    'graph_records': {},
                    'graph_repr': '1_row',
                    }
            # 
            self.collection.insert_one(data)
            return True


    def drop_user_data(self) -> None:
        self.collection.delete_one(self.user)


    def graph_records(self) -> dict:
        """
        queries the database to find the records if not found will return empty list
        """
        if self.user_exists():
            found_records = self.collection.find_one(self.user,{"graph_records.records":1})
            if found_records["graph_records"]:
                found_records.pop("_id")
                return found_records["graph_records"]["records"]
            else:
                return {}
        else:
            raise ValueError("the user not exists")


    def dump_test_records(self) -> None:
        #adding full list of records for TESTING ONLY!!!
        dump_data = {
                "1": {
                    'graph_title': 'Graph',
                    'graph_description': 'No Description',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023' ],
                    'y': [ 7491 ],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    },
                "2": {
                    'graph_title': 'Graph',
                    'graph_description': 'No Description',
                    'graph_type': 'bar_graph',
                    'created_at': '2023-12-5. 20:15',
                    'x': [ 'December 2023' ],
                    'y': [ 7491 ],
                    'y_2':[],
                    'sql_database':'income',
                    'start_date': '2023-11-26',
                    'end_date': '2024-01-06',
                    }}
        
        for key in dump_data:
            data = dump_data[key]
            name = key
            new_record_query = {
                "$set":{
                    f"graph_records.records.{str(name)}":data

                }
            }
            self.collection.update_one(self.user,new_record_query)


    def remove_record(self,required_record:str,delete_all=False) -> None :
        """
        method removes specific record by the record number provided from the arguments.

        Args:
            required_record(str) : this record number provided in the args and represented as the key in the mongodb structure.
                example for mongodb record structure:
                each record will generate a number 
                {"records":{"1":{this record data is here},"2":{this record data is here},"3":{this record data is here}}
            delete_all(bool=False) : if True it will drop the whole table of the user 

        Returns:
            deletes the required record and returns None
        """

        #first checking if the user exists
        if self.user_exists():
            
            if delete_all:
                #deletes the whole user data from the database
                    self.collection.delete_one(self.user)
                    print(f"the {self.user} deleted from the database")


            #if delete_all is False
            if not delete_all:
                
                #calling graph_records will return records dict if exists or empty list of not exists
                records = self.graph_records()
                
                if not records:
                    raise ValueError("the user exists but dont have records")
                
                if records:
                    #this checking if the required_record exists inside the  records and if not then it will return an error
                    if str(required_record) not in records:
                        raise ValueError("this record not exists")

                    else:
                        #create the delte query dict
                        delete_query = {
                            "$unset":{
                                f"graph_records.records.{str(required_record)}":1,
                                },
                            }
                        #the final result that will save the added record in the mongo db database
                        self.collection.update_one(self.user,delete_query)
                        print("the record deleted successfully")
                        
                
                #if there are not records exists it will raise a ValueError
                else:
                    raise ValueError("this record not exists")
        
        else:
            raise ValueError("the user not exists")


    def graph_positions(self) -> list:
        """
        method that returns a list of all positions inside the records
        if no records will raise ValueError

        Returns:
            list of positions if exists 
            ValueError if no records
        """

        if self.user_exists():
            records = self.graph_records()
            if records:
                positions = []
                for keys in records:
                    positions.append(str(keys))
                return positions
            else:
                raise ValueError("no records exists")
        raise ValueError("user not exists")
    

    def add_record(self,new_record:dict,position:int=0) -> None:
        """ 
        adding record to users mongo database 
        
        Args:
            new_record (dict) : the data of the new record that need to be added
            position (int) : default value is 0 and will do nothing 
                if the position will have another value it will set the new_record position to this position argument value
        """



        #if the user not exists it will create basic user record and then continue
        if not self.user_exists():
            self.create_basic_record()

        #records list 
        records = self.graph_records()


        #first we checking if the users max records capacity is full 
        if len(records) >= self.max_records:
            max_record_exceded_message = f"you exceded the maximum records in the user. your maximum is: {self.max_records}"
            print(max_record_exceded_message)
            raise ValueError(max_record_exceded_message)
        

        if int(position) > 0:
            #the format of the new data
            new_record_query = {
                "$set":{
                    f"graph_records.records.{position}":new_record
                }
            }

            #the final result that will save the added record in the mongo db database
            final = self.collection.update_one(self.user,new_record_query)
            print(f"the record is added successfully. record number : {position}")
            return None



        if len(records) ==  0:

            #the new record that will be created

            #if its new record so its the first graph position
            init_position = 1

            #the format of the new data example:"graph_records.records.1:{"x":[1,2,3],"y":["t","y","l"]...}
            graph_record = {
                "$set":{
                    f"graph_records.records.{init_position}":new_record,
                }
            }

            self.collection.update_one(self.user,graph_record)
            print(f"the record is added successfully. record number : {init_position}")
            return None


        #if user already have records in their mongo database
        if len(records) > 0:

            #position will be always len-1 and added to the end of the records
            last_position = int((self.graph_positions())[-1])
            new_position  = last_position + 1

            #the format of the new data
            new_record_query = {
                "$set":{
                    f"graph_records.records.{new_position}":new_record
                }
            }

            #the final result that will save the added record in the mongo db database
            final = self.collection.update_one(self.user,new_record_query)
            print(f"the record is added successfully. record number : {position}")
            return None


    def switch_records(self,src_position:str,dst_position:str) -> None:
        """
        this method switching places the position number

        Args:
            src_position (str,int) : the source position
            dst_position (str,int) : the destination position
        """

        #getting the user records
        records = self.graph_records()
        positions = self.graph_positions()
        #checking if the src record exists

        if str(src_position) not in positions:
            raise ValueError("src_position is invalid")

        if str(dst_position) not in positions:
            raise ValueError("dst_position is invalid")

        else:

            src_data = records[str(src_position)]
            dst_data = records[str(dst_position)]

            # changing the src to dst
            src_to_dst = {
            "$set": {
                f"graph_records.records.{dst_position}":src_data
            }}
            self.collection.update_one(self.user,src_to_dst)
            
            dst_to_src = {
            "$set": {
                f"graph_records.records.{src_position}":dst_data
            }}
            self.collection.update_one(self.user,dst_to_src)
            return None    
            

    def compare_record(self,position_1:str,position_2:str) -> None:
        """
        this method checking that the compare record is having the same amount of months and returns 3 lists
        one with first graph y(values)
        second with second graph y_2(values)
        third is a list with the x(months)
        """

        
        records = self.graph_records()
        #if the user dont have recods to compare
        if not records:
            raise ValueError("user dont have records")
        #if the user have available records and more than 1
        if len(records) > 1 :
            first_compare_record = records[position_1]
            second_compare_record_y = records[position_2]["y"]

            new_record = {
                "graph_title":first_compare_record["graph_title"],
                "graph_description":first_compare_record["graph_description"],
                "graph_type":(first_compare_record["graph_type"])+"_compared",
                "created_at":first_compare_record["created_at"],
                "x":first_compare_record["x"],
                "y":first_compare_record["y"],
                "y_2":second_compare_record_y,
                "sql_database":"income",
                "sql_database_compared":"outcome",
                "start_date":first_compare_record["start_date"],
                "end_date":first_compare_record["end_date"],
            }

            #deleting the existing records and creating new one compared
            self.remove_record(required_record=position_1)
            self.remove_record(required_record=position_2)

            self.add_record(new_record=new_record,position=position_1)

        else:
            raise ValueError("cant compare when have only one record")


    def edit_record(self,record_position:str,edit_data:dict) -> None:
        """
        method that gets the wanted record position and update it with the new data 

        Args:
            record_position (str) : specific record position that we want to edit.
            edit_data (dict) : the new data that will be edited
        """

        edit_record_query = {
            "$set":{
                f"graph_records.records.{record_position}":edit_data
            }
        }
        self.collection.update_one(self.user,edit_record_query)


    def find_data(self,data:dict) -> None:
        """
        mongodb.find wrapper method that can accept any raw mongodb find syntax:
            filter,projection,sort.
        
        Args:
            data (dict): the structure have to be like : {{filter},{projection},{sort}}

        Returns:
            print statment with the find result
        """
        find_result = self.collection.find_one(data)

        print("\n\nfind result ******************")
        print(find_result)
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
            "graph_repr":1,
            "current_year_income":1,
            "current_year_spendings":1,
            "max_records":1,
            "total_records":1,
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
            "graph_repr":{"$first":"$graph_repr"},
            "max_records":{"$first":"$max_records"},
            "total_records":{"$first":"$,total_records"},
            "current_year_income":{"$first":"$current_year_income"},
            "current_year_spendings":{"$first":"$current_year_spendings"},
            "lastrecords": {"$push": "$lastrecords"}
        }
    }
]
            

            aggregated_data = self.db.gr.aggregate(pipeline=pipe_line)

            # return aggregated_data
            for items in aggregated_data:
                #the total records here only for user representation
                total_records = {"total_records":records_amount}

                # print(items["max_records"])
                # print(items["max_records"])
                # print(items["current_year_income"])
                # print(items["current_year_spendings"])
                print(items["lastrecords"][0]["v"])
                return items


    def edit_graph_repr(self,new_repr:str) -> None:
        """
        method that changing the users graph representation to one of these:1 row , 2 rows

        Args:
            collection_name(str):mongodb collection name
            user(str):the user name that will be queried in the db
            new_repr(str):new representation of the users graph page (1 row or 2 rows)        
        """

        new_query = {
                "$set":{
                    "graph_repr":new_repr,
                }
            }
        
        print(self.graph_records())
        self.collection.update_one(self.user,new_query)


    def get_insights(self,user:str):
        """
        method that represents the insights data and returns it as a dict

        Args:
            collection_name(str) : collection name of the mongo database
            user(str) : the specific user that we need to get insights
        """
        query_filter = {"user_name":user}
        user_data = self.db_gr_query.find_one(query_filter)
        print(user_data)


    def save_insights(self,collection_name:str,user:str,insights_data:dict):
        """
        this method is saving the insights of the user in a mongodb table so it will be queried faster to a 
        mongodb and not with sql each get request

        Args:
            collection_name(str) : the collection name of the mongodb database.
            user(str) : the user that we will querie in the mongodb
            insights_data(dict) : this data will be saved in the db each time the method called 
        """
        filter_query = {"user_name":user}
        new_query = {
                "$set":insights_data
            }
        self.db_gr_query.update_one(filter_query,new_query)


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




# test_class = MongoDBConstructor(uri,"test")
# add_record_test = test_class.extract_record("gr","david",2)



# test_dict = {
#     "created_at":"YYYY-MM-DD",
#     "x":[1,1,1,1],
#     "y":["q","w","e","r"]
# }


#checking if the add record working - done
# add_record_test = test_class.add_record(collection_name="gr",user="ben",new_record=test_dict,many_records=False)

#checking the delete record method - done
# del_record_test = test_class.remove_records(collection_name="gr",user="david",record_number="1006")

#checking the get_record method - done
# get_record_test = test_class.get_record(collection_name="gr",user_name="david",record_count=1)

#checking the find_record method - done
# test_class.find_data(collection_name="gr",data={"user_name":"david"})





# test_class.remove_records(collection_name="gr",user="ben",record_number="1")