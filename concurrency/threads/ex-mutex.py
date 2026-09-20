import threading
import time

lock = threading.Lock()
counter = 0

def increment():
    global counter
    for _ in range(1_000):
        with lock:
            temp = counter
            time.sleep(0)  
            counter = temp + 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter) 
