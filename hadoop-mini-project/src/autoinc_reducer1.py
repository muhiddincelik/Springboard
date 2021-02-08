#!/usr/bin/env python
import sys

# [Define group level master information]
group_vin = None
group_make = None
group_year = None
group_accident = 0


# Run for end of every group
def flush(a, b, c, d):
    for i in range(d):
        print ' '.join([a, b, c])


# input comes from STDIN
for line in sys.stdin:
    # [parse the input we got from mapper and update the master info]
    record = line.rstrip('\n').split(' ')
    vin = record[0]
    incident = record[1]
    make = record[2]
    year = record[3]

    # [detect key changes]
    if group_vin != vin:
        if group_vin is not None and group_accident > 0:
            # write result to STDOUT
            flush(group_vin, group_make, group_year, group_accident)
            # group_vin = None
            group_make = None
            group_year = None
            group_accident = 0

    # [update more master info after the key change handling]
    group_vin = vin
    if make != '':
        group_make = make
        group_year = year
    if incident == 'A':
        group_accident += 1


# do not forget to output the last group if needed!
if group_accident > 0:
    flush(group_vin, group_make, group_year, group_accident)
