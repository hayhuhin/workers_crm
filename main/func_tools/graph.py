import plotly.express as px
import pandas as pd
from pathlib import Path
import calendar
import datetime


#TESTING 
# from dashboard.models import Income
# from django.db.models import Sum



# from dashboard.models import Position_responsabilities

class graph_presentation(object):
    def __init__(self,presentation='card'):
        self.presentation = presentation
        self.template = 'plotly_dark'
        self.currant_path = Path.cwd()
    
    def bar_graph(self,group:list,value:list,path=None,to_html=True):
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




# fig = px.scatter(df, x="total_bill", y="tip", facet_col="sex",
#                  width=800, height=400)

# fig.update_layout(
#     margin=dict(l=20, r=20, t=20, b=20),
#     paper_bgcolor="LightSteelBlue",
# )






    def pie_graph(self,values:list,names:list,path='',to_html=True):
        path = str(self.currant_path) +"/employer_profile/static/employer/images/pie.png"


        pie_fig = px.pie(values=values,names=names,template=self.template)
        pie_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        pie_fig.update_traces(textfont_size=12,textinfo='percent+label')


        if to_html:
            graph = pie_fig.to_html()
        else:
            graph = pie_fig.write_image(path)
        return graph


    def donut_graph(self,values:list,names:list,path="",to_html=True):
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
    

    def test(self):
      """test method that creates an instance and prints the html output of the graphs"""
      instance = graph_presentation(calculations='calc')
      data = instance.user_card({'username':'test user','user_position':'test team','picture':'employer/images/photo.png'})
      print(data)




class graph_queries:
    def __init__(self):
        self.data = []
    
    def task_completion(self,user):
      # task = Position_responsabilities.objects.get(id=2)
      task = 'radco'
      users_task_objects = user.employer.job_position
      record = users_task_objects
      test_record = task
      print(test_record)



def employer_data_extraction(request):
    first_name = request.user.employer.first_name
    last_name = request.user.employer.last_name
    department = request.user.employer.job_position.position
    rank = request.user.employer.job_position.rank 
    profile_pic = request.user.employer.profile_pic.url

    request_data = {'username':first_name+" "+last_name,'job_position':department,'job_rank':rank,'profile_pic':profile_pic}
    return request_data



start = "2024-10-01"
end = "2024-10-30"



def sum_month(start,db,db_func):
    """ gets the start date then Sum all amounts that is exists in this started month"""
    
    start_date = datetime.datetime.strptime(start,"%Y-%m-%d").date()
    print(start_date)
    end = start_date.replace(day = calendar.monthrange(start_date.year, start_date.month)[1])

    all_months_test = db.objects.filter(month__range=(start_date,end)).all().values_list().aggregate(db_func('amount'))

    date_list = str(start_date) + " - " + str(end)
    summary_list = all_months_test['amount__sum']

    return date_list,summary_list



def sum_date_by_range(start_date,end_date,db,db_func):
  """ calculates the whole range of months and returns two lists of summary by months and list of the months themselves"""
  months_query_set = db.objects.filter(month__range=(start_date,end_date)).all().order_by("month").values_list()

  unique_year_month_set = set()
  for month in months_query_set:
      unique_year_month_set.add((datetime.datetime.strftime(month[1],"%Y-%m"))+"-01")
  
  # print(unique_year_month_set)

  sum_by_period = []
  full_summary = []
  for unique_date in unique_year_month_set:
  
    calculated_period_sum = sum_month(unique_date,db,db_func)
    sum_by_period.append(calculated_period_sum[0])
    full_summary.append(calculated_period_sum[1])


  # return sum_by_period
  return full_summary,sum_by_period




def save_the_graph(graph_html):
    """saves the graph query and users detailes in log file 
        return: the graph html 
    """
    #TODO add the write&read into file later
    user_data = []
    return graph_html
    

class GraphHandler:
    """ graph handler takes the users input saves it for reusage and have methods that return graph representation as html """
    def __init__(self,user,db:list,db_func:list,last_save):
        self.user = user
        self.last_save = last_save
        # self.start_date = self.start_date()
        # self.end_date = self.end_date()
        self.db = db 
        self.db_func = db_func

    def graph_log(self,graph_html):
        """ in the future will save the data in log folder with log file of graph repr and the user that used it"""
        
        return graph_html
        
    def last_save(self):
        user = None
        databases = None
        functions = None
        _repr = None

    def sum_by_range(self,start_date,end_date):
        self.start_date(start_date)
        self.end_date(end_date)

        graph_data_lists = sum_date_by_range(start_date,end_date,self.db[0],self.db_func[0])

        graph_repr_inst = graph_presentation()
        graph_repr_inst.bar_graph(group=graph_data_lists[1],value=graph_data_lists[0],path="/")

        return graph_repr_inst





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