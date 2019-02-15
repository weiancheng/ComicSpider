from logger.singleton import Singleton
import logging
import inspect


class LOGGER(metaclass=Singleton):
    def __init__(self, name='LOGGER'):
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
        self.logger = logging.getLogger(name)

    def set_level(self, level):
        self.logger.setLevel(level)

    def d(self, msg):
        self.logger.debug('D ' + inspect.stack()[1][3] + ' : ' + msg)

    def i(self, msg):
        self.logger.info('I ' + inspect.stack()[1][3] + ' : ' + msg)

    def w(self, msg):
        self.logger.warning('W ' + inspect.stack()[1][3] + ' : ' + msg)

    def e(self, msg):
        self.logger.error('E ' + inspect.stack()[1][3] + ' : ' + msg)

    def f(self, msg):
        self.logger.critical('F ' + inspect.stack()[1][3] + ' : ' + msg)
