#!/usr/bin/env python

from Queue import PriorityQueue

class Job(object):
    def __init__(self, priority=10, description="Default Job"):
        self.priority = priority
        self.description = description
        print "New: ", description, "(" + str(priority) + ")"

    def __cmp__(self, other):
        if self and other:
            return cmp(self.priority, other.priority)


if __name__ == '__main__':
    q = PriorityQueue()
    q.put(Job(3, "Mid-level job"))
    q.put(Job())
    q.put(Job(1, "Verify import job"))
    q.put(Job(0, "Super import job"))

    while not q.empty():
        j = q.get()
        print "Processing: {} \t ({})".format(j.description, j.priority)
