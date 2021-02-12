import logging
from logging.handlers import RotatingFileHandler

'''
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
'''

import os
import sys
import colorlog
import configparser
config = configparser.ConfigParser()
#dir_name = os.path.basename(os.getcwd()).lower()
#config.read(f'{dir_name}.conf')
config.read('my_config.conf')

log_level = config['logger']['log_level']
log_path = config['logger']['log_path']
log_file_name = config['logger']['log_file_name']

if not os.path.exists('log/'):
    os.makedirs('log/')
    
def setup_logging():

    log_level = config['logger']['log_level'].upper()
    if log_level == "DEBUG":
        log_level = logging.DEBUG
    elif log_level == "INFO":
        log_level = logging.INFO
    elif log_level == "WARNING":
        log_level = logging.WARNING
    elif log_level == "ERROR":
        log_level = logging.ERROR
    elif log_level == "CRITICAL":
        log_level = logging.CRITICAL
    else:
        log_level = logging.NOTSET

    format = '[%(asctime)s] [%(name)-8s] %(levelname)-8s: %(message)s'
    filename=f'{log_path}/{log_file_name}.log'
    date_format = '%Y-%m-%d %H:%M:%S'
    log_colors = { 'DEBUG': 'blue', 'INFO' : 'green', 'WARNING': 'bold_yellow', 'ERROR': 'bold_red', 'CRITICAL': 'purple'}

    # set up logging to file - see previous section for more details
    #logging.basicConfig(format=format, filename=filename, filemode='a')
    #fh = logging.FileHandler(encoding='utf-8', mode='a', filename=filename)
    fh = logging.handlers.TimedRotatingFileHandler(filename=filename, when='d', interval=1, encoding='utf-8', utc=True)
    logging.basicConfig(handlers=[fh], format=format, datefmt=date_format, level=log_level)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    if 'colorlog' in sys.modules and os.isatty(2):
        cformat = '%(log_color)s' + format
        f = colorlog.ColoredFormatter(cformat, date_format, log_colors = log_colors)
    else:
        f = logging.Formatter(format, date_format)
    ch = logging.StreamHandler()
    ch.setFormatter(f)
    root_logger.addHandler(ch)


setup_logging()


def get_logger(logger_name):
        
    log = logging.getLogger(logger_name)
    return log

log = get_logger(__name__)
'''
log.debug   ('Hello Debug')
log.info    ('Hello Info')
log.warning ('Hello Warn')
log.error   ('Hello Error')
log.critical('Hello Critical')
'''