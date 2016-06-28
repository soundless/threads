#!/usr/bin/env python

import threading
MY_LOCK = threading.Lock()

TOTAL = 0

class CountThread(threading.Thread):
    def run(self):
        global TOTAL
        for i in range(1000000):
            MY_LOCK.acquire()
            TOTAL += 1
            MY_LOCK.release()
        print(TOTAL)


if __name__  == '__main__':
    a = CountThread()
    b = CountThread()
    a.start()
    b.start()

