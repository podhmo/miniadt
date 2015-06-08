# -*- coding:utf-8 -*-
import abc
import inspect
from .langhelpers import reify
from .adttype import adttype, ADTType


class NotComprehensive(Exception):
    pass


class ADTTypeProvider(object):
    def __init__(self, tag):
        self.tag = tag
        self.members = {}

    @reify
    def base(self):
        return abc.ABCMeta(self.tag, (ADTType, ), {})

    def __call__(self, name, fields):
        return self.register(adttype(name, fields))

    def register(self, cls):
        name = cls.__name__
        self.members[name] = cls
        self.base.register(cls)
        return cls

    def is_comprehensive(self, candidates):
       return (all(m in candidates for m in self.members.keys()) and len(candidates) == len(self.members))

    def _validation_members(self, cls):
        for m in self.members.keys():
            if not hasattr(cls, m):
                raise NotComprehensive("{} is not found. expected={}".format(m, list(self.members.keys())))

    def match(self, cls):  # side effect!!
        self._validation_members(cls)

        for name, type_constructor in self.members.items():
            template_argspec = inspect.getargspec(type_constructor.__init__)
            fn_argspec = inspect.getargspec(getattr(cls, name))
            if tuple(template_argspec.args[1:]) != tuple(fn_argspec.args):
                raise NotComprehensive("on {tag}.{name}:  expected={template} != actual={fn}".format(
                    tag=self.tag,
                    name=name,
                    template=template_argspec.args[1:],
                    fn=fn_argspec.args))

        def dispatch(cls, target):
            tag = target.__class__.__name__
            return getattr(cls, tag)(*target._as_list())

        cls.__new__ = staticmethod(dispatch)
        return cls

    def match_instance(self, cls):  # side effect!!
        self._validation_members(cls)

        for name, type_constructor in self.members.items():
            template_argspec = inspect.getargspec(type_constructor.__init__)
            fn_argspec = inspect.getargspec(getattr(cls, name))
            if tuple(template_argspec.args[1:]) != tuple(fn_argspec.args[1:]):
                raise NotComprehensive("on {tag}.{name}:  expected={template} != actual={fn}".format(
                    tag=self.tag,
                    name=name,
                    template=template_argspec.args[1:],
                    fn=fn_argspec.args[1:]))

        def dispatch(self, target):
            tag = target.__class__.__name__
            return getattr(self, tag)(*target._as_list())

        cls.__call__ = dispatch
        return cls

    def classify(self, cls):  # side effect!!
        self._validation_members(cls)

        def dispatch(self, ob, *args, **kwargs):
            tag = ob.__class__.__name__
            return getattr(self, tag)(ob, *args, **kwargs)
        cls.__call__ = dispatch
        return cls
