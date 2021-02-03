#!/usr/bin/env python
import sys

for line in sys.stdin:
    lst = line.split(' ')
    key = str(lst[2]) + '-' + lst[3]
    count = 1
    print(key, count)

