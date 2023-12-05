from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from  pathlib import Path
from django.contrib.auth.decorators import login_required
from .forms import AddGraphForm,EditGraphForm,DeleteGraphForm,ChangeGraphPosition,ImportCSVForm,CompareGraphForm,EditGraphRow,AddInsights
from .models import Income,Outcome
from django.db.models import Sum
from func_tools.graph_calculations import GraphCalculator
from func_tools.graph_presentations import GraphRepresantation
from func_tools.file_validation import FileValidator
from mongo_db_graph.mongodb_connector import MongoDBConstructor
import time
from user.models import Employer
import csv
import io


curr_path = Path.cwd()


@login_required
def dashboard(request):
    """dashboard function that gets the request from the user validates the data and returning the response\n
        this specific page using many classes that each class do stuff in the backend.\n
        for example: class that connects to the database and queries users specific data needed from his post form and displays it in the frontend\n
        this function using login required decorator that checking that the user is loged in
    """

    #database user specific instance
    employer_db_inst = Employer.objects.get(user=request.user)


    #class that have methods and can query the sqlite for all the records of the db
    graph_calculator = GraphCalculator( user=request.user,db=[Income,Outcome],db_func=[Sum],last_save = "")

    #this class have CRUD methods that save the graph data into the mongodb
    windows_uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
    mac_uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
    mongodb_handler = MongoDBConstructor(uri=windows_uri,db_name="test")
    
    #the graph html representation class
    graph_repr = GraphRepresantation()


    #this dict will have data of the graph later
    graph_chart = []

    #gets the users all records from the mongodb 
    record_amount = employer_db_inst.graph_permission.all().values("record_amount")[0]
    

    #####################!testing in the get method section #############################
    # mongodb_handler.remove_records(collection_name="gr",user=str(request.user),record_number="3")

    #! uncomment this and refresh the dashboard page to delete all ben records
    # mongodb_handler.remove_records("gr",str(request.user),record_number="*",delete_all=True)


    #! uncomment this if you want to see a repr of the user data
    # mongodb_handler.find_data("gr",{"user_name":str(request.user)})
    #!###################################################################################



    #* this section is querying the mongo db for records and saves the graphs as a dict of keys and values
    #* the key is the graph_name and the value is the html(with plotly lib) of the graph

    ######################################
    #this section will have a method that checking if the user exists already or not and add a simple first data into the db
    res = mongodb_handler.user_exists(collection_name="gr",user=str(request.user))

    ######################################


    #this method gives me this specific user all records
    total_records = mongodb_handler.user_all_records(user=str(request.user),collection_name="gr",return_int=True)
    #this method will be used always when the page refreshing and query the mongodb for data
    mongodb_getting_data = mongodb_handler.get_record(collection_name="gr",user_name=str(request.user),record_count=total_records)


    information_insight = []
    #checking if there is any data at all from the mongodb query

    if mongodb_getting_data:

        #this dict structures the group and values data into a dict

        graph_values = {}
        #loops over the mongodb data and then using the graph_repr class to generate visual plotly graph and
        #save it as html

        for graph in mongodb_getting_data[0]:
            # graph_values["group"] = graph["v"]["x"]
            # graph_values["value"] =  graph["v"]["y"]
            # graph_values["value_2"] = graph["v"]["y_2"]
        
            graph_html = graph_repr.graph_options(dict_values=graph["v"],graph_type=graph["v"]["graph_type"],graph_repr=mongodb_getting_data[2])  

            #this is the graph chart list that pushed to the html template with its graph data
            graph_chart.append({"graph_data":graph,"graph_html":graph_html})

            total_graph = mongodb_getting_data[1]["total_records"]


        ########################################################################################
        #this section will be done inside the get/post request later 
        #
        #
        ########################################################################################
        # yearly_income_summary = graph_calculator.get_data_by_year(args=["2024","2025"],kwargs={"db":"income"})
        # yearly_outcome_summary = graph_calculator.get_data_by_year(args=["2024","2025"],kwargs={"db":"outcome"})

        # information_insight.append({
        #     "total_records":total_graph,
        #     "max_records" :record_amount["record_amount"],
        #     "current_year_income":yearly_income_summary,
        #     "current_year_spendings":yearly_outcome_summary,
            
        # })
        ########################################################################################




    #instance of  "add graph form"
    income_form = AddGraphForm()

    #instance of a "edit graph form"
    edit_graph_form = EditGraphForm()

    #delete graph form class instance
    delete_graph_form = DeleteGraphForm()

    change_positon_form = ChangeGraphPosition()

    import_csv_form = ImportCSVForm()

    compare_graph_form = CompareGraphForm()

    edit_graph_repr_form = EditGraphRow()

    add_insights_form = AddInsights()


    #* this is only for testing 

    values=[20, 20, 20, 20, 20,13,51]
    names= ['sunday', 'monday', 'tuesday', 'wednesday','thursday','friday','saturday']
    weekly_donut_graph = graph_repr.donut_graph(values=values,names= names)
    weekly_donut_graph2 = graph_repr.donut_graph(values=values,names= names)
    weekly_pie_graph = graph_repr.pie_graph(values=values,names=names)

    weekly_graph_card = graph_repr.graph_card('weekly lead',user_calc=weekly_donut_graph)
    weekly_graph_card2 = graph_repr.graph_card('weekly lead',user_calc=weekly_donut_graph2)
    weekly_pie_card = graph_repr.graph_card('weekly lead',user_calc=weekly_pie_graph)


    #! only for testing for now (later it will be queried and represented)
    databases = ["Income","Outcome"]








    #checking if the request method is POST
    if request.method == "POST":


        if request.POST.get("remove_graph") == "remove_graph":
            form_inst = DeleteGraphForm(request.POST)
            if form_inst.is_valid():
                graph_id = form_inst.cleaned_data.get("graph_id")
                mongodb_handler.remove_records(collection_name="gr",user=str(request.user),record_number=str(graph_id),delete_all=False)

                return HttpResponseRedirect("/dashboard")
            
            if not form_inst.is_valid():
                return redirect("the form is invalid")





        #only used as a shortcut to get the request.post data as "post_data"
        post_data = request.POST


        #? this sectiong is only if the post request comming from the add graph form
        if request.POST.get("add_graph_data") == "add_graph_data":


            #filling the AddGraphForm with the request.POST data from the user
            form_inst = AddGraphForm(request.POST)
            # print(f"the requested post data is:{request.POST}")

            #checking the validity of the form (no injection etc...)
            if form_inst.is_valid():
                print("is valid")

                #simple form data for later usage
                user = request.user
                graph_title = form_inst.cleaned_data.get("graph_title")
                graph_description = form_inst.cleaned_data.get("graph_description")
                graph_type = form_inst.cleaned_data.get("graph")
                db = form_inst.cleaned_data.get("db")
                start = form_inst.cleaned_data.get("start_date")
                end = form_inst.cleaned_data.get("end_date")


                #this is the calculation of the data and returning it as 2 lists with x and y 
                graph_data = graph_calculator.sum_by_range(start_date=start,end_date=end,db=db)



                #getting the time for the new_record that will be added to the mongodb record
                gmtime_dict = time.gmtime()
                time_now = str(f"{gmtime_dict[0]}-{gmtime_dict[1]}-{gmtime_dict[2]}. {gmtime_dict[3]}:{gmtime_dict[4]}")

                #the new record that will be added to the mongodb 
                new_record = {
                    "graph_title":graph_title,
                    "graph_description":graph_description,
                    "graph_type":graph_type,
                    "created_at" : time_now,
                    "x":graph_data[1],
                    "y":graph_data[0],
                    "start_date":str(start),
                    "end_date":str(end),
                    }

                ######################################
                #this section will have a method that checking if the user exists already or its new
                res = mongodb_handler.user_exists(collection_name="gr",user=str(request.user))

                ######################################


                #this the record that added to the collection in the mongodb 
                mongodb_added_record = mongodb_handler.add_record(collection_name="gr",user=str(request.user),new_record=new_record,max_record_amount=int(record_amount["record_amount"]))

                #returns http response redirect to the same page makes the page reload and update the view of the template
                #this needed because the post data is using ajax method that disables the normal refresh of the page
                return HttpResponseRedirect('/dashboard')


        #* this if statement is for edit post method
        if request.POST.get("edit_graph_data") == "edit_graph_data":
                
                #this is the instance of the edit graph form with the request.post user data
                edit_form_inst = EditGraphForm(request.POST)

                #this validates that the data is clean
                if edit_form_inst.is_valid():

                    #form data for later usage
                    edit_user = request.user
                    edit_graph_id = edit_form_inst.cleaned_data.get("graph_id")
                    edit_graph_title = edit_form_inst.cleaned_data.get("graph_title")
                    edit_graph_description = edit_form_inst.cleaned_data.get("graph_description")
                    edit_graph_type = edit_form_inst.cleaned_data.get("graph")
                    edit_db = edit_form_inst.cleaned_data.get("db")
                    edit_start = edit_form_inst.cleaned_data.get("start_date")
                    edit_end = edit_form_inst.cleaned_data.get("end_date")
                    edit_graph_position = edit_form_inst.cleaned_data.get("graph_position")

                    #calculates the x and the y of the graph and returns it as two lists
                    edit_graph_data = graph_calculator.sum_by_range(start_date=edit_start,end_date=edit_end,db=edit_db)
                    
                    
                    #showing the current time- its for user graph creation show
                    gmtime_dict = time.gmtime()
                    edit_time_now = str(f"{gmtime_dict[0]}-{gmtime_dict[1]}-{gmtime_dict[2]}. {gmtime_dict[3]}:{gmtime_dict[4]}")



                    edited_data = {
                         "graph_title":edit_graph_title,
                         "graph_description":edit_graph_description,
                         "graph_type":edit_graph_type,
                         "created_at":edit_time_now,
                         "x":edit_graph_data[1],
                         "y":edit_graph_data[0],
                         "position":edit_graph_position
                    }
                    final = mongodb_handler.edit_record(collection_name="gr",user=str(edit_user),record_id=edit_graph_id,new_data=edited_data)
                    # mongodb_handler.find_data(collection_name="gr",data={"user_name":"ben"})

            
                    return HttpResponseRedirect("/dashboard")
                
                #this is if the form is not valid
                else:
                     #? later it will display an error page 
                     return HttpResponse("invalid form")
        if request.POST.get("change_position_graph") == "change_position_graph":
            form_inst = ChangeGraphPosition(request.POST)


            if form_inst.is_valid():
                current_graph_id = form_inst.cleaned_data.get('src_graph_id')
                new_graph_position = form_inst.cleaned_data.get('dst_graph_id')
                mongodb_handler.switch_records(collection_name="gr",user=str(request.user),current_graph_id=current_graph_id,requested_position=new_graph_position)
                return HttpResponseRedirect("/dashboard")

            else:
                return HttpResponse("the form is invalid")

        #! later add here form validation 
        if request.POST.get("export_csv") == "export_csv":
            graph_id = request.POST.get("graph_id")
            graph_csv_model_data = mongodb_handler.export_csv_data(collection_name="gr",user=str(request.user),graph_id=graph_id)
            csv_data = generate_csv([graph_csv_model_data[0],graph_csv_model_data[1]])

            # print(graph_csv_model_data)
            response = HttpResponse(csv_data,content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="graph_1_data.csv"'
            return response

        if request.POST.get("import_csv_file") == "import_csv_file":
            #*here its passing into the file form the data
            form_inst = ImportCSVForm(request.POST,request.FILES)

            #*in the form is validated
            if form_inst.is_valid():
                csv_file = request.FILES['csv_file']

                #*this is the file validator that checking the file contents and validate it
                validation_proccess_instance = FileValidator(csv_file,2)
                validated_data = validation_proccess_instance.start_validation()
                if validated_data:
                    mongodb_added_record = mongodb_handler.add_record(collection_name="gr",user=str(request.user),new_record=validated_data,max_record_amount=int(record_amount["record_amount"]))
                    return HttpResponseRedirect("/dashboard")
                

                else:
                    return HttpResponse("the record is not added because the file content is invalid")
                    

                
            else:
                return HttpResponse("file form is invalid")

        if request.POST.get("delete_all_records") == "delete_all_records":
            mongodb_handler.remove_records("gr",str(request.user),record_number="*",delete_all=True)
            return HttpResponseRedirect("/dashboard")
        
        if request.POST.get("compare_graph_data") == "compare_graph_data":
            form_inst = CompareGraphForm(request.POST)
            print(request.POST)
            if form_inst.is_valid():
                print("the graph_compare is valid")
                user = str(request.user)
                graph_title = form_inst.cleaned_data.get("graph_title")
                graph_description = form_inst.cleaned_data.get("graph_description")
                graph_type = form_inst.cleaned_data.get("graph")
                db = form_inst.cleaned_data.get("db")
                start = form_inst.cleaned_data.get("start_date")
                end = form_inst.cleaned_data.get("end_date")
                src_id = form_inst.cleaned_data.get("graph_id")
                dst_position = form_inst.cleaned_data.get("dst_position")
                src_position = form_inst.cleaned_data.get("graph_position")


                user_compare_data = {
                    "graph_title":graph_title,
                    "graph_description":graph_description,
                    "graph_type":graph_type,
                    "src_position":src_position,
                    "dst_position":dst_position,
                    "start":str(start),
                    "end":str(end)
                        }
                # final = mongodb_handler.edit_record(collection_name="gr",user=str(edit_user),record_id=src_id,new_data=edited_data)
              
                structured_data = mongodb_handler.compare_record(collection_name="gr",user=user,src_id=src_id,user_data=user_compare_data,max_record_amount=int(record_amount["record_amount"]))
                return HttpResponseRedirect("/dashboard")
                #if the method returned data it will continue and add the data
                #     mongodb_handler.switch_records(collection_name="gr",max_record_amount=int(record_amount["record_amount"]),user=user,new_record=new_record)
            else:
                return HttpResponse("the form is not valid")
                #!steps to acomplish the compare graph
                #!need to add more fields to the form
                #!

        if request.POST.get("set_row") == "set_row":
            form_inst = EditGraphRow(request.POST)
            if form_inst.is_valid():
                row_repr = form_inst.cleaned_data.get("row_repr")
                if row_repr == "graph_representation":
                    return HttpResponseRedirect("/dashboard")
                else:
                    mongodb_handler.edit_graph_repr(collection_name="gr",user=str(request.user),new_repr=row_repr)
                    return HttpResponseRedirect("/dashboard")
                
            if not form_inst.is_valid():
                return HttpResponse("the form is invalid")
        
        if request.POST.get("add_insights_btn") == "add_insights_btn":

            form_inst = AddInsights(request.POST)

            if form_inst.is_valid():

                #all data gathered from the user input fields after validation 
                total_records = form_inst.cleaned_data.get("total_records")
                max_records = form_inst.cleaned_data.get("max_records")
                income_year_1 = form_inst.cleaned_data.get("income_year_1")
                income_year_2 = form_inst.cleaned_data.get("income_year_2")
                outcome_year_1 = form_inst.cleaned_data.get("outcome_year_1")
                outcome_year_2 = form_inst.cleaned_data.get("outcome_year_2")
                
                
                yearly_income_summary = graph_calculator.get_data_by_year(args=["2024","2025"],kwargs={"db":"income"})
                yearly_outcome_summary = graph_calculator.get_data_by_year(args=["2024","2025"],kwargs={"db":"outcome"})
                information_insight.append({
                    "total_records":total_graph,
                    "max_records" :record_amount["record_amount"],
                    "current_year_income":yearly_income_summary,
                    "current_year_spendings":yearly_outcome_summary,
                    
                })
                
                
                
                
                insights_data = {}

                mongodb_handler.save_insights(collection_name="gr",user=str(request.user),insights_data=insights_data)




    
    if request.method == "DELETE":
        print("the requested method is DELETE")
    




        #? here its response in the post scope
        context = {'databases':databases,'income_form':income_form,"graph_chart":graph_chart}
        return render(request,'code/dashboard.html',context)


    #? here its the response in the get scope
    if request.method == "GET":
        context= {'databases':databases,
                    'income_form':income_form,
                    'import_csv_form':import_csv_form,
                    'edit_graph_form':edit_graph_form,
                    'delete_graph_form':delete_graph_form,
                    'change_position_form':change_positon_form,
                    'graph_chart':graph_chart,
                    'compare_graph_form':compare_graph_form,
                    'edit_graph_row':edit_graph_repr_form,
                    'add_insights_form':add_insights_form}
        if information_insight:
            context = {'databases':databases,
                    'income_form':income_form,
                    'import_csv_form':import_csv_form,
                    'edit_graph_form':edit_graph_form,
                    'delete_graph_form':delete_graph_form,
                    'change_position_form':change_positon_form,
                    'graph_chart':graph_chart,
                    'compare_graph_form':compare_graph_form,
                    'information_insight':information_insight[0],
                    'graph_repr':mongodb_getting_data[2][0],
                    'edit_graph_row':edit_graph_repr_form,
                    'add_insights_form':add_insights_form}
   
        if not information_insight:
            context = {'databases':databases,
                    'income_form':income_form,
                    'import_csv_form':import_csv_form,
                    'edit_graph_form':edit_graph_form,
                    'delete_graph_form':delete_graph_form,
                    'change_position_form':change_positon_form,
                    'graph_chart':graph_chart,
                    'compare_graph_form':compare_graph_form,
                    'information_insight':information_insight,
                    'edit_graph_row':edit_graph_repr_form,
                    'add_insights_form':add_insights_form}
        
        
        return render(request,'code/dashboard.html',context)


def generate_csv(graph_data):
    # Your data source (replace this with your data retrieval logic)
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerows(graph_data)
    return csv_data.getvalue()