from termcolor import colored
import logging


def set_logger():
    logging.basicConfig(format='%(asctime)s: ' + '%(levelname)-.1s:' +
                               ':[%(filename)s:%(funcName)s:%(lineno)3d]:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log.txt')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # formatter = logging.Formatter(
    #     '%(asctime)s: ' + '%(levelname)-.1s:' + ':[%(filename)s:%(funcName)s:%(lineno)3d]:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)
    # logger.handlers = []
    # logger.addHandler(console_handler)
    return logger


logger = set_logger()


if __name__ == '__main__':
    logger = set_logger(colored('test', 'magenta'))
    logger.info(' ....')