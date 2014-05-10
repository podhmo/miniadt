"""
this is demo

## create Type

>>> from miniadt import ADTTypeProvider, dispatchmethod
>>> TreeType = ADTTypeProvider("Tree")

>>> Node = TreeType("Node", "e children")
>>> Leaf = TreeType("Leaf", "e")


## printing value

>>> Leaf(e=10)
Leaf(e=10)
>>> Node(e=10, children=[Leaf(e=20)])
Node(e=10, children=[Leaf(e=20)])


## use pattern match

>>> @TreeType.match
... class depth(object):
...     @dispatchmethod
...     def Node(e, children):
...         return max(depth(e)for e in children) + 1
...
...     @dispatchmethod
...     def Leaf(e):
...         return 1

>>> depth(Leaf(e=10))
1

>>> depth(Node(e=10, children=[Leaf(e=20), Node(e=30, children=[Leaf(e=40)])]))
3


## not comprehensive definition on pattern matching function error is occur 

### 1. lack of dispatch candidates
>>> class invalid_dispatch(object):
...     @dispatchmethod
...     def Node(e, children):
...         return "foo"

>>> TreeType.match(invalid_dispatch)
Traceback (most recent call last):
 ...
miniadt.NotComprehensive: expected=['Leaf', 'Node'] != actual=['Node']


### 2. dispatch function's arguments are invalid.
>>> class invalid_dispatch2(object):
...     @dispatchmethod
...     def Node(e):  ## correct argsspec is "e, children"
...         return "foo"
...     @dispatchmethod
...     def Leaf(e):
...         return "foo"

>>> TreeType.match(invalid_dispatch2)
Traceback (most recent call last):
 ...
miniadt.NotComprehensive: on Tree.Node:  expected=['e', 'children'] != actual=['e']
"""


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
