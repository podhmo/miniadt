# -*- coding:utf-8 -*-
import sys

class ClassStoreDecoratorFactory(object):
    def __init__(self, cache_name, cache_factory, cache_convert, value_convert):
        self.cache_name = cache_name
        self.cache_factory = cache_factory
        self.cache_convert =  cache_convert
        self.value_convert = value_convert

    def on_classmethod(self, fn):
        f = sys._getframe()
        class_env = f.f_back.f_locals
        if not self.cache_name in class_env:
            class_env[self.cache_name] = self.cache_factory()
        class_env[self.cache_name].add(self.cache_convert(fn))
        return self.value_convert(fn)
    __call__ = on_classmethod

    def with_class_attributes(self, fn, class_env, name=None):
        if not self.cache_name in class_env:
            class_env[self.cache_name] = self.cache_factory()
        if name is None:
            class_env[self.cache_name].add(self.cache_convert(fn))
        else:
            class_env[self.cache_name].add(name)
        return self.value_convert(fn)


    def get_candidates(self, module_class):
        if hasattr(module_class, self.cache_name):
            for name in getattr(module_class, self.cache_name):
                yield name

