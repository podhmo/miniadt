# -*- coding:utf-8 -*-
"""
## define mini adt
Result = ADTTypeProvider("Result")
Failure = Result("Failure", "code message")
Success = Result("Success", "value")

@Result.match
class match0(object):
    @Result.dispatchmethod
    def Failure(code, message):
        return ["oops", code, message]

    @Result.dispatchmethod
    def Success(value):
        return ["ok", value]
"""

from collections import namedtuple
from .langhelpers import ClassStoreDecoratorFactory
import inspect

class NotComprehensive(Exception):
    pass

dispatchmethod = ClassStoreDecoratorFactory(
    cache_name="_dispatch_method_name_list", 
    cache_factory=set,
    cache_convert=lambda x : x.__name__,
    value_convert=staticmethod
)

def match_dispatch(cls, target):
    tag = target.__class__.__name__
    return getattr(cls, tag)(*target)

class ADTTypeProvider(object):
    def __init__(self, tag, dispatch_function=match_dispatch):
        self.tag = tag
        self.members = {}
        self.dispatch_function = staticmethod(dispatch_function)

    def as_member(self, cls):
        name = cls.__name__
        self.members[name] = cls
        return cls

    def is_comprehensive(self, candidates):
       return (all(m in candidates for m in self.members.keys())
               and len(candidates) == len(self.members))

    def validation(self, cls):
        candidates = list(dispatchmethod.get_candidates(cls))
        if not self.is_comprehensive(candidates):
            raise NotComprehensive("{} != {}".format(candidates, list(self.members.keys())))

        for name, type_constructor in self.members.items():
            template_argspec = inspect.getargspec(type_constructor.__new__)
            fn_argspec = inspect.getargspec(getattr(cls, name))
            if tuple(template_argspec.args[1:]) != tuple(fn_argspec.args):
                raise NotComprehensive("on {tag}.{name}:  {template} != {fn}".format(
                    tag=self.tag, 
                    name=name, 
                    template=template_argspec.args[1:],
                    fn=fn_argspec.args))
        return cls

    def match(self, cls):  ##side effect!!
        cls.__new__ = self.dispatch_function
        return self.validation(cls)

    def __call__(self, name, fields):
        return self.as_member(namedtuple(name, fields))

    dispatchmethod = staticmethod(dispatchmethod)

