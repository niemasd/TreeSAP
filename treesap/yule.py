#!/usr/bin/env python3
from .common import check_end_conditions
from numpy.random import exponential
from random import randint
from treeswift import Node,Tree

def yule_tree(L, end_num_leaves=float('inf'), end_time=float('inf')):
    '''Sample a Yule tree with speciation rate L. If both an end number of leaves and an end time are specified, the tree sampling will terminate when the first of the two is reached.

    Args:
        ``L`` (``float``): The speciation rate L

        ``end_num_leaves`` (``int``): The final number of leaves

        ``end_time`` (``float``): The final height of the tree

    Returns:
        A ``Tree`` object storing the sampled Yule tree
    '''
    check_end_conditions(end_num_leaves,end_time)
    if not isinstance(L,float) and not isinstance(L,int):
        raise TypeError("L must be a 'float', but it was a %s" % str(type(L)))
    if L <= 0:
        raise ValueError("L must be positive")
    B = 1./L; t = 0.; time = dict(); tree = Tree(); leaves = [tree.root]
    while len(leaves) < end_num_leaves:
        t += exponential(scale=B/len(leaves))
        if t >= end_time:
            break
        i = randint(0,len(leaves)-1); node = leaves[i]; time[node] = t
        c1 = Node(); node.add_child(c1); leaves[i] = c1
        c2 = Node(); node.add_child(c2); leaves.append(c2)
    if len(leaves) == end_num_leaves:
        t += exponential(scale=B/len(leaves))
    if t > end_time:
        t = end_time
    i = 0
    for node in tree.traverse_postorder():
        if node.is_leaf():
            time[node] = t; node.label = i; i+= 1
        if node.is_root():
            node.edge_length = time[node]
        else:
            node.edge_length = time[node] - time[node.parent]
    return tree
