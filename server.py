import socket
from threading import Thread
from helper import *
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 1234

server_socket.bind((HOST, PORT))
server_socket.listen(5)

class Client (Thread):
  def __init__(self, connection, client_addr):
    Thread.__init__(self)
    self.connection = connection
    self.client_addr = client_addr

  def run(self):
    #Sending a greeting message
    try:
      (valid, username) = validate_client(connection)
      if not valid:
        return

      #make user as active  
      self.username = username
      Helper.add_user_to_active(username)

      #waiting for input from client
      while True:
        option = self.connection.recv(1024).decode('utf-8')
        if not option:
          raise Exception('Client is disconnected')
        method = Helper.OPTION_TO_METHOD_MAPPING[int(option)]
        getattr(self, method)()

    except Exception as e:
      print("Client is disconnected")
      if hasattr(self, 'username'):
        Helper.remove_user_from_active(self.username)
      return

  def get_server_name_ip(self):
    self.connection.send('ack'.encode('utf-8'))
    organisation_name = self.connection.recv(1024).decode('utf-8')
    organisation = Helper.find_organisation(organisation_name)
    self.connection.send(organisation.encode('utf-8'))

  def get_statistics(self):
    statistics = Helper.get_statistics()
    self.connection.send(statistics.encode('utf-8'))

  def add_new_organisation(self):
    organisation = self.connection.recv(1024).decode('utf-8')
    status = Helper.add_new_organisation(organisation)
    self.connection.send(status.encode('utf-8'))

  def remove_organisation(self):
    organisation_name = self.connection.recv(1024).decode('utf-8')
    status = Helper.remove_organisation(organisation_name)
    self.connection.send(status.encode('utf-8'))

  def quit_program(self):
    pass

def create_client(connection, client_addr):
  client = Client(connection, client_addr)
  client.start()

def validate_client(connection):
  #validates username and password
  for index in [1,2,3]:
    print("Waiting for username and password")
    credentials = connection.recv(1024).decode('utf-8')
    print("Credentials received")
    (valid, username, response) = Helper.authenticate(credentials)
    print(response)
    connection.send(Helper.validate_and_format_response(response, index).encode('utf-8'))
    if valid:
      return True, username
  return False, username

while True:
  try:
    connection, client_addr = server_socket.accept() 
    print(client_addr)
    create_client(connection, client_addr)
  except KeyboardInterrupt:
    print("Closing server")
    Helper.close_all_active_users()
    server_socket.close()
    os._exit(1)