import socket

# Client side code

def main():
  client_socket = socket.socket()

  server_ip = '192.168.1.68' # Change this to the IP address of the server
  port = 53147 # Change this to the port number of the server

  try: 
    # Set timeout for the connection
    client_socket.settimeout(10)
    client_socket.connect((server_ip, port)) # Connect to the server
    print("Connected to server at: ", server_ip, port)

    while True:
      server_message = client_socket.recv(1024).decode() # Receive message from server
      print("Server: ", server_message)
      if "Disconnecting" in server_message:  # Close the connection if server is disconnecting
        print("Server closed the connection")
        break
      
      user_input = input("Enter message to server: ") 
      client_socket.send(user_input.encode()) # Send message to server

  except ConnectionRefusedError:
    print("Server is not up and running")

  except TimeoutError:
    print("Connection timed out. Server is not responding")

  except Exception as e:
    print("An error occurred: ", e)
  

  finally:
    client_socket.close()

if __name__ == "__main__":
  main()



