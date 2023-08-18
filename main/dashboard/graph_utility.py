import plotly.express as px
import pandas as pd

#comments for development only#

#class that will create graph with the parameters that i will choose and there will be 
#option to display it as html or image that will be saved in the static folder

class graph_creator(object):
    def __init__(self):

        self.template = 'plotly_dark'

        

    
    def bar_graph(self,group:list,value:list,path=None,to_html=True):
        data_frame = pd.DataFrame(dict(group=group,value=value))

        graph_fig = px.bar(data_frame,x='group',y='value')
        if to_html:
            graph = graph_fig.to_html()
        else:
            graph = graph_fig.write_image(path)
        return graph

    def pie_graph(self,values:list,names:list,path=None,to_html=True):

        pie_fig = px.pie(values=values,names=names,template=self.template)

        if to_html:
            graph = pie_fig.to_html()
        else:
            pie_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            pie_fig.update_traces(textposition="outside",textfont_size=30,textinfo='percent+label')
            graph = pie_fig.write_image(path)
        return graph


    def donut_graph(self,values:list,names:list,path="",to_html=True):
        donut_fig = px.pie(values = values,template=self.template,
                names = names,
                color = ['G1', 'G2', 'G3', 'G4'],
                hole = 0.5)
        #the bg color of the pie
        donut_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        #text position and the font size udjustments
        donut_fig.update_traces(textposition="outside",textfont_size=30,textinfo='percent+label')
        if to_html:
            graph = donut_fig.to_html()
        
        else:
            graph = donut_fig.write_image(path)
        return graph
    