#!/usr/bin/env python

from Queue import Queue
from threading import Thread

import time
import feedparser

threads = 6
queue = Queue()

feed_urls = ['https://news.ycombinator.com/rss']

def download(i, q):
    """
    This is the worker thread function. It processes items in the queue one
    after another. These daemon threads go into an infinite loop, and only exit
    when the main thread ends.
    """
    while True:
        #print "%s worker: " % ( i + 1 )
        url = q.get()
        print '%s: Downloading: ' % ( i + 1 ), url
        time.sleep(i + 1)
        q.task_done()


if __name__ == '__main__':
    # setup some threads to fetch the links
    for i in range(threads):
        worker = Thread(target=download, args=(i, queue))
        worker.setDaemon(True)
        worker.start()

    # Download the feed(s) and put the enclosure URLs into the queue.
    for url in feed_urls:
        d = feedparser.parse(url)
        for item in d['entries']:
            print "Queuing:", item['link']
            queue.put(item['link'])

    print "*** Main thread waiting ***"

    queue.join()

    print "*** Done ***"

