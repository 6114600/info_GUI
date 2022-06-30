import logging
import datetime

level_dict = {'info': logging.INFO,'debug':logging.DEBUG}

def set_logger(type,log_path):
    logger = logging.getLogger('test_logger')
    logger.setLevel(level_dict[type])
    fh = logging.FileHandler(log_path,'a',encoding='utf-8')
    fh.setLevel(level_dict[type])
    fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)
    return logger


if __name__ == '__main__':
    logger = set_logger('debug','test.log')
    logger.info('test')

