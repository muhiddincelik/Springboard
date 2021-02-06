#!/usr/bin/env python
import sys
import logging.config
import logging
import yaml

with open("docs\\check.logging.yml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


for line in sys.stdin:
    lst = line.split(' ')
    key = str(lst[2]) + '-' + str(lst[3].rstrip('\n'))
    count = 1
    print(key, count)

logger.info('Second Mapping has been completed successfully.')

