#encoding:utf-8

import os
import logging
import logging.config

script_path = os.path.dirname(os.path.abspath(__file__))

try:
    import settings
    config_file = settings.LOG_CONFIG_FILE
    logging.config.fileConfig(os.path.join(script_path,config_file))
except:
    logging.config.fileConfig(os.path.join(script_path,"logging.ini"))

#create logger
def getLogger(func_name):
    return logging.getLogger(func_name)

def test():
    log = getLogger('test')
    log.debug('this is a debug msg')
    log.info('this is a debug msg')
    log.warning('this is a debug msg')
    log.error('this is a debug msg')

def another_test():
    log = getLogger('another_test')
    log.debug('this is a debug msg')
    log.info('this is a debug msg')
    log.warning('this is a debug msg')
    log.error('this is a debug msg')

if __name__ == '__main__':
    test()
    another_test()