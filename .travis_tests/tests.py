#!/usr/bin/env python
from treesap import nonhomogeneous_yule_tree
if __name__ == "__main__":
    tree = nonhomogeneous_yule_tree(lambda x: 2*x, end_num_leaves=100)
