#!/usr/bin/env python3
from math import exp
from scipy.stats import rv_continuous
from scipy.integrate import quad as integral
from treeswift import Node,Tree
from .common import check_end_conditions
try:
    from Queue import PriorityQueue  # ver. < 3.0
except ImportError:
    from queue import PriorityQueue

class NHPP_first_interarrival_time(rv_continuous):
    '''Random variable class for T = first interarrival time of a NHPP with rate function L(t)'''
    def set_L(self, L):
        '''Set the rate function L(t)

        Args:
            ``L`` (``func``): The rate function L(t)
        '''
        self.L = L

    def check_L(self):
        '''Check that the rate function L(t) has been set'''
        if not hasattr(self,'L'):
            raise RuntimeError("Must run set_L function to set rate function L(t) first")

    def _cdf(self, x):
        '''The CDF of T = first interarrival time of a NHPP with rate function L(t)

        Args:
            ``x`` (``float``): A positive number

        Returns:
            F_T(x) = P(T <= x)
        '''
        self.check_L()
        return 1 - exp(-integral(self.L,0,x)[0])
        
    def _pdf(self, x):
        self.check_L()
        return self.L(x) * exp(-integral(self.L,0,x)[0])

def nonhomogeneous_yule_tree(L, end_num_leaves=float('inf'), end_time=float('inf')):
    '''Sample a non-homogeneous Yule tree with speciation rate function L(t). If both an end number of leaves and an end time are specified, the tree sampling will terminate when the first of the two is reached.

    Args:
        ``L`` (``func``): The speciation rate function L(t)

        ``end_num_leaves`` (``int``): The final number of leaves

        ``end_time`` (``float``): The final height of the tree

    Returns:
        A ``Tree`` object storing the sampled non-homogeneous Yule tree
    '''
    check_end_conditions(end_num_leaves,end_time)
    if not callable(L):
        raise TypeError("L must be a 'func', but it was a %s" % str(type(L)))
    tree = Tree(); num_leaves = 1; curr_time = 0; time = dict()
    rv = NHPP_first_interarrival_time(a=0); rv.set_L(L); time[tree.root] = rv.rvs(size=1)[0]
    pq = PriorityQueue(); pq.put((time[tree.root],tree.root))
    while True:
        curr_time,node = pq.get()
        if num_leaves == end_num_leaves or curr_time > end_time:
            break
        rv = NHPP_first_interarrival_time(a=0); rv.set_L(lambda x: L(x + time[node])); lengths = rv.rvs(size=2)
        for i in range(2):
            child = Node(); node.add_child(child)
            time[child] = time[node] + lengths[i]
            pq.put((time[child],child))
        num_leaves += 1
    curr_time = min(curr_time,end_time)
    for node in tree.traverse_preorder():
        if node.is_leaf():
            node.label = str(num_leaves); num_leaves -= 1; time[node] = curr_time
        if node.is_root():
            node.edge_length = time[node]
        else:
            node.edge_length = time[node] - time[node.parent]
    return tree
