from threading import Thread, Lock
from random import randint


size = 3
queue = [None]*size
start = 0
end = 0
indices = [start, end]
lock = Lock()

def generator():
    for i in range(100):
        yield i
gene = generator()
def producer(queue, indices):
    done = False
    while not done:
        lock.acquire()
        start, end = indices
        if (end+1)%size != start:
            product = gene.__next__()
            queue[end] = product
            print(f"product produced: {product} from {queue}")
            end = (end+1)%size
            indices[1] = end
            done = True
        lock.release()

def consumer(queue, indices):
    done = False
    while not done:
        lock.acquire()
        start, end = indices
        if start!=end:
            product = queue[start]
            queue[start] = None
            print(f"product consumed: {product} from {queue}")
            start = (start+1)%size
            indices[0] = start
            done = True
        lock.release()

threads = []
for i in range(20):
    threads.append(Thread(target=producer, args=(queue, indices)))

for i in range(2):
    threads.append(Thread(target=producer, args=(queue, indices)))


for i in range(20):
    threads.append(Thread(target=consumer, args=(queue, indices)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

