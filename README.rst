miniadt
========================================

how to use

.. code:: 

    ## create Type

    >>> from miniadt import ADTTypeProvider
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
    ...     def Node(e, children):
    ...         return max(depth(e)for e in children) + 1
    ...
    ...     def Leaf(e):
    ...         return 1

    >>> depth(Leaf(e=10))
    1

    >>> depth(Node(e=10, children=[Leaf(e=20), Node(e=30, children=[Leaf(e=40)])]))
    3

miniadt has comprehensive check function.

.. code::

  ## not comprehensive definition on pattern matching function error is occur 

  ### 1. lack of dispatch andidates
  >>> class invalid_dispatch(object):
  ...     def Node(e, children):
  ...         return "foo"

  >>> TreeType.match(invalid_dispatch)
  Traceback (most recent call last):
   ...
  miniadt.NotComprehensive: Leaf is not found. expected=['Node', 'Leaf']


  ### 2. dispatch function's arguments are invalid.
  >>> class invalid_dispatch2(object):
  ...     def Node(e):  ## correct argsspec is "e, children"
  ...         return "foo"
  ...     def Leaf(e):
  ...         return "foo"

  >>> TreeType.match(invalid_dispatch2)
  Traceback (most recent call last):
   ...
  miniadt.NotComprehensive: on Tree.Node:  expected=['e', 'children'] != actual=['e']


similar functions
----------------------------------------

- match
- match_instance
- classify

.. code-block:: python

  from miniadt import ADTTypeProvider
  Tree = ADTTypeProvider("Tree")
  Node = Tree("Node", "e children")
  Leaf = Tree("Leaf", "e")

  print(Leaf(e=10))  # => Leaf(e=10)
  print(Node(e=10, children=[Leaf(e=20)]))  # => Node(e=10, children=[Leaf(e=20)])


  @Tree.match
  class depth(object):
      def Leaf(e):
          return 1

      def Node(e, children):
          return max(depth(e) for e in children) + 1


  print(depth(Leaf(e=10)))  # => 10
  print(depth(Node(e=10, children=[Leaf(e=20)])))  # 2


  @Tree.match_instance
  class Applicator(object):
      def __init__(self, name):
          self.name = name

      def Leaf(self, e):
          return self.name

      def Node(self, e, children):
          return [self.name, [self(x) for x in children]]

  print(Applicator("foo")(Leaf(e=10)))  # => foo
  print(Applicator("foo")(Node(e=10, children=[Leaf(e=20)])))  # => ['foo', ['foo']]


  @Tree.classify
  class ToDict(object):
      def Leaf(self, leaf):
          return leaf.e

      def Node(self, node):
          return {"e": node.e, "children": [self(e) for e in node.children]}

  todict = ToDict()
  print(todict(Leaf(e=10)))  # => 10
  print(todict(Node(e=10, children=[Leaf(e=20)])))  # => {'e': 10, 'children': [20]}

