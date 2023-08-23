class graph_presentation(object):
    def __init__(self,calculations,presentation='card'):
        self.calculations = calculations
        self.presentation = presentation


    def user_card(self,user_data):
        """returns html card with the user data that recieved from the user"""

        username = user_data['username']
        user_position = user_data['user_position']
        picture = user_data['picture']
        card_html = """<div class="card">
        <div class="card-body">
          <h5 class="card-title">{}</h5>
          <h6 class="card-subtitle mb-2 text-body-secondary">{}</h6>

          <img
            src={}
            class="card-img-top"
            alt="..."
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
        </div>""".format(username,user_position,picture)
        
        return card_html
    
    
    def graph_card(self,user_data,user_calc):
        """returns html card with the graph data that recieved from users queries"""
        pass
    

    def test(self):
      """test method that creates an instance and prints the html returns with test data """
      instance = graph_presentation(calculations='calc')
      data = instance.user_card({'username':'test user','user_position':'test team','picture':'"employer/images/photo.png"'})
      print(data)



#uncomment if you want to test the class 
# test_instance = graph_presentation('calc')
# test_instance.test()