import plotly.express as px
import pandas as pd
from pathlib import Path
import calendar
import datetime
import plotly.graph_objects as go



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



# class DatabaseExtractor:
#    def __init__(self,databases=list[object],functions=list):
#       self.databases = databases
#       self.functions = functions

#     def sum_month(self,start,d)
   


def sum_single_month(date:str,db:object,db_func:object):
    """
    sums all records inside the same month and returning two lists with data if the records exists 
    if the records not exists it will raise exception message

    Attributes:
      first_day (str) : the starting point of the month(example: "2024-11-01").
      db (object): database instance.
      db_func (object function): database function(example "Sum" object that can be used inside the aggregate method when extracting sql data)
    
    """

    first_day_datetime_object = datetime.datetime.strptime(date,"%Y-%m-%d").date()
    last_day_datetime_object = first_day_datetime_object.replace(day = calendar.monthrange(first_day_datetime_object.year, first_day_datetime_object.month)[1])

    first_day = first_day_datetime_object.strftime("%Y-%m-%d")
    last_day = last_day_datetime_object.strftime("%Y-%m-%d")

    full_amount_summary = db.objects.filter(month__range=(first_day,last_day)).all().values_list().aggregate(db_func('amount'))["amount__sum"]
    month_year_repr= first_day_datetime_object.strftime("%B %Y")

    if full_amount_summary: 
      return month_year_repr,full_amount_summary
    
    else:
       raise Exception("the record doesnt exists in the database")
    


def sum_by_range(start_date:str,end_date:str,db:object,db_func:object):
  """
  queries the database and returning two lists of months and the amount in this month
  example:["november"][1000]

  Attributes:
    start_date (str): the start date for the year range query
    end_date (str): the last date for the year range query
    db (object): the object of the database 
    db_func (object): the object of the django database aggregate functions

  """

  months_query_set = db.objects.filter(month__range=(start_date,end_date)).all().order_by("month").values_list()
  print(start_date,end_date)
#! here somewhere the order is breaking 
  unique_year_month_list = []
  for month in months_query_set:
      # print((datetime.datetime.strftime(month[1],"%Y-%m"))+"-01")

      if ((datetime.datetime.strftime(month[1],"%Y-%m"))+"-01") in unique_year_month_list:
          continue
      else:
        unique_year_month_list.append((datetime.datetime.strftime(month[1],"%Y-%m"))+"-01")
  
  # print(unique_year_month_list)
  
  #string repr of the months and years
  period = []
  #each month total sum of the income\outcome
  full_summary = []

  for unique_date in unique_year_month_list:
  
    calculated_period_sum = sum_single_month(unique_date,db,db_func)
    period.append(calculated_period_sum[0])
    full_summary.append(calculated_period_sum[1])
  return full_summary,period



#?graph classes that will do some of the functionality in the website



class GraphRepresantation(object):
    """graph class that using the plotly.express and pandas .
       class is used for returning plotly graphs in much easier and cleaner way
       each method is returning graph as image or html
    """
    def __init__(self,presentation='card'):
        self.presentation = presentation
        self.template = 'plotly_dark'
        self.currant_path = Path.cwd()

    def graph_options(self,graph_type,dict_values:dict,path=None,to_html=True):
        """method that gives you the option to choose which grap to represent by the graph_type
           arg that must be the same as the name of the func (example:"graph_type")
        """
        if graph_type == self.bar_graph.__name__:
            return self.bar_graph(dict_values=dict_values,path=path,to_html=to_html)
        if graph_type == self.pie_graph.__name__:
            return self.pie_graph(dict_values=dict_values,path=path,to_html=to_html)
        if graph_type == self.donut_graph.__name__:
            return self.donut_graph(dict_values=dict_values,path=path,to_html=to_html)
        if graph_type == self.line_graph.__name__:
            return self.line_graph(dict_values=dict_values,path=path,to_html=to_html)
        if graph_type == "bar_graph_compare":
            return self.bar_graph(dict_values=dict_values,path=path,to_html=to_html,compare=True)
        if graph_type == "line_graph_compare":
            return self.line_graph(dict_values=dict_values,path=path,to_html=to_html,compare=True)

    
    def bar_graph(self,dict_values:dict,path=None,to_html=True,compare=False):
        """this method return the bar graph 
            args:
              group: most of the time its the x line on the graphs
              value: its the y line on the graphs
              path: only used to_html=False and saving the pic in specified path
              to_html : default is true and returns the graph as html repr so it can be loaded in the html template
        """

        group = dict_values["x"]
        value = dict_values["y"]
        data_frame = pd.DataFrame(dict(group=group,value=value))

        graph_fig = px.bar(data_frame,x='group',y='value',template=self.template)


        #,margin=dict(l=50,r=20,t=20,b=100)
        graph_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                modebar={'bgcolor':'rgba(0, 0, 0, 0)'},
                                bargap=0.2,
                                bargroupgap=0.2,
                                # width=300
)

        graph_fig.update_traces(textfont_size=12)

        graph_fig.update_xaxes(
          tickangle=-45,#the angle of the presentation
          dtick="M1", # sets minimal interval to month
          tickformat="%d.%m.%Y", # the date format you want 
)
        if compare:

          values_1 = dict_values["y"]
          values_2 = dict_values["y_2"]
          group = dict_values["x"]

          graph_fig = px.bar(
              x=group,
              y=[values_1, values_2],
              labels={'value': 'Income', 'x':'Date','variable': 'amount'},
              title=dict_values["graph_description"],
              color_discrete_sequence=['blue', 'orange'],  # Set custom colors
              template=self.template,
          )

          # fig.update_layout(barmode='group')
          # graph_fig = px.bar(data_frame,x='group',y='value',template=self.template)
          graph_fig.update_layout(barmode='group',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                  modebar={'bgcolor':'rgba(0, 0, 0, 0)'},
                                  bargap=0.2,
                                  bargroupgap=0.2,)
                                  # width=300


          graph_fig.update_traces(textfont_size=12)

          graph_fig.update_xaxes(
            tickangle=-45,#the angle of the presentation
            dtick="M1", # sets minimal interval to month
            tickformat="%d.%m.%Y",) # the date format you want 
          
          graph = graph_fig.to_html(config={'displayModeBar': True})
          return graph
        
        if to_html:
            graph = graph_fig.to_html(config={'displayModeBar': True})
        else:
            graph = graph_fig.write_image(path)
        return graph


    def pie_graph(self,values:list,names:list,path='',to_html=True):
        """this method return the pie graph 
            args:
              group: most of the time its the x line on the graphs
              value: its the y line on the graphs
              path: only used to_html=False and saving the pic in specified path
              to_html : default is true and returns the graph as html repr so it can be loaded in the html template
        """
        path = str(self.currant_path) +"/employer_profile/static/employer/images/pie.png"

        pie_fig = px.pie(values=values,names=names,template=self.template)
        pie_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        pie_fig.update_traces(textfont_size=12,textinfo='percent+label')


        if to_html:
            graph = pie_fig.to_html(config={'displayModeBar': True})
        else:
            graph = pie_fig.write_image(path)
        return graph

    def line_graph(self,dict_values:dict,path='',to_html=True,compare=False):
        

        #! examples 
        # df = px.data.gapminder().query("country=='Canada'")
        # fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
        # fig.show()

        group = dict_values["x"]
        value = dict_values["y"]

        path = str(self.currant_path) +"/employer_profile/static/employer/images/pie.png"
        line_fig = px.line(y=value,x=group,template=self.template)
        line_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor = "rgba(0,0,0,0)",modebar={'bgcolor':'rgba(0, 0, 0, 0)'},)
        line_fig.update_traces(textfont_size=12,text='percent+label')
        line_fig.update_xaxes(tickangle=-45)

        if compare:
            
          dict_values
          values_1 = dict_values["y"]
          values_2 = dict_values["y_2"]
          group = dict_values["x"]

          line_fig = px.line(
              x=group,
              y=[values_1, values_2],
              labels={'value': 'Income', 'x':'Date','variable': 'amount'},
              title=dict_values["graph_description"],
              color_discrete_sequence=['blue', 'orange'],  # Set custom colors
              template=self.template,
          )

          # fig.update_layout(barmode='group')
          # graph_fig = px.bar(data_frame,x='group',y='value',template=self.template)
          line_fig.update_layout(barmode='group',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                  modebar={'bgcolor':'rgba(0, 0, 0, 0)'},
                                  bargap=0.2,
                                  bargroupgap=0.2,)
                                  # width=300


          line_fig.update_traces(textfont_size=12)

          line_fig.update_xaxes(
            tickangle=-45,#the angle of the presentation
            dtick="M1", # sets minimal interval to month
            tickformat="%d.%m.%Y",) # the date format you want 
          
          graph = line_fig.to_html(config={'displayModeBar': True})
          return graph



        if to_html:
            graph = line_fig.to_html(config={'displayModeBar': True})
        else:
            graph = line_fig.write_image(path)
        return graph


    def donut_graph(self,values:list,names:list,path="",to_html=True):
        """this method return the donut graph 
            args:
              group: most of the time its the x line on the graphs
              value: its the y line on the graphs
              path: only used to_html=False and saving the pic in specified path
              to_html : default is true and returns the graph as html repr so it can be loaded in the html template
        """
        path = str(self.currant_path) +"/employer_profile/static/employer/images/donut.png"

        donut_fig = px.pie(values = values,template=self.template,
                names = names,
                # color = ['G1', 'G2', 'G3', 'G4'],
                hole = 0.5,
                width=400,
                )
        #the bg color of the pie
        donut_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=0,r=20,t=20,b=20))
        #text position and the font size udjustments
        donut_fig.update_traces(textfont_size=12,textinfo='percent+label')#textposition="outside",
        if to_html:
            graph = donut_fig.to_html(config={'displayModeBar': True})
        
        else:
            graph = donut_fig.write_image(path)
        return graph
    

    def user_card(self,user_data):
        """returns html card with the user data that recieved from the user
          the user data must contain 'username','user_position','picture' as a 
          dict 
        """

        username = user_data['username']
        user_position = user_data['job_position']
        profile_pic = user_data['profile_pic']
        # picture = user_data['picture']
        card_html = """<div class="">
        <div class="">

          <img

            src={}
            class="rounded-5 mb-3"
            style="height:225px"
            alt="employer picture"
          />

          <h3 class="text-capitalize mb-2">{}</h3>
        <div class="text-capitalize">
          <a class="nav-link dropdown-toggle mb-5" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            edit details
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">contact details</a></li>
            <li><a class="dropdown-item" href="#">department details</a></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>


          <h5 class="mt-5 mb-3">contact details</h5>
           
          <p class="card-text">phone number: +973 552251273 </p>
          <p class="card-text">position: {} department</p>
          <p class="card-text">department contact number: +1 47577226</p>
          <p class="card-text">department address: vaizman 24 tel-aviv </p>

          <h5 class="mt-5 mb-3">personal details</h5>
          <p class="card-text">age: 33</p>
          <p class="card-text">address: anilevich 28 holon </p>
          <p class="card-text">workers: 0</p>
          <p class="card-text">manager: valeri levinson</p>
          <p class="card-text">department manager: arg argus</p>
          <p class="card-text">description: none</p>

        </div>

      </div>

        <div class="card-footer text-body-secondary">
          <div class="container">
            <div class="row">
              <div class="col-sm-auto" style="margin-top: 15px">
                <a href="#" class="btn btn-success">EDIT</a>
              </div>
            </div>
            </div>
            </div>
          
          
        </div>""".format(profile_pic,username,user_position)
        
        return card_html
    

    def graph_card(self,user_data,user_calc):
        """returns html card with the graph data that recieved from users queries"""

        card_html = """<div class="col"style='width:350px;height:450px'>
                          <div class="ms-3"> 
                          <p class="text-secondary fs-5">- {}</p>
                          <div name="plotly_element">{}</div>
                        </div>
                            </div>""".format(user_data,user_calc)
        
        return card_html
    

    
class GraphCalculator:
    """ graph calculater can 
    """
    def __init__(self,user,db:list,db_func:list,last_save):
        self.user = user
        self.last_save = last_save
        self.db = db 
        self.db_func = db_func


    def graph_log(self,graph_html):
        """ in the future will save the data in log folder with log file of graph repr and the user that used it"""
        
        return graph_html

    def repr_yearly_data(self,args,**kwargs):
      database = kwargs["kwargs"]["db"]
      print(database)
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



    def sum_by_range(self,start_date,end_date):
        #TODO add much more functionality to this method that can return the data in more ways

        graph_data_lists = sum_by_range(start_date,end_date,self.db[0],self.db_func[0])
        return graph_data_lists


    def start_date(self,start):
      if start:
        return start
      else:
          return self.default_view_repr


    def end_date(self,end):
        if end :
          return end
        else:
            return self.default_view_repr

    def default_view_repr(self):
        """returns default graph repr when there is no data present"""
        pass
    
