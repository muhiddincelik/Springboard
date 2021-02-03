import sys

# input comes from STDIN (standard input)

for line in sys.stdin:
    lst = line.split(',')
    key = lst[2]
    # value = lst[1], lst[3], lst[5]
    print(key, lst[1], lst[3], lst[5])