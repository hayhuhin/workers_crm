
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
            user_exists() -> boolean :
                queries the mongodb database and checking if \n \t\trecord exists for specific user

            create_basic_record() -> True or raises Value error:
                adding simple first record to the mongo database.
                returns bool if user already exists or not.

            drop_user_data() - None :
                drops the specific users data by the user name

            graph_records() -> dict:
                queries the database and searching for user \n\t\tspecific records.
                if records exists - > returns dict with the data
                if no records -> returns empty dict

            add_record(new_record:list,position:int=0,ignore_max:bool=False):
                method that adds the record adds the record to the end of the list
                this makes it o(1) and updating the database accordingly with the internal functions
                
            switch_records(src_position:str,dst_position:str)
                switching the positions of the records

            compare_record(position_1:str,position_2:str)
                this method creating a new record combined with the ones parsed in the args 
                and removes the seperated from the database with the remove_record() method

            remove_record(required_record:str,delete_all:bool):
                this method removes the items and then sorting the list by degrading the records
                to the start the time complexity is o(n-len(n))

            edit_record(record_position:str,edit_data:dict):
                saving the parsed data in the requested record_position
            find_data(data:dict):
                wrapper method that acts as a find function in mongodb
            graph_positions() -> list:
                method that returns a list of all positions inside the records.
                this method is used internally to have better sorting with CRUD operations
                if no records will raise ValueError.

            find_graph_ordered_list() -> list:
                queries the database and represents the saved positions list.

            update_ordered_list() -> None:
                internal functionallity for updating the ordered list.

            dump_test_records() -> None:
                FOR TESTING ONLY-- adds two random records to the \n\t\tusers records database.

            remove_record(required_record,delete_all) -> None
                this method removes specific record or deleting all\n\t\t records.
            
            

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
        checking if the user exists in the database
        
        Returns:
            if exists -> True
            if not exists -> False
        """
        
        #query to find the user
        user = self.collection.find_one(self.user)
        
        if not user:
            return False

        if user:
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
                    'ordered_list':[]
                    }
            # 
            self.collection.insert_one(data)
            return True


    def drop_user_data(self) -> None:
        """
        deletes the database of the specific user.

        Returns:
            None.
        """

        self.collection.delete_one(self.user)


    def graph_records(self) -> dict:
        """
        returning dict with records

        Returns:
            if user have records -> dict with data
            if user dont have records -> empty dict
        """
        if self.user_exists():
            found_records = self.collection.find_one(self.user,{"graph_records.records":1})
            if found_records["graph_records"]:
                found_records.pop("_id")
                return found_records["graph_records"]["records"]
            else:
                return {}
        else:
            return {}


    def dump_test_records(self) -> None:
        """
        adds two records to the users database.
        used for unittesting only.

        Returns:
            None
        """
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
            self.add_order_item(int(name))
            self.collection.update_one(self.user,new_record_query)
            # self.add_record(dump_data)


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

        #* checking if the user exists
        if not self.user_exists():
            message = {"error":"user not exists"}
            return False,message
        
        #* checkinf if delete_all is True
        if delete_all:
            #deletes the whole user data from the database
                self.collection.delete_one(self.user)
                    # print(f"the {self.user} deleted from the database")

        
        #* checking if user have records
        records_data = self.graph_records()
        if not records_data:
            message = {"error":"user dont have records"}
            return False,message

        

        #* checking if the required record is exists in the data itself
        if str(required_record) not in records_data:
            message = {"error":"the required position not exists"}
            return False,message


        #delete the requested record
        delete_query = {
            "$unset":{
                f"graph_records.records.{str(required_record)}":1,
                },
            }
        self.collection.update_one(self.user,delete_query)
        #deleting the ordered list 
        list_data = self.find_graph_ordered_list()
        target = int(required_record)-1
        list_data.pop(target)


        #getting the newest records(after deleting the required record)
        new_records = self.graph_records()

        
        #iterating over the requested index += 1
        for index in range(len(list_data)-target):
            #updates the list_data from [1,2,4] to [1,2,3]
            list_data[target] = list_data[target]-1
            


            #creating vars of new key and the old data {"3(new key)":"old data"}
            prev_index = list_data[target]+1
            prev_data = new_records[str(prev_index)]

            self.collection.update_one(self.user,{"$set":
                                                    {f"graph_records.records.{str(list_data[target])}":prev_data},
                                                    })
            #this removing the multiplied record
            # self.remove_record(required_record=prev_index)
            self.collection.update_one(self.user,{"$unset":{
                                                        f"graph_records.records.{prev_index}":1}})
            
            
            target += 1

        #updating the list data 
        self.update_ordered_list(list_data)

        message = {"success":"the required position is deleted successfully"}
        return True,message
        


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
    

    def add_order_item(self,position:int) -> None:
        """
        adding the item to the last index of the list
        the position must be int and by the right order

        Returns:
            None
        """

        ordered_list = (self.collection.find_one(self.user,{"ordered_list":1})["ordered_list"])
        ordered_list.insert(position-1,position)
        update_order_list = {
            "$set":{
                "ordered_list":ordered_list
            }
        }
        self.collection.update_one(self.user,update_order_list)


    def find_graph_ordered_list(self) -> list:
        """
        returns the ordered_list from the mongodb.

        Returns:
            list of the last updated ordered_list from the mongodb 
        """
        ordered_list = self.collection.find_one(self.user,{"ordered_list":1})["ordered_list"]
        return ordered_list


    def update_ordered_list(self,updated_list:list) -> None:
        """
        updating the whole ordered_list with the new list that will provided as the argument

        Args:
            updated_list(list):the new list that will be saved in the database as "ordered_list"
        """
        ordered_list = self.collection.update_one(self.user,
                                                  {"$set":
                                                    {"ordered_list":updated_list}
                                                    })


    def add_record(self,new_record:dict,position:int=0,ignore_max:bool=False) -> None:
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

        if not records:

            #the new record that will be created

            #if its new record so its the first graph position
            init_position = 1

            #the format of the new data example:"graph_records.records.1:{"x":[1,2,3],"y":["t","y","l"]...}
            graph_record = {
                "$set":{
                    f"graph_records.records.{init_position}":new_record,
                }
            }

            #updating the ordered list
            self.add_order_item(int(init_position))

            self.collection.update_one(self.user,graph_record)
            # print(f"the record is added successfully. record number : {init_position}")
            return None
        

        if len(records) >= self.max_records and ignore_max == False:
            max_record_exceded_message = f"you exceded the maximum records in the user. your maximum is: {self.max_records}"

            raise ValueError(max_record_exceded_message)
        

        if int(position) > 0:
            #the format of the new data
            new_record_query = {
                "$set":{
                    f"graph_records.records.{position}":new_record
                }
            }
            
            #updating the ordered list
            self.add_order_item(int(position))

            #the final result that will save the added record in the mongo db database
            final = self.collection.update_one(self.user,new_record_query)
            # print(f"the record is added successfully. record number : {position}")
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

            #updating the ordered list
            self.add_order_item(int(new_position))

            #the final result that will save the added record in the mongo db database
            final = self.collection.update_one(self.user,new_record_query)
            # print(f"the record is added successfully. record number : {position}")


    def switch_records(self,src_position:str,dst_position:str) -> None:
        """
        this method switching places the position number

        Args:
            src_position (str,int) : the source position
            dst_position (str,int) : the destination position

        Returns:
            None.
        """

        #* checking if positions exist
        src_position_exists = self.get_record_by_position(src_position)
        if not all(src_position_exists):
            message = {"error":"invalid position passed"}
            return False,message
        
        dst_position_exists = self.get_record_by_position(dst_position)
        if not all(dst_position_exists):
            message = {"error":"invalid position passed"}
            return False,message



        #getting the user records
        records = self.graph_records()
        # positions = self.graph_positions()
        #checking if the src record exists

        # if str(src_position) not in positions:
        #     raise ValueError("src_position is invalid")

        # if str(dst_position) not in positions:
        #     raise ValueError("dst_position is invalid")

    # else:

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
        message = {"success":"switched the positions successfully"}
        return True,message
            

    def get_record_by_position(self,position:int):
        """
        method that returns the graph data of the passed position 

        data returned as a Dict
        Returns boolean,dict
        """
        #* checking if the position is passed as integer
        if not isinstance(position,int):
            message = {"error":"passed invalid type"}
            return False,message

        projection = {f"graph_records.records.{int(position)}":{"$exists": True}}

        data_found = self.find_data(data={**self.user,**projection})


        if not data_found:
            message = {"error":"position not exists"}
            return False,message
        
        data_found.pop("_id")
        message = {"success":"found required data",f"{position}":data_found["graph_records"]["records"][str(position)]}
        return True,message


    def compare_record(self,position_1:str,position_2:str) -> None:
        """
        this method checking that the compare record is having the same amount of months and returns 3 lists
        one with first graph y(values)
        second with second graph y_2(values)
        third is a list with the x(months)
        """
        #transforms it to strings
        #! ill add another method that will check the types of the inserted data before passing the args 

        #* checking if positions are exist
        pos_1_exists = self.get_record_by_position(position_1)
        if not all(pos_1_exists):
            message = {"error":"invalid position passed"}
            return False,message
        
        pos_2_exists = self.get_record_by_position(position_2)
        if not all(pos_2_exists):
            message = {"error":"invalid position passed"}
            return False,message

        #! into the class/method
        position_1 = str(position_1)
        position_2 = str(position_2)

        records = self.graph_records()
        #if the user dont have recods to compare
        if not records:
            message = {"error":"user dont have any record to compare with"}
            return False,message
        
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
            ordered_list = self.find_graph_ordered_list()
            #adding the new compared graph to the end of the list
            # ordered_list.append(len(ordered_list))
            self.update_ordered_list(ordered_list)

            self.add_record(new_record=new_record,ignore_max=True)
            if int(position_1) > int(position_2):
                self.remove_record(required_record=position_1)
                self.remove_record(required_record=int(position_2))
                message = {"success":"compared the record successfully"}
                return True,message
            else:
                self.remove_record(required_record=int(position_2))
                self.remove_record(required_record=int(position_1))
                message = {"success":"compared the record successfully"}
                return True,message

        else:
            message = {"error":"cant compare when have only one record"}
            return True,message


    def edit_record(self,record_position:str,edit_data:dict) -> None:
        """
        saving the parsed data in the requested record_position

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


    def find_data(self,data:dict) -> list:
        """
        mongodb.find wrapper method that can accept any raw mongodb find syntax:
            filter,projection,sort.
        
        Args:
            data (dict): the structure have to be like : {{filter},{projection},{sort}}

        Returns:
            print statment with the find result
        """
        find_result = self.collection.find_one(data)
        # find_result.pop("_id")
        return find_result


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
        
        
        self.collection.update_one(self.user,new_query)


    def get_insights(self,user:str) -> None:
        """
        method that represents the insights data and returns it as a dict

        Args:
            collection_name(str) : collection name of the mongo database
            user(str) : the specific user that we need to get insights
        """
        query_filter = {"name":user}
        user_data = self.collection.find_one(query_filter,{"insights":1})
        return user_data["insights"]


    def update_insights(self,insights_data:dict) -> None:
        """
        this method is saving the insights of the user in a mongodb table so it will be queried faster to a 
        mongodb and not with sql each get request

        Args:
            collection_name(str) : the collection name of the mongodb database.
            user(str) : the user that we will querie in the mongodb
            insights_data(dict) : this data will be saved in the db each time the method called 
        """

        json_data= {
                "$set":{"insights":insights_data}
            }

        self.collection.update_one(self.user,json_data)


    def delete_insights(self,insights_id:str):



        id_exists = self.collection.find_one(self.user,{f"insights.{insights_id}":1})["insights"]

        if id_exists:

            query = {
                "$unset":{f"insights.{insights_id}":1}
            }

            result = self.collection.update_one(self.user,query)
            return True
        return False


    def add_insights(self,insights_data:dict,max_amount:int) -> None:
        """
        this method is saving the insights of the user in a mongodb table so it will be queried faster to a 
        mongodb and not with sql each get request

        Args:
            collection_name(str) : the collection name of the mongodb database.
            user(str) : the user that we will querie in the mongodb
            insights_data(dict) : this data will be saved in the db each time the method called 
        """

        #* checking if the user exist
        user_exists = self.user_exists()
        if not user_exists:
            self.create_basic_record()

        # insight_format = {str(randint(1,10000000)):insights_data}
        current_insight_amount = self.collection.find_one(self.user,{"insights":1})
        if "insights" not in current_insight_amount:
            self.collection.update_one(self.user,{"$set":{"insights":{}}})


        current_insight_amount = self.collection.find_one(self.user,{"insights":1})
        if (len(current_insight_amount["insights"])) >= max_amount:
            return False
        else:
            json_data= {
                    "$set":{f"insights.{str(randint(1,100000))}":insights_data}
                        }
            self.collection.update_one(self.user,json_data)
            return True


    def export_csv_data(self,graph_position) -> list:
        """
        this method returns the specific data needed to be exported the by the user as csv
        Returns:
            two lists - one with titles.
                        second with the data.
        """
        records = self.graph_records()
        titles = []
        content = []
        for data in records[graph_position]:

            titles.append(data)
            content.append(records[graph_position][data])

        return titles,content
    
    