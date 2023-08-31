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

        graph_fig = px.bar(data_frame,x='group',y='value')
        if to_html:
            graph = graph_fig.to_html()
        else:
            graph = graph_fig.write_image(path)
        return graph


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
                hole = 0.5)
        #the bg color of the pie
        donut_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
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
        # picture = user_data['picture']
        card_html = """<div class="card">
        <div class="card-body">
          <h5 class="card-title">{}</h5>
          <h6 class="card-subtitle mb-2 text-body-secondary">{}</h6>

          <img
            src=''
            class="card-img-top"
            alt=""
          />
          <p class="card-text">100 leads - this month.</p>
          <p class="card-text">100,000 revenue - this month.</p>
        </div>
        <div class="card-footer text-body-secondary">
          <div class="container">
            <div class="row">
              <div class="col-sm-auto" style="margin-top: 15px">
                <a href="#" class="btn btn-success">EDIT</a>
              </div>
            </div>
          </div>
        </div>""".format(username,user_position)
        
        return card_html
    
    
    def graph_card(self,user_data,user_calc):
        """returns html card with the graph data that recieved from users queries"""

        card_html = """<div class="col border border-info border-1 "style='width:350px;height:450px'>
                          <div class="ms-3"> 
                          <h3>{}</h3>
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