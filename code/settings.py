import json  # for later to get the data from local file

# Opening JSON file
with open(r'D:\git_shell\Git\etc\workers_crm.json') as json_data:
    data = json_data.read()
    parsed_json = json.loads(data)


USERNAME = 'root'
PASSWORD = parsed_json['data']

WIDTH = 800
HEIGHT = 800


BG_COLOR = '#121212'
LAYOUT_COLOR = '#1C273D'
