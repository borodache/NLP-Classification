import logging

# logname = 'logger.text'
# logging.basicConfig(filename=logname,
logging.basicConfig(filename='logger.txt',
                    filemode='a',
                    level=logging.INFO)

logging.info("Running Logger")

logger = logging.getLogger('logger.txt')

