import itertools
import threading
from multiprocessing import Value

# itertools.count().next() is implemented in C and is atomic under the GIL
counter = itertools.count()

def bump_atomic():
    for _ in range(100_000):
        next(counter)

threads = [threading.Thread(target=bump_atomic) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(next(counter))  # always 400000, no lock needed

# multiprocessing.Value: atomic across separate processes (real parallelism, no GIL)
shared = Value('i', 0)

def bump_shared():
    for _ in range(100_000):
        with shared.get_lock():
            shared.value += 1

threads = [threading.Thread(target=bump_shared) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(shared.value)  # always 400000
