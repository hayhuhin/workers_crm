from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from  pathlib import Path
from django.contrib.auth.decorators import login_required
from .forms import AddGraphForm,EditGraphForm
from .models import Income,Outcome
from django.db.models import Sum
from func_tools.graph import GraphCalculator,graph_presentation
from mongo_db_graph.mongodb_connector import mongodb_constructor
import time
from user.models import Employer


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

    #this dict will have data of the graph later
    graph_chart = []

    #class that have methods and can query the sqlite for all the records of the db
    graph_calculator = GraphCalculator( user=request.user,db=[Income,Outcome],db_func=[Sum],last_save = "")

    #the graph html representation class
    graph_repr = graph_presentation()

    #this class have CRUD methods that save the graph data into the mongodb
    mongodb_handler = mongodb_constructor(uri="mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2",db_name="test")


    #gets the users all records from the mongodb 
    record_amount = employer_db_inst.graph_permission.all().values("record_amount")[0]




    #####################!testing in the get method section #############################


    #! uncomment this and refresh the dashboard page to delete all ben records
    # mongodb_handler.remove_records("gr","ben",record_number="*",delete_all=True)


    #! uncomment this if you want to see a repr of the user data
    # mongodb_handler.find_data("gr",{"user_name":str(request.user)})
    #!###################################################################################



    #* this section is querying the mongo db for records and saves the graphs as a dict of keys and values
    #* the key is the graph_name and the value is the html(with plotly lib) of the graph

    #this method gives me this specific user all records
    total_records = mongodb_handler.user_all_records(user=str(request.user),collection_name="gr")

    #this method will be used always when the page refreshing and query the mongodb for data
    mongodb_getting_data = mongodb_handler.get_record(collection_name="gr",user_name=str(request.user),record_count=total_records)



    #checking if there is any data at all from the mongodb query
    if mongodb_getting_data:
        #loops over the mongodb data and then using the graph_repr class to generate visual plotly graph and
        #save it as html
        for graph in mongodb_getting_data:

            
            
            graph_html = graph_repr.graph_options(graph_type=graph["v"]["graph_type"],group=graph["v"]["x"],values=graph["v"]["y"])  

            #this is the graph chart list that pushed to the html template with its graph data
            graph_chart.append({"graph_data":graph,"graph_html":graph_html})


    #instance of  "add graph form"
    income_form = AddGraphForm()

    #instance of a "edit graph form"
    edit_graph_form = EditGraphForm()


    #! only for testing for now (later it will be queried and represented)
    databases = ["Income","Outcome"]



    #checking if the request method is POST
    if request.method == "POST":
        print(request.POST)



        #only used as a shortcut to get the request.post data as "post_data"
        post_data = request.POST


        #? this sectiong is only if the post request comming from the add graph form
        if request.POST.get("add_graph_data") == "add_graph_data":

            #filling the AddGraphForm with the request.POST data from the user
            form_inst = AddGraphForm(request.POST)
            print(f"the requested post data is:{request.POST}")

            #checking the validity of the form (no injection etc...)
            if form_inst.is_valid():


                #simple form data for later usage
                user = request.user
                graph_title = form_inst.cleaned_data.get("graph_title")
                graph_description = form_inst.cleaned_data.get("graph_description")
                graph_type = form_inst.cleaned_data.get("graph")
                db = form_inst.cleaned_data.get("db")
                start = form_inst.cleaned_data.get("start_date")
                end = form_inst.cleaned_data.get("end_date")


                #this is the calculation of the data and returning it as 2 lists with x and y
                graph_data = graph_calculator.sum_by_range(start_date=start,end_date=end)


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
                    "y":graph_data[0]
                    }

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

                    #calculates the x and the y of the graph and returns it as two lists
                    edit_graph_data = graph_calculator.sum_by_range(start_date=edit_start,end_date=edit_end)
                    
                    
                    #showing the current time- its for user graph creation show
                    gmtime_dict = time.gmtime()
                    edit_time_now = str(f"{gmtime_dict[0]}-{gmtime_dict[1]}-{gmtime_dict[2]}. {gmtime_dict[3]}:{gmtime_dict[4]}")



                    edited_data = {
                         "graph_title":edit_graph_title,
                         "graph_description":edit_graph_description,
                         "graph_type":edit_graph_type,
                         "created_at":edit_time_now,
                         "x":edit_graph_data[1],
                         "y":edit_graph_data[0]
                    }
                    final = mongodb_handler.edit_record(collection_name="gr",user=str(edit_user),record_id=edit_graph_id,new_data=edited_data)
                    # mongodb_handler.find_data(collection_name="gr",data={"user_name":"ben"})

            
                    return HttpResponseRedirect("/dashboard")
                
                #this is if the form is not valid
                else:
                     #? later it will display an error page 
                     return HttpResponse("invalid form")
                
                    
                    


        #? here its response in the post scope
        context = {'databases':databases,'income_form':income_form,"graph_chart":graph_chart}
        return render(request,'code/dashboard.html',context)


    #? here its the response in the get scope
    context = {'databases':databases,'income_form':income_form,'edit_graph_form':edit_graph_form,'graph_chart':graph_chart}
    return render(request,'code/dashboard.html',context)


