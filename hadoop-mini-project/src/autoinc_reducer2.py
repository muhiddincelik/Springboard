#!/usr/bin/env python
import sys
import logging.config
import logging
import yaml

with open("docs\\check.logging.yml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

freq = {}
for item in sys.stdin:
    if item.split(' ')[0] in freq:
        freq[item.split(' ')[0]] += 1
    else:
        freq[item.split(' ')[0]] = 1

for key, value in freq.items():
    print(key, value)

logger.info('Second Reducing has been completed successfully.')

