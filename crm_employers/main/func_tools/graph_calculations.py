import datetime
import calendar


#handle DB querying from the arguments passed to the function
def graph_percentage_presentation(user_model,job_position_tasks=False,personal_tasks=False,leads=False):
    """ simple percentage function that returns the completed percentage of the tasks"""
    if job_position_tasks:
        
        all_tasks = user_model.job_position.task.all()
        completed_tasks = user_model.job_position.task.filter(completed=True)

        if len(all_tasks):
            percentage_single_task = (100/len(all_tasks))

            percentage_done = len(completed_tasks) * percentage_single_task

            return round(percentage_done)
        else:
            return 0
    

    if  personal_tasks:

        all_tasks = user_model.task.all()
        completed_tasks = user_model.task.filter(completed=True)

        percentage_single_task = (100/len(all_tasks))

        percentage_done = len(completed_tasks) * percentage_single_task

        return round(percentage_done)
    
    if leads:


        all_leads = user_model.lead.all()
        completed_leads = user_model.lead.filter(completed=True)

        percentage_single_lead = (100/len(all_leads))

        percentage_done = len(completed_leads) * percentage_single_lead

        return round(percentage_done)
   

#* this function used in the employer profile app view
def employer_data_info(request):
    """method returning dict with the user information"""
    first_name = request.user.employer.first_name
    last_name = request.user.employer.last_name
    department = request.user.employer.job_position.position
    rank = request.user.employer.job_position.rank 
    profile_pic = request.user.employer.profile_pic.url

    request_data = {'username':first_name+" "+last_name,'job_position':department,'job_rank':rank,'profile_pic':profile_pic}
    return request_data



class GraphCalculator:
    """
    class that connecting to the db and performing data extraction with its methods

    Attributes:
        user (str) : the specific users name as string.
        last_save (str) : doesnt have any purpose for now.
        db (list(object)) : must contain the object of the database of the specific user.
        db_func (list(object)) : must contain the specific django database functions (example:Sum function that
        used in the aggregate method).
        
    Methods:
        sum_single_month(self,date (str),db (object),db_func (object)) -> list
            sums all records in the same month of the year
        sum_by_range(self,start_date (str),end_date (str),db (object) ,db_func (object)) -> list
            sums all months in the range and return two lists with the months-year(str) and amount(int)
        get_data_by_year(self,args(list(int)),**kwargs(dict(str))) -> dict
            
            sums the result of all months in the same year and returns a dict with the year:sum(amount)
    """

    def __init__(self,user:str,last_save:str,db=list(),db_func=list()):
        self.user = user
        self.last_save = last_save
        self.db = db 
        self.db_func = db_func


    def sum_single_month(self,date:str,db:str):
        """
        sums all records inside the same month and returning two lists with data if the records exists 
        if the records not exists it will raise exception message

        Attributes:
        first_day (str) : the starting point of the month(example: "2024-11-01").
        db (str): database str repr.
        db_func (object function): database function(example "Sum" object that can be used inside the aggregate method when extracting sql data)
        
        """

        first_day_datetime_object = datetime.datetime.strptime(date,"%Y-%m-%d").date()
        last_day_datetime_object = first_day_datetime_object.replace(day = calendar.monthrange(first_day_datetime_object.year, first_day_datetime_object.month)[1])

        first_day = first_day_datetime_object.strftime("%Y-%m-%d")
        last_day = last_day_datetime_object.strftime("%Y-%m-%d")

        #varifing that the string is lower case
        db = db.lower()

        if db == "income":
            full_amount_summary = self.db[0].objects.filter(month__range=(first_day,last_day)).all().values_list().aggregate(self.db_func[0]('amount'))["amount__sum"]
            month_year_repr= (first_day_datetime_object.strftime("%B")[0:3] +" "+ (first_day_datetime_object.strftime("%Y"))[2:])

            if full_amount_summary: 
                return month_year_repr,full_amount_summary
            
            else:
                raise Exception("the record doesnt exists in the database")
            
        if db == "outcome":
            full_amount_summary = self.db[1].objects.filter(month__range=(first_day,last_day)).all().values_list().aggregate(self.db_func[0]('amount'))["amount__sum"]
            month_year_repr= (first_day_datetime_object.strftime("%B")[0:3] +" "+ (first_day_datetime_object.strftime("%Y"))[2:])

            if full_amount_summary: 
                return month_year_repr,full_amount_summary
            
            else:
                raise Exception("the record doesnt exists in the database")
        
        #else here if the db name is invalid
        else:
            raise Exception("invalid db name")


    def sum_by_range(self,start_date:str,end_date:str,db:str):
        """
        queries the database and returning two lists of months and the amount in this month
        example:["november"][1000]

        Attributes:
            start_date (str): the start date for the year range query
            end_date (str): the last date for the year range query
            db (str): database str repr.
            db_func (object): the object of the django database aggregate functions

        """

        #the data can be stored not ordered by the dates in the sql so the query below orders it by months
        months_query_set = self.db[0].objects.filter(month__range=(start_date,end_date)).all().order_by("month").values_list()

        #checking if the input of the start and end date was valid if not raises exeption
        if not months_query_set:
            raise Exception("invalid records input or the record not exists")

        #checking if the sql query is valid 
        if months_query_set:

            #this list will contain only the unique months and years
            #this needed if there are more than one record in the same day-month-year in the sql 
            unique_year_month_list = []
            for month in months_query_set:
                if ((datetime.datetime.strftime(month[1],"%Y-%m"))+"-01") in unique_year_month_list:
                    continue
                else:
                    unique_year_month_list.append((datetime.datetime.strftime(month[1],"%Y-%m"))+"-01")
            

            #string repr of the months and years
            period = []
            #each month total sum of the income\outcome
            full_summary = []
            #here its the full calculation of the sum_by_range
            #iterates over the unique months list
            for unique_date in unique_year_month_list:
                #calculating each unique date full month
                calculated_period_sum = self.sum_single_month(unique_date,db)

                #saving the month-year of result in the period list
                period.append(calculated_period_sum[0])

                #saving the result of the sum in the full_summary list
                full_summary.append(calculated_period_sum[1])

            #return two lists with the months and sums
            return full_summary,period


    def get_data_by_year(self,args:list,**kwargs:str):
        """
        sum of all the dates in the specified year.

        Attributes:
            args (list(int)): must get a list of the years that have to be queried
            kwargs(dict(str)) : must contain str name of the database that is required to query
        """

        #the choosen database
        database = kwargs["kwargs"]["db"]
        #the choosen year list
        year_range = args

        if database == "income":
            yearly_sum_dict = {}
            for year in year_range:
                start = f"{year}-01-01"
                end = f"{year}-12-31"

                full_sum = self.db[0].objects.filter(month__range=(start,end)).aggregate(self.db_func[0]("amount"))['amount__sum']
                yearly_sum_dict[year] = full_sum

            return yearly_sum_dict

        if database == "outcome":
            yearly_sum_dict = {}
            for year in year_range:
                start = f"{year}-01-01"
                end = f"{year}-12-31"

                full_sum = self.db[1].objects.filter(month__range=(start,end)).aggregate(self.db_func[0]("amount"))['amount__sum']
                yearly_sum_dict[year] = full_sum

        return yearly_sum_dict
    
