from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from  pathlib import Path
from django.contrib.auth.decorators import login_required
from .forms import AddGraphForm,EditGraphForm,DeleteGraphForm,ChangeGraphPositionForm,ImportCSVForm,CompareGraphForm,EditGraphRowForm,AddInsightsForm
from .models import Income,Outcome
from django.db.models import Sum
from func_tools.graph_calculations import GraphCalculator
from func_tools.graph_presentations import GraphRepresantation
from func_tools.file_validation import FileValidator,generate_csv
from mongo_db_graph.mongodb_connector import MongoDBConstructor
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
    #user name string representation
    user = str(request.user)

    #gets the current time 
    gmtime_dict = time.gmtime()
    time_now = str(f"{gmtime_dict[0]}-{gmtime_dict[1]}-{gmtime_dict[2]}. {gmtime_dict[3]}:{gmtime_dict[4]}")

    #database user specific instance
    employer_db_inst = Employer.objects.get(user=request.user)

    #class that have methods and can query the sqlite for all the records of the db
    graph_calculator = GraphCalculator( user=request.user,db=[Income,Outcome],db_func=[Sum],last_save = "")

    #max records gives me the max graph mermission
    max_records = employer_db_inst.graph_permission.all().values("max_record_amount")[0]["max_record_amount"]

    #uri is the url to that im connecting to mongodb
    uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2"
    #mongodb wrapper class that have CRUD methods
    mongodb_handler = MongoDBConstructor(uri=uri,db="test",collection="gr",user=str(request.user),max_records=max_records)
    graph_repr = GraphRepresantation()


    #* the initialising of the forms 

    income_form = AddGraphForm()

    edit_graph_form = EditGraphForm()

    delete_graph_form = DeleteGraphForm()

    change_positon_form = ChangeGraphPositionForm()

    import_csv_form = ImportCSVForm()

    compare_graph_form = CompareGraphForm()

    edit_graph_repr_form = EditGraphRowForm()

    add_insights_form = AddInsightsForm()


    #this list will parse graph data and graph html into the template
    graph_chart = []
    #this list will parse insights data and graph html into the template
    insights_data = []


    #*need to check later if the user have all permission from sql first -  models.GraphPermissions
    if not mongodb_handler.user_exists():
        mongodb_handler.create_basic_record()

    #method returns dict with records or empty dict if records not exist
    graph_records_dict = mongodb_handler.graph_records()

    #users first basic data
    user_basic_data = mongodb_handler.find_data({"name":user})

    #saving the insights data to be parsed into the template
    if "insights_data" in user_basic_data:
        insights_data = user_basic_data["insights_data"]

    #checking if the user have records
    if graph_records_dict:
        #itarates over the records keys
        for record in graph_records_dict:
            
            #for comparison methods i should parse "sql_database_compared" even if empty
            #checking if there are any sql_comparison records in the db
            if "sql_database_compared" in graph_records_dict[record]:
                sql_comparison = graph_records_dict[record]["sql_database_compared"]
            else:
                sql_comparison = []

            #this is how the structure if the "dict_values" argument have to look like
            dict_values = {"x":graph_records_dict[record]["x"],
                           "y":graph_records_dict[record]["y"],
                           "y_2":graph_records_dict[record]["y_2"],
                           "graph_description":graph_records_dict[record]["graph_description"],
                           "DB_1":graph_records_dict[record]["sql_database"],
                           "DB_2":sql_comparison}

            #this method creating graph html with the data extracted from the mongodb 
            graph_html = graph_repr.graph_options(graph_type=graph_records_dict[record]["graph_type"],dict_values=dict_values,graph_repr=user_basic_data["graph_repr"])  

            #appending the graph_html to the graph_chart list and the list will be parsed into the html template
            graph_chart.append({"graph_data":graph_records_dict[record],"graph_position":record,"graph_html":graph_html})



    #! in the future it will be automaticly gathered from the users graph permissions
    databases = ["Income","Outcome"]



    #* the get request scope
    if request.method == "GET":            
        context= {  'databases':databases,
                    'income_form':income_form,
                    'import_csv_form':import_csv_form,
                    'edit_graph_form':edit_graph_form,
                    'delete_graph_form':delete_graph_form,
                    'change_position_form':change_positon_form,
                    'graph_chart':graph_chart,
                    'compare_graph_form':compare_graph_form,
                    'edit_graph_row':edit_graph_repr_form,
                    'graph_repr':user_basic_data["graph_repr"][0],
                    'add_insights_form':add_insights_form,
                    'insights_data':insights_data}

        return render(request,'code/dashboard.html',context)


    #* the post request scope
    if request.method == "POST":


        #* add graph record post
        if request.POST.get("add_graph_data") == "add_graph_data":

            #firmfilling with user post data
            form_inst = AddGraphForm(request.POST)

            #validating form
            if not form_inst.is_valid():
                HttpResponse("form is invalid")
            #if form is valid

            else:
                #*  user field data
                graph_title = form_inst.cleaned_data.get("graph_title")
                graph_description = form_inst.cleaned_data.get("graph_description")
                graph_type = form_inst.cleaned_data.get("graph")
                db = form_inst.cleaned_data.get("db")
                start = form_inst.cleaned_data.get("start_date")
                end = form_inst.cleaned_data.get("end_date")


                #*   this is the calculation of the data and returning it as 2 lists with x and y 
                graph_data = graph_calculator.sum_by_range(start_date=start,end_date=end,db=db)

                #the new record that will be added to the mongodb 
                new_record = {
                    "graph_title":graph_title,
                    "graph_description":graph_description,
                    "graph_type":graph_type,
                    "created_at" : time_now,
                    "x":graph_data[1],
                    "y":graph_data[0],
                    "y_2":[],
                    'sql_database':db,
                    "start_date":str(start),
                    "end_date":str(end),
                    }

                #adding the record to mongodb
                mongodb_handler.add_record(new_record=new_record)
                #reloads the same page
                return HttpResponseRedirect('/dashboard')


        #* remove graph record post
        if request.POST.get("remove_graph") == "remove_graph":

            form_inst = DeleteGraphForm(request.POST)
            if not form_inst.is_valid():
                return HttpResponse("the form is invalid")
            
            #for is valid
            else:
                graph_position = form_inst.cleaned_data.get("graph_position")
                mongodb_handler.remove_record(required_record=graph_position)
                return HttpResponseRedirect("/dashboard")


        #* edit graph record post
        if request.POST.get("edit_graph_data") == "edit_graph_data":
            edit_form_inst = EditGraphForm(request.POST)
            if not edit_form_inst.is_valid():
                return HttpResponse("invalid edit form")
            
            #if form is valid
            else:
                #form data for later usage
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
                
                edited_data = {
                        "graph_title":edit_graph_title,
                        "graph_description":edit_graph_description,
                        "graph_type":edit_graph_type,
                        "created_at":time_now,
                        "x":edit_graph_data[1],
                        "y":edit_graph_data[0],
                        "y_2":[],
                        "sql_database":edit_db,
                        "start_date":str(edit_start),
                        "end_date":str(edit_end)
                }
                
                final = mongodb_handler.edit_record(record_position=edit_graph_position,edit_data=edited_data)        
                return HttpResponseRedirect("/dashboard")
                

        #* switch graph position post
        if request.POST.get("change_position_graph") == "change_position_graph":
            form_inst = ChangeGraphPositionForm(request.POST)
            if not form_inst.is_valid():
                return HttpResponse("form is invalid")

            #valid form
            else:
                src_position = form_inst.cleaned_data.get('src_graph_id')
                dst_position = form_inst.cleaned_data.get('dst_graph_id')
                mongodb_handler.switch_records(src_position=src_position,dst_position=dst_position)

                return HttpResponseRedirect("/dashboard")


       #* compare graph records post 
        if request.POST.get("compare_graph_data") == "compare_graph_data":
            form_inst = CompareGraphForm(request.POST)
            if not form_inst.is_valid():
                return HttpResponse("the form is not valid")

            #valid form
            else:
                #* this data will get another step of validation later 
                #* for now we will trust the users input correctness
                #* this should return error if im comparing bad data(different dates or more y data than y_2 etc...)
                graph_title = form_inst.cleaned_data.get("graph_title")
                graph_description = form_inst.cleaned_data.get("graph_description")
                graph_type = form_inst.cleaned_data.get("graph")
                db = form_inst.cleaned_data.get("db")
                start = form_inst.cleaned_data.get("start_date")
                end = form_inst.cleaned_data.get("end_date")
                src_id = form_inst.cleaned_data.get("graph_id")
                src_position = form_inst.cleaned_data.get("graph_position")
                dst_position = form_inst.cleaned_data.get("dst_position")

                
                structured_data = mongodb_handler.compare_record(position_1=src_position,position_2=dst_position)
                return HttpResponseRedirect("/dashboard")


        #* delete all records post
        if request.POST.get("delete_all_records") == "delete_all_records":
            mongodb_handler.remove_records("gr",str(request.user),record_number="*",delete_all=True)
            return HttpResponseRedirect("/dashboard")

        #! later add here form validation 
        if request.POST.get("export_csv") == "export_csv":
            graph_id = request.POST.get("graph_position")
            graph_csv_model_data = mongodb_handler.export_csv_data(graph_position=graph_id)
            csv_data = generate_csv([graph_csv_model_data[0],graph_csv_model_data[1]])

            response = HttpResponse(csv_data,content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="graph_1_data.csv"'
            return response

        #! for now this feature is disabled 
        if request.POST.get("import_csv_file") == "import_csv_file":
            #*here its passing into the file form the data
            form_inst = ImportCSVForm(request.POST,request.FILES)

            #*in the form is validated
            # if form_inst.is_valid():
            #     csv_file = request.FILES['csv_file']

            #     #*this is the file validator that checking the file contents and validate it
            #     validation_proccess_instance = FileValidator(csv_file,2)
            #     validated_data = validation_proccess_instance.start_validation()
            #     if validated_data:
            #         mongodb_added_record = mongodb_handler.add_record(collection_name="gr",user=str(request.user),new_record=validated_data,max_record_amount=int(record_amount["record_amount"]))
            #         return HttpResponseRedirect("/dashboard")
            return HttpResponseRedirect("/dashboard")

                # else:
                #     return HttpResponse("the record is not added because the file content is invalid")
                    

                
            # else:
            #     return HttpResponse("file form is invalid")


        if request.POST.get("set_row") == "set_row":
            form_inst = EditGraphRowForm(request.POST)
            if form_inst.is_valid():
                row_repr = form_inst.cleaned_data.get("row_repr")
                if row_repr == "graph_representation":
                    return HttpResponseRedirect("/dashboard")
                else:
                    mongodb_handler.edit_graph_repr(new_repr=row_repr)
                    return HttpResponseRedirect("/dashboard")
                
            if not form_inst.is_valid():
                return HttpResponse("the form is invalid")
        

        if request.POST.get("add_insights_btn") == "add_insights_btn":

            form_inst = AddInsightsForm(request.POST)
            print(request.POST)

            if not form_inst.is_valid():
                return HttpResponse("invalid form")

            #form is valid
            else:

                income_year_1 = form_inst.cleaned_data.get("income_year_1")
                income_year_2 = form_inst.cleaned_data.get("income_year_2")
                outcome_year_1 = form_inst.cleaned_data.get("outcome_year_1")
                outcome_year_2 = form_inst.cleaned_data.get("outcome_year_2")
                total_graph = len(user_basic_data["ordered_list"])
                yearly_income_summary = graph_calculator.get_data_by_year(args=[income_year_1,income_year_2],kwargs={"db":"income"})
                yearly_outcome_summary = graph_calculator.get_data_by_year(args=[outcome_year_1,outcome_year_2],kwargs={"db":"outcome"})


                insights_data = {
                    "total_records":total_graph,
                    "max_records" :max_records,
                    "current_year_income":yearly_income_summary,
                    "current_year_spendings":yearly_outcome_summary,                    
                }

                mongodb_handler.save_insights(insights_data={"insights_data":insights_data})
                return HttpResponseRedirect("/dashboard")

    #* the delete request scope
    if request.method == "DELETE":
        print("the requested method is DELETE")
    




        #? here its response in the post scope
        context = {'databases':databases,'income_form':income_form,"graph_chart":graph_chart}
        return render(request,'code/dashboard.html',context)


