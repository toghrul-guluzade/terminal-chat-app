from cryptography.fernet import Fernet
import csv
import os


#This file contains functions for user authentication

#Generate a key for encryption
if not os.path.exists("key.txt"):
  key = Fernet.generate_key()
  with open("key.txt", "wb") as file:
    file.write(key)

  with open("key.txt", "rb") as file:
    key = file.read()
else:
  with open("key.txt", "rb") as file:
    key = file.read()

#Function to sign up a user
def userSignUp (username, password):
  password = Fernet(key).encrypt(password.encode())
  with open ("users.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["username", "password"])
    if file.tell() == 0: writer.writeheader()
    writer.writerow({"username": username, "password": password.decode()})
  return True

#Function to sign in a user
def userSignIn(username, password):
    password = password.encode()
    found = False  # Add a flag to track if user is found
    
    with open("users.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                found = True  # Set flag when user is found
                stored_password = Fernet(key).decrypt(row["password"].encode())
                if stored_password == password:
                    print("Welcome, ", username)
                    return True
                    break
        
        if not found:  # Handle case when username is not found
            print("User not found")
            return False

    