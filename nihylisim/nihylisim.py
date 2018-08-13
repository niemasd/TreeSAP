#!/usr/bin/env python3
from math import exp
from scipy.stats import rv_continuous
from scipy.integrate import quad as integral
from treeswift import Node,Tree
try:
    from Queue import PriorityQueue  # ver. < 3.0
except ImportError:
    from queue import PriorityQueue

# PDF of first interarrival time of non-homogeneous Poisson process with rate function L(t)
class NHPP_first_interarrival_time(rv_continuous):
    def set_L(self, L):
        self.L = L
    def _pdf(self, x):
        if not hasattr(self,'L'):
            raise RuntimeError("Must run set_L function to set rate function L(t) first")
        return self.L(x) * exp(-integral(self.L,0,x)[0])

# sample a non-homogeneous Yule tree with rate function L(t)
def nonhomogeneous_yule_tree(L, end_num_leaves=None, end_time=None):
    '''Sample a non-homogeneous Yule tree with rate function λ(t). If both an end number of leaves and an end time are specified, the tree sampling will terminate when the first of the two is reached.

    Args:
        ``L`` (``func``): The rate function λ(t)

        ``end_num_leaves`` (``int``): The final number of leaves

        ``end_time`` (``float``): The final height of the tree

    Returns:
        A ``Tree`` object storing the sampled non-homogeneous Yule tree
    '''
    if not callable(L):
        raise TypeError("L must be a 'func', but it was a %s" % str(type(L)))
    if end_num_leaves is None and end_time is None:
        raise ValueError("Must specify either end_num_leaves or end_time (or both)")
    if end_num_leaves is not None:
        if not isinstance(end_num_leaves,int):
            raise TypeError("end_num_leaves must be an integer")
        elif end_num_leaves < 1:
            raise ValueError("end_num_leaves must be at least 1")
    if end_time is not None:
        try:
            end_time = float(end_time)
        except:
            raise TypeError("end_time must be a float")
        if end_time <= 0:
            raise ValueError("end_time must be positive")
    tree = Tree(); num_leaves = 1; curr_time = 0
    rv = NHPP_first_interarrival_time(a=0); rv.set_L(L); tree.root.time = rv.rvs(size=1)[0]
    pq = PriorityQueue(); pq.put((tree.root.time,tree.root))
    while True:
        curr_time,node = pq.get()
        if num_leaves == end_num_leaves or (end_time is not None and curr_time > end_time):
            break
        rv = NHPP_first_interarrival_time(a=0); rv.set_L(lambda x: L(x + node.time)); lengths = rv.rvs(size=2)
        for i in range(2):
            child = Node(); node.add_child(child)
            child.time = node.time + lengths[i]
            pq.put((child.time,child))
        num_leaves += 1
    if end_time is not None:
        curr_time = min(curr_time,end_time)
    for node in tree.traverse_preorder():
        if node.is_leaf():
            node.label = str(num_leaves); num_leaves -= 1; node.time = curr_time
        if node.is_root():
            node.edge_length = node.time
        else:
            node.edge_length = node.time - node.parent.time
    return tree
