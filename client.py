import socket
import time
import threading

def close_socket(sock):
  """Gracefully shutdown and close a socket."""
  if sock:  # Check if the socket object exists
    try:
      sock.shutdown(socket.SHUT_RDWR)  # Shut down both send and receive
    except OSError as e:
      if e.errno != 10038:  # Ignore error if it's already closed
        print(f"Error during socket shutdown: {e}")
    except Exception as e:
      print(f"Unexpected error during socket shutdown: {e}")
    finally:
      try:
        sock.close()  # Always attempt to close the socket
        print("Socket closed.")
      except OSError as e:
        if e.errno != 10038:  # Ignore already closed error
          print(f"Error during socket close: {e}")
      except Exception as e:
        print(f"Unexpected error during socket close: {e}")



# Client side code
def input_with_timeout(timeout=10):
    """Custom input function with a timeout."""
    user_input = [None]  # Mutable container to store the input

    def get_input():
        """Get input from the user."""
        user_input[0] = input()

    # Create a thread to get user input
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True  # Ensure the thread doesn't block program exit
    input_thread.start()

    # Wait for the thread to complete or timeout
    input_thread.join(timeout)
    if input_thread.is_alive():
        raise TimeoutError("Input timed out.")

    return user_input[0]

def main():
  client_socket = socket.socket()

  server_ip = '192.168.1.68' # Change this to the IP address of the server
  server_port = 53147 # Change this to the port number of the server

  client_socket.settimeout(300)
  # Set timeout for the connection
  client_socket.connect((server_ip, server_port)) # Connect to the server
  print("Connected to server at: ", server_ip, server_port)

  try: 
    
    server_message = client_socket.recv(1024).decode() # Receive welcome message from server
    print("Server: ", server_message)
    time.sleep(.5)

    while True:
      server_message = client_socket.recv(1024).decode() # Receive message from server
      print("Server: ", server_message, end=" ")

      if "Enter" in server_message or "Options" in server_message or "Do you want" in server_message:
        try:
          user_input = input_with_timeout(10) 
          client_socket.send(user_input.encode()) # Send message to server
        except TimeoutError as e:
          server_message = client_socket.recv(1024).decode() # Receive message from server
          print("\nServer: ", server_message)
          print("Input timed out. Disconnected")
          close_socket(client_socket)
          break

      if "Disconnecting" in server_message or "Disconnected" in server_message:  # Close the connection if server is disconnecting
        print("\nServer closed the connection")
        close_socket(client_socket)
        break
      time.sleep(.5)


  except ConnectionRefusedError:
    print("Server is not up and running")
    

  except TimeoutError:
    print("\nConnection timed out. Server is not responding")

  except Exception as e:
    print("An error occurred: ", e)
  

  finally:
    close_socket(client_socket)

if __name__ == "__main__":
  main()



