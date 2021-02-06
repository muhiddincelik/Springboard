#!/usr/bin/env python
import sys
import logging.config
import logging
import yaml

with open("docs\\check.logging.yml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

vins = []
updated = []
# input comes from STDIN
for line in sys.stdin:
    # [parse the input we got from mapper and update the master info]
    lst = line.split(' ')
    if lst[1] == 'I':
        vins.append(lst)
    else:
        for vin in vins:
            if lst[0] == vin[0]:
                lst = lst[:-2]
                lst.extend(vin[2:])
                updated.append(lst)

vins.extend(updated)
vins = [' '.join(vin) for vin in vins if vin[1] == 'A']
for vin in vins:
    print(vin, end='')

logger.info('First Reducing has been completed successfully.')
