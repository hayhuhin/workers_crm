import plotly.express as px
import pandas as pd
from pathlib import Path
import calendar
import datetime


#? helper function that will be used later inside the class

def employer_data_info(request):
    """method returning dict with the user information"""
    first_name = request.user.employer.first_name
    last_name = request.user.employer.last_name
    department = request.user.employer.job_position.position
    rank = request.user.employer.job_position.rank 
    profile_pic = request.user.employer.profile_pic.url

    request_data = {'username':first_name+" "+last_name,'job_position':department,'job_rank':rank,'profile_pic':profile_pic}
    return request_data


def sum_month(start,db,db_func):
    """sums all records inside the same month and returning two lists :
       one list with the dates another with the summary of all the records inside the same month
    """
    
    start_date = datetime.datetime.strptime(start,"%Y-%m-%d").date()
    # print(start_date)
    end = start_date.replace(day = calendar.monthrange(start_date.year, start_date.month)[1])

    all_months_test = db.objects.filter(month__range=(start_date,end)).all().values_list().aggregate(db_func('amount'))

    date_list = str(start_date) + " - " + str(end)
    summary_list = all_months_test['amount__sum']

    return date_list,summary_list


def sum_date_by_range(start_date,end_date,db,db_func):
  """method that returns two lists:
  1.with the summ of all the records in the same month
  2.with the all months and years
  """

  months_query_set = db.objects.filter(month__range=(start_date,end_date)).all().order_by("month").values_list()

  unique_year_month_set = set()
  for month in months_query_set:
      unique_year_month_set.add((datetime.datetime.strftime(month[1],"%Y-%m"))+"-01")
  
  # print(unique_year_month_set)

  period = []
  full_summary = []
  for unique_date in unique_year_month_set:
  
    calculated_period_sum = sum_month(unique_date,db,db_func)
    period.append(calculated_period_sum[0])
    full_summary.append(calculated_period_sum[1])


  # return sum_by_period
  return full_summary,period



#?graph classes that will do some of the functionality in the website



class graph_presentation(object):
    """graph class that using the plotly.express and pandas .
       class is used for returning plotly graphs in much easier and cleaner way
       each method is returning graph as image or html
    """
    def __init__(self,presentation='card'):
        self.presentation = presentation
        self.template = 'plotly_dark'
        self.currant_path = Path.cwd()

    def graph_options(self,graph_type,group:list,values:list,path=None,to_html=True):
        """method that gives you the option to choose which grap to represent by the graph_type
           arg that must be the same as the name of the func (example:"graph_type")
        """
        if graph_type == self.bar_graph.__name__:
            return self.bar_graph(group=group,value=values,path=path,to_html=to_html)
        if graph_type == self.pie_graph.__name__:
            return self.pie_graph(group=group,value=values,path=path,to_html=to_html)
        if graph_type == self.donut_graph.__name__:
            return self.donut_graph(group=group,value=values,path=path,to_html=to_html)
        if graph_type == self.line_graph.__name__:
            return self.line_graph(values=values,names=group,path=path,to_html=to_html)

    
    def bar_graph(self,group:list,value:list,path=None,to_html=True):
        """this method return the bar graph 
            args:
              group: most of the time its the x line on the graphs
              value: its the y line on the graphs
              path: only used to_html=False and saving the pic in specified path
              to_html : default is true and returns the graph as html repr so it can be loaded in the html template
        """

        data_frame = pd.DataFrame(dict(group=group,value=value))

        graph_fig = px.bar(data_frame,x='group',y='value',template=self.template,width=600)

        graph_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor= 'rgba(0, 0, 0, 0)',margin=dict(l=50,r=20,t=20,b=100))

        graph_fig.update_traces(textfont_size=12)

        graph_fig.update_xaxes(
          tickangle=-45,#the angle of the presentation
          dtick="M1", # sets minimal interval to month
          tickformat="%d.%m.%Y", # the date format you want 
)


        if to_html:
            graph = graph_fig.to_html()
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
            graph = pie_fig.to_html()
        else:
            graph = pie_fig.write_image(path)
        return graph

    def line_graph(self,values:list,names:list,path='',to_html=True):
        

        #! examples 
        # df = px.data.gapminder().query("country=='Canada'")
        # fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
        # fig.show()




        path = str(self.currant_path) +"/employer_profile/static/employer/images/pie.png"
        line_fig = px.line(y=values,x=names,template=self.template)
        line_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor = "rgba(0,0,0,0)")
        line_fig.update_traces(textfont_size=12,text='percent+label')


        if to_html:
            graph = line_fig.to_html()
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
            graph = donut_fig.to_html()
        
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


    def sum_by_range(self,start_date,end_date):
        #TODO add much more functionality to this method that can return the data in more ways

        graph_data_lists = sum_date_by_range(start_date,end_date,self.db[0],self.db_func[0])
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
    
