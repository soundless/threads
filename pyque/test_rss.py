#!/usr/bin/env python

import feedparser
from pprint import pprint

d = feedparser.parse('./rss1.xml')
for item in d['entries']:
    print item['link']
