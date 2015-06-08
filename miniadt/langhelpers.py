# -*- coding:utf-8 -*-
from prestring.python import PythonModule
import logging
logger = logging.getLogger(__name__)


class reify(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


def as_python_code(fn):
    def wrapper(name, *args, **kwargs):
        m = PythonModule()
        env = {}
        fn(m, name, *args, **kwargs)
        code = str(m)
        logger.debug("-- as_python_code --\n%s", code)
        # activate python code
        exec(code, globals(), env)
        return env[name]
    return wrapper
