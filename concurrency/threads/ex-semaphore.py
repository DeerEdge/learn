import threading
import time

sem = threading.Semaphore(3)
active = 0
peak = 0
peak_lock = threading.Lock()

def use_connection(i):
    global active, peak
    with sem:
        with peak_lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.1)  # simulate work while holding a "connection"
        with peak_lock:
            active -= 1

threads = [threading.Thread(target=use_connection, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("peak concurrent:", peak)  # never exceeds 3
