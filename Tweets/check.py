#!/usr/bin/env python3
saved = set()
with open('tweets_url.data', 'r') as f:
    count = 0
    for line in f:
        if line in saved:
            count += 1
        else:
            saved.add(line)
    print('Duplicates found: {}'.format(count))

with open('tweets_url_no_dup.data', 'w') as f:
    for json in saved:
        f.write(json)

