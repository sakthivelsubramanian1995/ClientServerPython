import socket
from helper import *

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 1234

try:
  client_socket.connect((HOST, PORT))
except:
  print("Server is not active")
  exit(1)

while True:
  try:
    print("Enter username and password")
    username = input()
    password = input()
    credentials = username + "#" + password
    client_socket.send(credentials.encode('utf-8'))
    response =  client_socket.recv(1024).decode('utf-8')
    status = Helper.validate_login_access(response)
    if status == "success":
      break
    elif status == "terminate":
      raise Exception("terminate")
  except:
    print("Closing client....")
    client_socket.close()
    exit(1)

class Client: 
  @staticmethod
  def get_server_name_ip(client_socket):
    response = client_socket.recv(1024).decode('utf-8')
    if response == 'ack':
      organisation_name = input("Enter organisation name:  ")
      client_socket.send(organisation_name.encode('utf-8'))
      organisation = client_socket.recv(1024).decode('utf-8')
      if organisation == "not_found":
        print("Organisation is not found")
      else:
        Helper.format_response(organisation)

  @staticmethod
  def get_statistics(client_socket):
    response = client_socket.recv(1024).decode('utf-8')
    Helper.format_response(response)

  @staticmethod
  def add_new_organisation(client_socket):
    organisation_name = input("Enter organisation name:  ")
    server_name = input("Enter server name:  ")
    ip_address = input("Enter ip address:  ")
    connection_time = input("Enter connection time:  ")

    organisation = {
      'organisation_name' : organisation_name,
      'server_name' : server_name,
      'ip_address' : ip_address,
      'connection_time' : connection_time
    }
    organisation = json.dumps(organisation)
    client_socket.send(organisation.encode('utf-8'))
    message = client_socket.recv(1024).decode('utf-8')
    print(message)

  @staticmethod
  def remove_organisation(client_socket):
    organisation_name = input("Enter organisation name:  ")
    client_socket.send(organisation_name.encode('utf-8'))
    message = client_socket.recv(1024).decode('utf-8')
    print(message)

  @staticmethod
  def quit_program(client_socket):
    raise KeyboardInterrupt("Error")

print("-------------------------------------------------------")
print("                     Menu                              ")
print("-------------------------------------------------------")
print("(1) Get server name and IP")
print("(2) Get statistics (mean, median, minimum, maximum)")
print("(3) Add new organisation")
print("(4) Remove organisation")
print("(5) Quit program")

while True:
  try:
    option = input("Enter you choice (1, 2, 3, 4 or 5):  ")
    option = int(option)
    method = Helper.OPTION_TO_METHOD_MAPPING[option]
    client_socket.send(str(option).encode('utf-8'))
    getattr(Client, method)(client_socket)
  except Exception:
    print("Invalid option..")
  except KeyboardInterrupt:
    print("Closing client")
    client_socket.close()
    exit(1)