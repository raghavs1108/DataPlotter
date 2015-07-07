import time
import random

refreshSpeed = 50

def update():
    f = open("data.txt", "w")
    r = random.random() *10
    f.write(str(r))
    f.close()
    time.sleep (refreshSpeed / 1000.0);    
    

while True:
    update()
