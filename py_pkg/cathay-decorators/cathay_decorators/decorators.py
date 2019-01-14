import time
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class BaseDecorator(object):
    '''
        Base class to extend your custom decorators,
        define pre_func and pos_func actions
    '''

    def pre_func(self):
        raise NotImplementedError

    def pos_func(self):
        raise NotImplementedError

    def __call__(self, func):
        def wrapper(*args, **kargs):
            self.pre_func()
            result = func(*args, **kargs)
            self.pos_func()
            return result
        return wrapper


class TimeBlockDecorator(BaseDecorator):
    '''
        Use for timing certain function.
        Example:
            @TimeBlockDecorator(title='yout_text')
            def func():
                ...
    '''

    def __init__(self, title):
        super(TimeBlockDecorator, self).__init__()
        self.title = title

    def pre_func(self):
        self.start_time = time.time()
        logger.info("=== {} ===".format(self.title))

    def pos_func(self):
        logger.info("== exec time: {} ==".format(timedelta(seconds=time.time() - self.start_time)))


class LogDecorator(BaseDecorator):
    '''
        Use for log certain function start
        Example:
            @LogDecorator(title='yout_text')
            def func():
                ...
    '''

    def __init__(self, title):
        super(LogDecorator, self).__init__()
        self.title = title

    def pre_func(self):
        logger.info("{} ...".format(self.title))

    def pos_func(self):
        pass


class BlockDecorator(BaseDecorator):
    '''
        Use for block certain function
        Example:
            @BlockDecorator(title='yout_text')
            def func():
                ...
    '''

    def __init__(self, title):
        super(BlockDecorator, self).__init__()
        self.title = title

    def pre_func(self):
        logger.info("=== {} ===".format(self.title))

    def pos_func(self):
        logger.info("=" * 10)
