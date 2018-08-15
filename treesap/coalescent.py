#!/usr/bin/env python3
from .common import Set
from numpy.random import exponential,geometric
from random import randint
from treeswift import Node,Tree

def coalescent_const_pop_tree(pop_size, num_leaves, continuous=True):
    '''Sample a coalescent tree with a constant population size`. If both an end number of leaves and an end time are specified, the tree sampling will terminate when the first of the two is reached.

    Args:
        ``pop_size`` (``float``): The population size

        ``num_leaves`` (``int``): The final number of leaves

        ``continuous`` (``bool``): ``True`` to simulate a continuous-time coalescent tree, or ``False`` to simulate a discrete-time coalescent tree

    Returns:
        A ``Tree`` object storing the sampled coalescent tree
    '''
    if not isinstance(pop_size,float) and not isinstance(pop_size,int):
        raise TypeError("pop_size must be a 'float', but it was a %s" % str(type(pop_size)))
    if pop_size <= 0:
        raise ValueError("pop_size must be positive")
    if not isinstance(num_leaves,int):
        raise TypeError("num_leaves must be an 'int', but it was a %s" % str(type(num_leaves)))
    if num_leaves < 2:
        raise ValueError("num_leaves must be at least 2")
    leaves = Set(); time = dict(); t = 0
    for i in range(num_leaves):
        node = Node(label=i); time[node] = 0; leaves.add(node)
    while len(leaves) != 1:
        if continuous:
            t += exponential((2*pop_size)/(len(leaves)*(len(leaves)-1)))
        else:
            t += geometric((len(leaves)*(len(leaves)-1))/(2*pop_size))
        p = Node(); time[p] = t
        n1 = leaves.random(); leaves.remove(n1)
        n2 = leaves.random(); leaves.remove(n2)
        p.add_child(n1); p.add_child(n2); leaves.add(p)
    tree = Tree(); tree.root = leaves.random()
    for node in tree.traverse_preorder():
        if not node.is_root():
            node.edge_length = time[node.parent] - time[node]
    return tree


