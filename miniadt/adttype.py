# -*- coding:utf-8 -*-
from .langhelpers import as_python_code


class ADTType(object):
    pass


@as_python_code
def adttype(m, name, template):
    """
    syntax sugar, define a class, like this.
    * attrs :: attrname
    """

    names = [x.strip() for x in template.replace(",", "").split(" ") if x != ""]
    m.from_("functools", "total_ordering")
    m.from_("miniadt.adttype", "ADTType")

    m.stmt("@total_ordering")
    with m.class_(name, "ADTType"):
        if names:
            with m.method("__init__", ", ".join(names)):
                for name in names:
                    fmt = "self.{name} = {name}"
                    m.stmt(fmt.format(name=name))

            m.stmt("__slots__ = ({})", ", ".join(repr(name) for name in names))

        with m.method("__hash__"):
            cands = ["__class__"] + names
            m.return_("hash('@'.join(map(repr, ({}))))".format(", ".join("self.{}".format(name) for name in cands)))

        with m.method("__gt__", "other"):
            for name in names:
                with m.if_("self.{name} > other.{name}".format(name=name)):
                    m.return_("True")
            m.return_("False")

        with m.method("__eq__", "other"):
            with m.if_("not isinstance(other, self.__class__)"):
                    m.return_("False")
            for name in names:
                with m.if_("self.{name} != other.{name}".format(name=name)):
                    m.return_("False")
            m.return_("True")

        with m.method("__repr__"):
            m.stmt("name = self.__class__.__name__")
            args = ", ".join("{name}={{self.{name}!r}}".format(name=name) for name in names)
            m.return_("'{{}}({})'.format(name, self=self)".format(args))

        with m.method("_as_list"):
            m.return_("[getattr(self, x) for x in {!r}]".format(names))
    return name
