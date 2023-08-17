import plotly.express as px
import pandas as pd

#comments for development only#

#class that will create graph with the parameters that i will choose and there will be 
#option to display it as html or image that will be saved in the static folder

class graph_creator(object):
    def __init__(self,args,to_html=True,**kwargs):
        self.args = args
        self.kwargs = kwargs
        self.to_html = to_html

        

    
    def bar_graph(self,group:list,value:list):
        data_frame = pd.DataFrame(dict(group=group,value=value))

        graph_fig = px.bar(data_frame,x='group',y='value')
        if self.to_html:
            graph = graph_fig.to_html()
        else:
            graph = graph_fig.to_image()

    def pie_graph(self,values:list,names:list):

        pie_fig = px.pie(values=values,names=names)

        if self.to_html:
            graph = pie_fig.to_html()
        else:
            graph = pie_fig.to_image()


    def donut_graph(self,values:list,names:list):

        # donut_fig = px.pie
        pass