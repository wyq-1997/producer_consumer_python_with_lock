from threading import Thread, Lock
import numpy as np
from time import sleep

def create_thread():
    def my_func(num):
        print("do sth.")
        print(num)
    
    thread = Thread(target=my_func, args= (1,))
    thread.start()
    thread.join()

def race_condition(lock=None):
    x = [0]
    # def increment(x):
    #     x[0] += 1

    def thread_task(x, lock):
        if lock:
            lock.acquire()
        for _ in range(100000):
            x[0] += 1
        if lock:
            lock.release()
    
    def thread_main(x, lock):
        x[0]=0
        threads = [Thread(target=thread_task, args=(x, lock)) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return x[0]
    res = []
    target = 100000*10
    for i in range(500):
        ret = thread_main(x, lock)
        if ret!=target:
            string = f"Run #{i}: {ret}"
            res.append(string)
    print(res)

if __name__ == '__main__':
    print("Create a single thread")
    create_thread()
    # print("Wait for 2 secs")
    # sleep(2)
    print("race_condition")
    race_condition()

    print("solve race condition with lock")
    race_condition(lock=Lock())

    print("Deadlock")
    '''
    A thread: A->B->C->D->E
    read a global var at B and update it at D
    for two theads, we have:
        a: Aa->Ba->Ca->Da->Ea
        b: Ab->Bb->Cb->Db->Eb
    Actually:
        Aa->Ab->Bb->Cb->Ba->Db->Ca->Da->Ea->Eb
        ...
    A lock can be deployed:
    A->(lock)B->C->D(release)->E

    E
    D   * * *
    C   *   *
    B   * * *
    A
      A B C D E

    What is deadlock?

    6
    5(x)
    4(y)
    3(y)
    2(x)
    1
        A B C D E F
          y x x y
    
    for y:
    6
    5(x)
    4(y)  * * * *
    3(y)  * * * *
    2(x)
    1
        A B C D E F
          y x x y
    
    for x:
    6
    5(x)    * *
    4(y)    * *
    3(y)    * *
    2(x)    * *
    1
        A B C D E F
          y x x y

    for both:
    6
    5(x)    * *
    4(y)  * * * *
    3(y)  * * * *
    2(x)    * *
    1
        A B C D E F
          y x x y
    '''