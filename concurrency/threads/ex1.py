import threading
import time

def t1():
    print('hello')
    time.sleep(1)
    print('world')
    time.sleep(1.2)
    print('done')

# will create a new thread in addition to the main thread
t = threading.Thread(target=t1)
t.start()
print(threading.active_count())
time.sleep(0.9)
print("before")
