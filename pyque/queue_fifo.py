#!/usr/bin/env python

from Queue import Queue

q = Queue()

for i in xrange(10, 0, -1):
    q.put(i)

while not q.empty():
    print q.get()
