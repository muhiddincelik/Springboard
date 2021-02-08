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

# input comes from STDIN (standard input)


for line in sys.stdin:
    line = line.strip()
    line = line.rstrip('\n')
    cells = line.split(',')
    key = cells[2]
    value = ' '.join([cells[1], cells[3], cells[5]])
    print '%s %s' % (key, value)

# logger.info('First Mapping has been completed successfully.')
