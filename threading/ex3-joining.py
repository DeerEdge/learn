import threading
import time

glob_list = []

def count(n):
    for i in range(1, n+1):
        print("t1", i)
        glob_list.append(i)
        time.sleep(0.05)
    
def count2(n):
    for i in range(1, n+1):
        print("t2", i)
        glob_list.append(i)
        time.sleep(0.05)

t1 = threading.Thread(target=count, args=(5,))
t1.start()

t2 = threading.Thread(target=count2, args=(5,))
t2.start()

# don't move past this point until both threads are done
t1.join()
t2.join()

time.sleep(0.1)
print("glob_list", glob_list)
print("done")

