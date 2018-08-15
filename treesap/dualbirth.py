#!/usr/bin/env python3
from .common import check_end_conditions
from numpy.random import exponential
from random import randint,random
from treeswift import Node,Tree

def dualbirth_tree(La, Lb, end_num_leaves=float('inf'), end_time=float('inf')):
    '''Sample a Dual-Birth tree with activation rate La and birth rate Lb. If both an end number of leaves and an end time are specified, the tree sampling will terminate when the first of the two is reached.

    Args:
        ``La`` (``float``): The activation rate La

        ``Lb`` (``float``): The birth rate Lb

        ``end_num_leaves`` (``int``): The final number of leaves

        ``end_time`` (``float``): The final height of the tree

    Returns:
        A ``Tree`` object storing the sampled Dual-Birth tree
    '''
    check_end_conditions(end_num_leaves,end_time)
    if not isinstance(La,float) and not isinstance(La,int):
        raise TypeError("La must be a 'float', but it was a %s" % str(type(La)))
    if La <= 0:
        raise ValueError("La must be positive")
    if not isinstance(Lb,float) and not isinstance(Lb,int):
        raise TypeError("Lb must be a 'float', but it was a %s" % str(type(Lb)))
    if Lb <= 0:
        raise ValueError("Lb must be positive")
    t = 0.; time = dict(); tree = Tree(); active = [tree.root]; inactive = list()
    while len(active) + len(inactive) < end_num_leaves:
        t += exponential(scale=1./(len(active)*Lb+len(inactive)*La))
        if t >= end_time:
            break
        if random() < (len(active)*Lb)/(len(active)*Lb+len(inactive)*La):
            picked_set = active; other_set = inactive
        else:
            picked_set = inactive; other_set = active
        i = randint(0,len(picked_set)-1); node = picked_set[i]; time[node] = t
        c1 = Node(); node.add_child(c1); picked_set[i] = c1
        c2 = Node(); node.add_child(c2); other_set.append(c2)
    if len(active) + len(inactive) == end_num_leaves:
        t += exponential(scale=1./(len(active)*Lb+len(inactive)*La))
    if t > end_time:
        t = end_time
    for i,node in enumerate(tree.traverse_leaves()):
        time[node] = t; node.label = i
    for node in tree.traverse_preorder():
        if node.is_root():
            node.edge_length = time[node]
        else:
            node.edge_length = time[node] - time[node.parent]
    return tree
