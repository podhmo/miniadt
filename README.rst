miniadt
========================================

how to use

.. code:: 

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
    ...     @dispatch
    ...     def Node(e, children):
    ...         return max(depth(e)for e in children) + 1
    ...
    ...     @dispatch
    ...     def Leaf(e):
    ...         return 1

    >>> depth(Leaf(e=10))
    1

    >>> depth(Node(e=10, children=[Leaf(e=20), Node(e=30, children=[Leaf(e=40)])]))
    3

miniadt has comprehensive check function.

.. code:: 

    ## not comprehensive definition on pattern matching function error is occur 

    ### 1. lack of dispatch candidates
    >>> class invalid_dispatch(object):
    ...     @dispatch
    ...     def Node(e, children):
    ...         return "foo"

    >>> TreeType.match(invalid_dispatch)
    Traceback (most recent call last):
     ...
    miniadt.NotComprehensive: expected=['Node', 'Leaf'] != actual=['Node']


    ### 2. dispatch function's arguments are invalid.
    >>> class invalid_dispatch2(object):
    ...     @dispatch
    ...     def Node(e):  ## correct argsspec is "e, children"
    ...         return "foo"
    ...     @dispatch
    ...     def Leaf(e):
    ...         return "foo"

    >>> TreeType.match(invalid_dispatch2)
    Traceback (most recent call last):
     ...
    miniadt.NotComprehensive: on Tree.Node:  expected=['e', 'children'] != actual=['e']

