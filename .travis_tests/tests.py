#!/usr/bin/env python3
from treesap import nonhomogeneous_yule_tree,yule_tree
if __name__ == "__main__":
    tree = nonhomogeneous_yule_tree(lambda x: 2*x, end_num_leaves=100)
    tree = yule_tree(1, end_num_leaves=100)
