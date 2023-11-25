import csv
import datetime


            # class AddGraphForm(forms.Form):

            #     graph_title = forms.CharField(max_length=50,initial="Graph")
            #     graph_description = forms.CharField(max_length=400,initial="No Description")
            #     start_date = forms.DateField()
            #     end_date = forms.DateField()
            #     # db = forms.CharField(max_length=100)
            #     db = forms.CharField(
            #         max_length=100,
            #         widget=forms.TextInput(attrs={'hidden': 'hidden'})
            #     )
            #     graph = forms.CharField(
            #         max_length=100,
            #         widget=forms.TextInput(attrs={'hidden': 'hidden'})
        #     )



class FileValidator:
    def __init__(self,file_data,file_max_size):
        self.file = file_data
        self.max_size = file_max_size
        

        #graph maximum_length attributes
        self.graph_maximum_length = {"graph_title":50,"graph_description":400,"created_at":20,"x":1000,"y":1000,"position":1,"db":100,"graph":100}

    def start_validation(self):
        #!steps to handle security:
        #check the file extension of the uploaded file
        if self.file.content_type == "text/csv":

            #this checking the size of the file
            if self.file.size <= self.max_size *  1024 * 1024:

                #this calling the csv_constructor method that accepts the file object and returning a text data
                constructed_data = self.csv_constructor(self.file)
                self.mongodb_field_validator(form_type="graph",data=constructed_data)

                #this method checking the keys validation of the file


            else:
                raise "file is too big"

        else:
            raise "wrong file type"


    def mongodb_field_validator(self,form_type:str,data:list):
        if form_type == "graph":
            
            
            #extracting the data to perform checking methods on them and validation
            key_data = []
            value_data = []
            for key,value in data.items():
                key_data.append(key)

            self.validate_keys(keys_data=key_data,ordered_check=True)
            self.validate_values(values_data=data,ordered_check=True)



            






    def csv_constructor(self,csv_file):
        csv_content = csv_file.read().decode('utf-8')
        reader = csv.reader(csv_content.splitlines())
        header = next(reader)
        values = next(reader)

        graph_data = {header[i]: values[i] for i in range(len(header))}

        # graph_data['created_at'] = datetime.strptime(graph_data['created_at'], '%Y-%m-%d. %H:%M')
        return graph_data

    def validate_keys(self,keys_data:list,ordered_check=False):
        graph_default_data = ["graph_title","graph_description","graph_type","created_at","x","y","position"]

        if ordered_check == False:
            for items in keys_data:
                if items in graph_default_data:
                    continue
                else:
                    print("VALIDATE KEYS ERROR ONE OF THE KEYS INVALID")
                    return False

            print("ALL KEYS ARE VALIDATED")
            return True
        
        if ordered_check == True:
            max_index_num = len(graph_default_data)-1
            for index in  range(len(graph_default_data)):
                if keys_data[index] == graph_default_data[index]:
                    continue

                else:
                    print("VALIDATE KEYS ERROR ONE OF THE KEYS INVALID")
                    return False
            print("ALL KEYS ARE ORDERED AND VALIDATED")
            return True
    

    def validate_values(self,values_data,ordered_check=False):
        #checking the type of the data and the amount like it should be in the graph form
        #* example:
            # class AddGraphForm(forms.Form):

            #     graph_title = forms.CharField(max_length=50,initial="Graph")
            #     graph_description = forms.CharField(initial="No Description")
            #     start_date = forms.DateField()
            #     end_date = forms.DateField()
            #     # db = forms.CharField(max_length=100)
            #     db = forms.CharField(
            #         max_length=100,
            #         widget=forms.TextInput(attrs={'hidden': 'hidden'})
            #     )
            #     graph = forms.CharField(
            #         max_length=100,
            #         widget=forms.TextInput(attrs={'hidden': 'hidden'})
        #     )
        #default graph data that must be in every graph creation
        graph_default_data = ["graph_title","graph_description","graph_type","created_at","x","y","position"]
        graph_default_len = len(graph_default_data)






        #each item checked if its a string or not

        for key,value in values_data:
            print(key)
            if type(value) == str:
                #*checking if key exists in the default graph dict
                if key in self.graph_maximum_length.keys():
                    #*here it validates that the len of the values are smaller or equal the default settings
                    if len(values_data) <= self.graph_maximum_length[key]:
                        print("THE VALUES LEN IS VALIDATED")
                    else:
                        print(f"THE VALUES --{values_data[key]}-- ARE GREATER THEN THE DEFAULTS")
                else:
                    print(f"THE KEY --{key}-- IS NOT IN THE DEFAULTS")
                

            else:
                print(f"THE FIELD {str(value)} IS NOT STRING")
                return False
        
        #this section is only executed if the for loop above is not breaking duo a invalid type of item
        print("I PASSED THE VALUE FOR LOOP")


    def run_proccess(self):
        self.start_validation()


test_class_validation = FileValidator(file_data=["sasa","sasa"],file_max_size=1)
graph_default_data_test = ["graph_title","graph_description","graph_type","created_at","x","y","position"]
# result = test_class_validation.validate_keys(keys_data=graph_default_data_test,ordered_check=True)
# print(result)
