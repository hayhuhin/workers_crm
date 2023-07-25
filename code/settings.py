import json  # for later to get the data from local file

# Opening JSON file
with open('/etc/workers_crm.json') as json_data:
    data = json_data.read()
    parsed_json = json.loads(data)


USERNAME = 'root'
PASSWORD = parsed_json['data']
