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


for line in sys.stdin:
    cells = line.rstrip('\n').split(' ')
    key = str(cells[1]) + '-' + str(cells[2])
    count = str(1)
    print(','.join([key, count]))

# logger.info('Second Mapping has been completed successfully.')

