import socket
from helper import *

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 1234

try:
  client_socket.connect((HOST, PORT))
except:
  print "Server is not active"
  exit(1)

while True:
  print "Enter username and password"
  username = raw_input()
  password = raw_input()
  client_socket.send(username + "#" + password)
  response =  client_socket.recv(1024)
  status = Helper.validate_login_access(response)
  if status == "success":
    break
  elif status == "terminate":
    print colored("Closing client....", 'red')
    client_socket.close()
    exit(1)


class Client: 
  @staticmethod
  def get_server_name_ip(client_socket):
    response = client_socket.recv(1024)
    if response == 'ack':
      organisation_name = raw_input("Enter organisation name:  ")
      client_socket.send(organisation_name)
      organisation = client_socket.recv(1024)
      if organisation == "not_found":
        print "Organisation is not found"
      else:
        Helper.format_response(organisation)

  @staticmethod
  def get_statistics(client_socket):
    response = client_socket.recv(1024)
    Helper.format_response(response)

  @staticmethod
  def add_new_organisation(client_socket):
    organisation_name = raw_input("Enter organisation name:  ")
    server_name = raw_input("Enter server name:  ")
    ip_address = raw_input("Enter ip address:  ")
    connection_time = raw_input("Enter connection time:  ")

    organisation = {
      'organisation_name' : organisation_name,
      'server_name' : server_name,
      'ip_address' : ip_address,
      'connection_time' : connection_time
    }
    organisation = json.dumps(organisation)
    client_socket.send(organisation)
    message = client_socket.recv(1024)
    print message

  @staticmethod
  def remove_organisation(client_socket):
    organisation_name = raw_input("Enter organisation name:  ")
    client_socket.send(organisation_name)
    message = client_socket.recv(1024)
    print message

  @staticmethod
  def quit_program(client_socket):
    raise KeyboardInterrupt("Error")

print "-------------------------------------------------------"
print "                     Menu                              "
print "-------------------------------------------------------"
print "(1) Get server name and IP"
print "(2) Get statistics (mean, median, minimum, maximum)"
print "(3) Add new organisation"
print "(4) Remove organisation"
print "(5) Quit program"

while True:
  try:
    option = input("Enter you choice (1, 2, 3, 4 or 5):  ")
    option = int(option)
    method = Helper.OPTION_TO_METHOD_MAPPING[option]
    client_socket.send(str(option))
    getattr(Client, method)(client_socket)
  except Exception:
    print("Invalid option..")
  except KeyboardInterrupt:
    print "Closing client"
    client_socket.close()
    exit(1)