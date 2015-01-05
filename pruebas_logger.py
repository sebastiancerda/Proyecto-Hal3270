__author__ = 'sbea'

import logging
import time

logging.basicConfig(filename = 'events.log', format = '%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logging.warning('logger iniciado')
time.sleep(0.2)
logging.info('pasdasd')
time.sleep(0.2)
logging.debug('trama nueva')


