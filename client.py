import socket
import time
import threading
from colorama import Style, Fore

def close_socket(sock):
  """Gracefully shutdown and close a socket."""
  if sock:  # Check if the socket object exists
    try:
      sock.shutdown(socket.SHUT_RDWR)  # Shut down both send and receive
    except OSError as e:
      if e.errno != 10038:  # Ignore error if it's already closed
        print(f"{Fore.RED}Error during socket shutdown: {e}{Style.RESET_ALL}")
    except Exception as e:
      print(f"{Fore.RED}Unexpected error during socket shutdown: {e}{Style.RESET_ALL}")
    finally:
      try:
        sock.close()  # Always attempt to close the socket
        print(Fore.CYAN + "Socket closed." + Style.RESET_ALL)
      except OSError as e:
        if e.errno != 10038:  # Ignore already closed error
          print(f"{Fore.RED}Error during socket close: {e}{Style.RESET_ALL}")
      except Exception as e:
        print(f"{Fore.RED}Unexpected error during socket close: {e}{Style.RESET_ALL}")



# Client side code
#Function for disconnecting when server awaits for a long time without getting answer from client
def input_with_timeout(timeout):
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
        raise TimeoutError(Fore.RED + "Input timed out." + Style.RESET_ALL)

    return user_input[0]

def main():
  client_socket = socket.socket()

  server_ip = '192.168.1.68' # Change this to the IP address of the server
  server_port = 53147 # Change this to the port number of the server

  socket_closed_check = False
  #client_socket.settimeout(300)
  # Set timeout for the connection
  client_socket.connect((server_ip, server_port)) # Connect to the server
  print(Fore.GREEN, "Connected to server at: ", server_ip, server_port, Style.RESET_ALL)
  
  last_received_time = time.time()
  server_awaits = False

  try: 
    
    server_message = client_socket.recv(1024).decode() # Receive welcome message from server
    print(Fore.LIGHTBLUE_EX, "Server: ", Style.RESET_ALL, server_message)

    while True:
      try: 
        client_socket.settimeout(1)
        server_message = client_socket.recv(1024).decode() # Receive message from server
        last_received_time = time.time()
        print(Fore.LIGHTBLUE_EX, "Server: ", Style.RESET_ALL, server_message, end="")
          
        if "Enter" in server_message or "Options" in server_message or "Do you want" in server_message:
          
          server_awaits = True
          try:
            user_input = input_with_timeout(10)
 
            client_socket.send(user_input.encode()) # Send message to server
            server_awaits = False
          except TimeoutError:
            print(Fore.RED, "\nInput timed out while waiting. Disconnecting...", Style.RESET_ALL)
            close_socket(client_socket)
            socket_closed_check = True
            break

        if "Disconnecting" in server_message or "Disconnected" in server_message:  # Close the connection if server is disconnecting
          print(Fore.CYAN, "\nServer closed the connection", Style.RESET_ALL)
          close_socket(client_socket)
          socket_closed_check = True
          break
        #time.sleep(.5)
      
      except socket.timeout:
        if not server_awaits and time.time() - last_received_time >= 5:
          print(Fore.LIGHTGREEN_EX, "\nEnter your message: ", Style.RESET_ALL, end="")
          try: 
            user_input = input_with_timeout(10)
            client_socket.send(user_input.encode())
            last_received_time = time.time
          except TimeoutError:
            print(Fore.RED, "Input timed out. Disconnecting...", Style.RESET_ALL)
            close_socket(client_socket)
            socket_closed_check = True
            break

  except KeyboardInterrupt:
    print("Keyboard Interrupt ")

  except ConnectionRefusedError:
    print("Server is not up and running")
    

  except TimeoutError:
    print("\nConnection timed out. Server is not responding")

  except Exception as e:
    print("An error occurred: ", e)
  

  finally:
    if not socket_closed_check:
      close_socket(client_socket)

if __name__ == "__main__":
  main()



