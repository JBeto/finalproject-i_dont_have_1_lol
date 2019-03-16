#!/usr/bin/env python3
saved = set()
with open('tweets_url.data') as f:
    count = 0
    for line in f:
        if line in saved:
            print(line)
            count += 1
        saved.add(line)
    print(count)
