import threading
import time 

def walk_dog():
    time.sleep(8)
    print("Walking the dog")

def take_out_trash():
    time.sleep(3)
    print("Taking out the trash")

def get_mail():
    time.sleep(5)
    print("Getting the mail")


chore1 = threading.Thread(target=walk_dog)
chore1.start()

chore2 = threading.Thread(target=take_out_trash)
chore2.start()

chore3 = threading.Thread(target=get_mail)
chore3.start()