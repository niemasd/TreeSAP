#!/usr/bin/env python3
from .common import check_end_conditions,Set
from numpy.random import exponential
from random import randint,random
from treeswift import Node,Tree

def birthdeath_tree(L, M, end_num_extant=float('inf'), end_time=float('inf'), max_attempts=100):
    '''Sample a birth-death tree with speciation rate L and death rate M. If both an end number of leaves and an end time are specified, the tree sampling will terminate when the first of the two is reached.

    Args:
        ``L`` (``float``): The speciation rate L

        ``M`` (``float``): The death rate M

        ``end_num_extant`` (``int``): The final number of extant leaves

        ``end_time`` (``float``): The final height of the tree

        ``max_attempts`` (``int``): The maximum number of attempts

    Returns:
        A ``Tree`` object storing the sampled birth-death tree. Leaves with label A* (for Alive) are extant, and leaves with label D* (for Dead) are extinct
    '''
    check_end_conditions(end_num_extant,end_time)
    if not isinstance(L,float) and not isinstance(L,int):
        raise TypeError("L must be a 'float', but it was a %s" % str(type(L)))
    if L < 0:
        raise ValueError("L must be non-negative")
    if not isinstance(M,float) and not isinstance(M,int):
        raise TypeError("M must be a 'float', but it was a %s" % str(type(M)))
    if M < 0:
        raise ValueError("M must be non-negative")
    if L == 0 and M == 0:
        raise ValueError("Either L or M must be non-zero")
    if not isinstance(max_attempts,int):
        raise TypeError("max_attempts must be an 'int', but it was a %s" % str(type(max_attempts)))
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    for _ in range(max_attempts):
        tree = bd(L,M,end_num_extant,end_time)
        if tree is not None:
            return tree
    raise RuntimeError("Failed to sample birth-death tree after %d attempts" % max_attempts)

def bd(L, M, end_num_extant, end_time):
    '''Helper function to attempt to sample a birth-death tree'''
    t = 0.; time = dict(); tree = Tree(); alive = Set(); alive.add(tree.root); dead = list()
    while len(alive) < end_num_extant:
        if len(alive) == 0:
            return None # all lineages died early
        birth_rate = len(alive)*L; death_rate = len(alive)*M
        t += exponential(scale=1./(birth_rate+death_rate))
        if t >= end_time:
            break
        node = alive.random(); time[node] = t; alive.remove(node)
        if random() < birth_rate/(birth_rate+death_rate):
            c1 = Node(); node.add_child(c1); alive.add(c1)
            c2 = Node(); node.add_child(c2); alive.add(c2)
        else:
            dead.append(node)
    if len(alive) == end_num_extant:
        birth_rate = len(alive)*L; death_rate = len(alive)*M
        t += exponential(scale=1./(birth_rate+death_rate))
    if t > end_time:
        t = end_time
    i = 0
    for node in tree.traverse_postorder():
        if node.is_leaf():
            time[node] = t; node.label = '%s%d' % ({True:'A',False:'D'}[node in alive],i); i+= 1
        if node.is_root():
            node.edge_length = time[node]
        else:
            node.edge_length = time[node] - time[node.parent]
    return tree
