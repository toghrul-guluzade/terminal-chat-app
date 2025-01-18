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
