# -*- coding:utf-8 -*-
import abc
import inspect
from .langhelpers import ClassStoreDecoratorFactory, reify
from .adttype import adttype, ADTType


class NotComprehensive(Exception):
    pass

dispatchfunction = ClassStoreDecoratorFactory(
    cache_name="_dispatch_method_name_list",
    cache_factory=set,
    cache_convert=lambda x: x.__name__,
    value_convert=staticmethod
)
dispatchmethod = ClassStoreDecoratorFactory(
    cache_name="_dispatch_method_name_list",
    cache_factory=set,
    cache_convert=lambda x: x.__name__,
    value_convert=lambda x: x
)


class MethodControl(object):
    def __init__(self, provider):
        self.provider = provider

    def dispatch(self, cls, target, *args, **kwargs):
        instance = object.__new__(cls)
        instance.__init__(*args, **kwargs)
        tag = target.__class__.__name__
        return getattr(instance, tag)(*target._as_list())

    def generate(self, cls):
        cls.__new__ = self.dispatch
        self.provider.validation_members(cls)
        return self.validation(cls)

    def validation(self, cls):
        provider = self.provider
        for name, type_constructor in provider.members.items():
            template_argspec = inspect.getargspec(type_constructor.__new__)
            fn_argspec = inspect.getargspec(getattr(cls, name))
            if tuple(template_argspec.args[1:]) != tuple(fn_argspec.args[1:]):
                raise NotComprehensive("on {tag}.{name}:  expected={template} != actual={fn}".format(
                    tag=provider.tag,
                    name=name,
                    template=template_argspec.args[1:],
                    fn=fn_argspec.args))
        return cls


class FunctionControl(object):
    def __init__(self, provider):
        self.provider = provider

    def dispatch(self, cls, target):
        tag = target.__class__.__name__
        return getattr(cls, tag)(*target._as_list())

    def generate(self, cls):
        cls.__new__ = self.dispatch
        self.provider.validation_members(cls)
        return self.validation(cls)

    def validation(self, cls):
        provider = self.provider
        for name, type_constructor in provider.members.items():
            template_argspec = inspect.getargspec(type_constructor.__init__)
            fn_argspec = inspect.getargspec(getattr(cls, name))
            if tuple(template_argspec.args[1:]) != tuple(fn_argspec.args):
                raise NotComprehensive("on {tag}.{name}:  expected={template} != actual={fn}".format(
                    tag=provider.tag,
                    name=name,
                    template=template_argspec.args[1:],
                    fn=fn_argspec.args))
        return cls


class ADTTypeProvider(object):
    def __init__(self, tag):
        self.tag = tag
        self.members = {}
        self.function_control = FunctionControl(self)
        self.method_control = MethodControl(self)

    @reify
    def base(self):
        return abc.ABCMeta(self.tag, (ADTType, ), {})

    def __call__(self, name, fields):
        return self.as_member(adttype(name, fields))

    def as_member(self, cls):
        name = cls.__name__
        self.members[name] = cls
        self.base.register(cls)
        return cls

    def is_comprehensive(self, candidates):
       return (all(m in candidates for m in self.members.keys()) and len(candidates) == len(self.members))

    def validation_members(self, cls):
        candidates = list(dispatchmethod.get_candidates(cls))
        if not self.is_comprehensive(candidates):
            raise NotComprehensive("expected={} != actual={}".format(list(self.members.keys()), candidates))

    def match(self, cls):  # side effect!!
        return self.function_control.generate(cls)

    def match_method(self, cls):  # side effect!!
        return self.method_control.generate(cls)
