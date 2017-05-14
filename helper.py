import json

class Helper:
  OPTION_TO_METHOD_MAPPING = {
    1 : "get_server_name_ip",
    2 : "get_statistics",
    3 : "add_new_organisation",
    4 : "remove_organisation",
    5 : "quit_program"
  }

  keys = {
    'server_name' : 'Server Name',
    'ip_address' : 'IP Address',
    'no_of_minutes' : 'No of minutes',
    'min_time' : 'Min time',
    'max_time' : 'Max time',
    'mean_time' : 'Mean time',
    'median_time' : 'Median time'
  }

  @staticmethod
  def add_user_to_active(username):
    with open("active_users.txt", "a") as file:
      file.write(username + "\n")

  @staticmethod
  def remove_user_from_active(username):
    f = open("active_users.txt","r")
    lines = f.readlines()
    f.close()
    f = open("active_users.txt","w")
    for line in lines:
      if line.strip() != username:
        f.write(line)
    f.close()

  @staticmethod
  def remove_organisation(organisation_name):
    try:
      f = open("organisations.txt","r")
      lines = f.readlines()
      f.close()
      f = open("organisations.txt","w")
      for line in lines:
        name = line.split()[0]
        if name.lower() != organisation_name.lower():
          f.write(line)
      f.close()
      return "Removing organisation is successful"
    except:
      return "Removing organisation failed"

  @staticmethod
  def find_organisation(organisation_name):
    with open("organisations.txt") as file:
      for line in file:
        (name, server_name, ip_address, no_of_minutes) = line.split()
        if name.lower() == organisation_name.lower():
          org_details = {
            'server_name' : server_name,
            'ip_address' : ip_address,
            'no_of_minutes' : no_of_minutes
          }
          return json.dumps(org_details)
    return "not_found"

  @staticmethod
  def get_all_organisations():
    organisations = []
    with open("organisations.txt") as file:
      for line in file:
        (name, server_name, ip_address, no_of_minutes) = line.split()
        org_details = {
            'name' : name,
            'server_name' : server_name,
            'ip_address' : ip_address,
            'no_of_minutes' : no_of_minutes
          }
        organisations.append(org_details)
    return organisations

  @staticmethod
  def get_statistics():
    organisations = Helper.get_all_organisations()
    connection_times = []
    for organisation in organisations:
      connection_times.append(int(organisation['no_of_minutes']))
    min_time = min(connection_times)
    max_time = max(connection_times)
    total_organisations = len(organisations)
    median = (int)(total_organisations/2)
    median_time = organisations[median]['no_of_minutes']
    mean_time = sum(connection_times) / int(total_organisations)
    return json.dumps({
      'min_time' : min_time,
      'max_time' : max_time,
      'median_time' : median_time,
      'mean_time' : mean_time
    })

  @staticmethod
  def add_new_organisation(organisation):
    try:
      organisation = json.loads(organisation)
      organisation_string = organisation['organisation_name'] + " " + organisation['server_name'] + " " + organisation["ip_address"] + " " + organisation["connection_time"] + "\n"
      with open("organisations.txt", "a") as file:
        file.write(organisation_string)
      return "Organisation successfully added.."
    except:
      return "Organisation add failed.."

  @staticmethod
  def format_response(response):
    response = json.loads(response)
    for key, value in response.items():
      print(Helper.keys[key] or key, " ==>> ", value)

  @staticmethod
  def parse_users():
    users = {}
    try:
      with open('users.txt') as file:
        for line in file:
          (key, value) = line.split()
          users[str(key)] = value
    except:
      pass
    return users

  @staticmethod
  def close_all_active_users():
    with open('active_users.txt', 'w') as file:
      file.truncate()

  @staticmethod
  def get_current_active_users():
    active_users = set()
    try:
      with open('active_users.txt') as file:
        for line in file:
          username = line.strip()
          active_users.add(username)
    except:
      pass
    return active_users

  @staticmethod
  def not_logged_in_already(username):
    current_active_users = Helper.get_current_active_users()
    if username in current_active_users:
      return False
    return True

  @staticmethod
  def authenticate(credentials):
    users = Helper.parse_users()
    (username, password) = Helper.split_credentials(credentials)
    if (username in users) and (users[username] == password):
      if Helper.not_logged_in_already(username):
        return True, username, {"status": "successful", "message" : "You are welcome"}
      else:
        return False, username, {"status": "failed", "stand" : "wait", "message" : "Username is already taken"}
    return False, username, {"status": "failed", "stand" : "wait", "message" : "Invalid username or password"}

  @staticmethod
  def split_credentials(credentials):
    return credentials.split('#')

  @staticmethod
  def validate_and_format_response(response, index):
    if index == 3 and response['status'] == "failed":
      response['stand'] = 'terminate'
      response['message'] = 'You have reached maximum limit of invalid attempts'
    return json.dumps(response)

  @staticmethod
  def validate_login_access(response):
    response = json.loads(response)
    print(response['message'])
    if response['status'] == 'successful':
      return "success"
    return response['stand']