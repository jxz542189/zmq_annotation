# coding:utf-8
import logging.handlers
import config


class Logger:
    log_DEBUG = logging.getLogger('D')

    log_DEBUG.setLevel(logging.DEBUG)
    handler_D = logging.handlers.TimedRotatingFileHandler(config.info_file,
                                                          when='H',
                                                          interval=3,
                                                          backupCount=30,
                                                          delay=False, utc=False)
    handler_D.suffix = "%Y%m%d_%H%M.log"
    formatter = logging.Formatter(
        '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    handler_D.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    log_DEBUG.addHandler(handler_D)
    log_DEBUG.addHandler(ch)

    log_ERROR = logging.getLogger('E')
    log_ERROR.setLevel(logging.ERROR)
    handler_E = logging.handlers.TimedRotatingFileHandler(config.err_file,
                                                          when='H',
                                                          interval=3,
                                                          backupCount=30,
                                                          delay=False,
                                                          utc=False)
    handler_E.suffix = "%Y%m%d_%H%M.log"
    formatter = logging.Formatter(
        '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    handler_E.setFormatter(formatter)

    log_ERROR.addHandler(handler_E)
    log_ERROR.addHandler(ch)


if __name__ == '__main__':
    Logger.log_DEBUG.debug('foorbar兔子')
    Logger.log_ERROR.error('foorbar兔子log_ERROR')