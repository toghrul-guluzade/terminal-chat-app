from cryptography.fernet import Fernet
import csv
import os
import authentication as auth
import socket
import threading

connected_clients = {} # Dictionary to store connected clients and lively updates

#Function to handle each client
def handle_client(client_socket, client_address):
  print("Connection from: ", client_address)
  client_socket.send(b"Welcome to the server") # Send welcome message to client
  client_socket.settimeout(300) # Set timeout for the connection
  try:
    while True:
      try:
        message = client_socket.recv(1024).decode() # Receive message from client
        if not message:  # Client disconnected
            print(f"Client {client_address} disconnected.")
            break
        print("Client: ", message) # Print message from client in case of connection input

        for username, ip in list(connected_clients.items()): # Remove client from connected clients if they time out
          if ip == client_address[0]:
            del connected_clients[username]
            print(f"Removed {username} from connected clients")
            break

        if message == "auth": 
            auth_check = authentication(client_socket)
            if auth_check:
                options(client_socket, auth_check)
        else:
            client_socket.send(b"Invalid input. Disconnecting...")
            break
      except socket.timeout:
        print(f"Client {client_address} timed out. Disconnecting...")
        for username, ip in list(connected_clients.items()):
          if ip == client_address[0]:
            del connected_clients[username]
            print(f"Removed {username} from connected clients")
        break
            
  except Exception as e:
        print(f"Error handling client {client_address}: {e}")



def authentication(client_socket):
  client_socket.send(b"Do you want to sign up(0) or sign in?(1): ")
  condition = client_socket.recv(1024).decode()

  if condition == "0":
    client_socket.send(b"Enter username for sign up: ")
    username = client_socket.recv(1024).decode()
    client_socket.send(b"Enter password: ")
    password = client_socket.recv(1024).decode()
    auth.userSignUp(username, password)
    client_socket.send(b"User signed up successfully")
  elif condition == "1":
    client_socket.send(b"Enter username for sign in: ")
    username = client_socket.recv(1024).decode()
    client_socket.send(b"Enter password: ")
    password = client_socket.recv(1024).decode()
    if auth.userSignIn(username, password):
      client_socket.send(b"User signed in")
      client_ip = client_socket.getpeername()[0]
      connected_clients.update({username: client_ip})
      print(connected_clients)
      return True
    else: 
      client_socket.send(b"Invalid credentials")
  else:
    client_socket.send(b"Invalid input. Disconnecting...")
    client_socket.close()
    return False

def options(client_socket, auth_check):
  if auth_check == True:
    client_socket.send(b"Options: \n1. List the active users\n2. Send a message to a user\n3. Send a message to all users\n4. Sign out\nEnter your choice: ")
    choice = client_socket.recv(1024).decode()
    if choice == "1":
      client_socket.send(str(connected_clients).encode())
    elif choice == "2":
      client_socket.send(b"Enter the username of the user you want to send a message to: ")
    elif choice == "3":
      broadcast_message = True
    elif choice == "4":
      print("Signing out")
    else:
      client_socket.send(b"Invalid input. Disconnecting...")
      client_socket.close()
  
def start_server():
  while True:
    client_socket, client_address = server_socket.accept()
    # Create new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.daemon = True
    client_thread.start()
    
if __name__ == "__main__":
  

  server_socket = socket.socket()
  server_ip = '192.168.1.68'
  port = 53147

  server_socket.bind((server_ip, port))
  server_socket.listen(5)
  print("Server is up and running")
  print(connected_clients)

  start_server()
  