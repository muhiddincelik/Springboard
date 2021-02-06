import sys
import logging.config
import logging
import yaml

with open("docs\\check.logging.yml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

# input comes from STDIN (standard input)

for line in sys.stdin:
    lst = line.split(',')
    key = lst[2]
    print(key, lst[1], lst[3], lst[5])

logger.info('First Mapping has been completed successfully.')
