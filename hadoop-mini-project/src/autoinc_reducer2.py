#!/usr/bin/env python
import sys
# import logging.config
# import logging
# import yaml
#
# with open("docs\\check.logging.yml", "r") as f:
#     config = yaml.safe_load(f)
#     logging.config.dictConfig(config)
#
# logger = logging.getLogger(__name__)

freq = {}
for line in sys.stdin:
    item_list = line.rstrip('\n').split(',')
    if item_list[0] in freq:
        freq[item_list[0]] += 1
    else:
        freq[item_list[0]] = 1

for key, value in freq.items():
    print(key, value)

# logger.info('Second Reducing has been completed successfully.')

