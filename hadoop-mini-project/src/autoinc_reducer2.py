#!/usr/bin/env python
import sys


freq = {}
for item in sys.stdin:
    if item.split(' ')[0] in freq:
        freq[item.split(' ')[0]] += 1
    else:
        freq[item.split(' ')[0]] = 1

for key, value in freq.items():
    print(key, value)

