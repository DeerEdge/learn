import threading
import time

done = False

def worker(text):
    counter = 0
    while True:  # without daemon use done flag
        time.sleep(1)
        counter += 1
        print(text, counter)

# target the function to be run and pass in all args through args parameter
t1 = threading.Thread(target=worker, daemon=True, args=("ABC",))
t2 = threading.Thread(target=worker, daemon=True, args=("XYZ",))

# start the threads
t1.start()
t2.start()

# await until both are done, keep going
t1.join()
t2.join()

input("Enter to quit")
done = True
