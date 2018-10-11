#!/usr/bin/env python3
from random import randint
class Set:
    '''Set class to add, remove, find, and pick random elements in O(1) time'''
    def __init__(self):
        '''Initialize set'''
        self.a = list(); self.m = dict()

    def __len__(self):
        '''Return number of elements in this set

        Returns:
            The number of elements in this set
        '''
        return len(self.a)

    def __contains__(self, key):
        '''Check if ``key`` exists in this set

        Args:
            ``key``: The item to check

        Returns:
            ``True`` if ``key`` exists in this set, otherwise ``False``
        '''
        return key in self.m

    def add(self, x):
        '''Add new element to this set

        Args:
            ``x`` (``object``): The new element to add
        '''
        if x in self.m:
            return
        i = len(self.a); self.a.append(x); self.m[x] = i

    def remove(self, x):
        '''Remove an element from this set

        Args:
            ``x`` (``object``): The element to remove
        '''
        if x not in self.m:
            return
        i = self.m[x]; del self.m[x]
        last_i = len(self.a)-1; last = self.a[last_i]; self.a[last_i] = x; self.a[i] = last
        self.a.pop()
        if last in self.m:
            self.m[last] = i

    def random(self):
        '''Return a random (not arbitrary) element from this set

        Returns:
            A random element from this set
        '''
        assert len(self.a) != 0, "Calling random() on an empty set"
        return self.a[randint(0,len(self.a)-1)]

    def pop(self):
        '''Remove and return a random (not arbitrary) element from this set. Equivalent to calling random() and then remove()

        Returns:
            A random element from this set
        '''
        out = self.random(); self.remove(out); return out

def check_end_conditions(end_num_leaves, end_time):
    '''Check end_num_leaves and end_time parameters'''
    if end_num_leaves == float('inf') and end_time == float('inf'):
        raise ValueError("Must specify either end_num_leaves or end_time (or both)")
    if end_num_leaves != float('inf') and not isinstance(end_num_leaves,int):
        raise TypeError("end_num_leaves must be an integer")
    elif end_num_leaves < 1:
        raise ValueError("end_num_leaves must be at least 1")
    if not isinstance(end_time,float) and not isinstance(end_time,int):
        raise TypeError("end_time must be a float")
    if end_time <= 0:
        raise ValueError("end_time must be positive")

def check_transmission_event(e):
    if not isinstance(e,tuple) and not isinstance(e,list):
        raise TypeError("transmission_network must be a list of tuples")
    if len(e) != 3:
        raise ValueError("transmission_network must be a list of tuples of length 3")
    if not isinstance(e[2],float) and not isinstance(e[2],int):
        raise ValueError("The times of the tuples in transmission_network must be floats")
    if e[0] == e[1]:
        raise ValueError("Encountered transmission event with two identical individuals")
