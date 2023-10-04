import plotly.express as px
import pandas as pd
from pathlib import Path
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
