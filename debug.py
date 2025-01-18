import socket
from cryptography.fernet import Fernet
import csv
import os

if not os.path.exists("chatting//key.txt"):
  key = Fernet.generate_key()
  with open("chatting//key.txt", "wb") as file:
    file.write(key)

  with open("chatting//key.txt", "rb") as file:
    key = file.read()
else:
  with open("chatting//key.txt", "rb") as file:
    key = file.read()

def userSignUp ():
  username = input("Enter your username: ")
  password = Fernet(key).encrypt(input("Enter your password: ").encode())
  with open ("chatting//users.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["username", "password"])
    if file.tell() == 0: writer.writeheader()
    writer.writerow({"username": username, "password": password.decode()})


def userSignIn():
    username = input("Enter your username: ")
    password = input("Enter your password: ").encode()
    found = False  # Add a flag to track if user is found
    
    with open("chatting//users.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                found = True  # Set flag when user is found
                stored_password = Fernet(key).decrypt(row["password"].encode())
                if stored_password == password:
                    print("Welcome, ", username)
                    break
        
        if not found:  # Handle case when username is not found
            print("User not found")

    

#s = socket.socket()
#port = 12345
#s.connect(('192.168.1.69', port))
#print(s.recv(1024))
#s.close()

if __name__ == "__main__":
  condition = input("Do you want to sign up(0) or sign in?(1): ")
  if condition == "0":
    userSignUp()
  elif condition == "1":    
    userSignIn()