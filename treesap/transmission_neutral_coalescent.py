#!/usr/bin/env python3
from .common import check_end_conditions,check_transmission_event,Set
from numpy.random import exponential
from scipy.stats import truncexpon
from treeswift import Node,Tree

def transmission_neutral_coalescent_tree(transmission_network, sample_times, rate=1):
    '''Sample a tree under the pure-neutral coalescent model constrained to a given transmission network with given patient sampling times.

    Args:
        ``transmission_network`` (``list``): The transmission network as a ``list`` of ``(u,v,t)`` tuples denoting the transmission from ``u`` to ``v`` at time ``t``. The transmission network must be sorted in ascending order of time

        ``sample_times`` (``dict``): The times at which each individual was sampled (i.e., the times of the leaves) as a ``dict`` in which keys are individuals from ``transmission_network`` and the value associated with an individual ``u`` is a ``list`` of times at which ``u`` was sampled (i.e., the times of the leaves from individual ``u``)

        ``rate`` (``float``): The rate of the Poisson process of coalescing two lineages

    Returns:
        A ``Tree`` object storing the sampled pure-neutral tree, where leaves are labeled ``ID|u|t``, where ``ID`` is a unique identifier for the leaf, ``u`` is the corresponding individual from ``transmission_network``, and ``t`` is the sample time (which equals the leaf's distance from the root). If there are multiple seed individuals (infected beforehand), a tree will be output for each.
    '''
    if not isinstance(transmission_network,list):
        raise TypeError("transmission_network must be a list, but it was a %s" % str(type(transmission_network)))
    if not isinstance(sample_times,dict):
        raise TypeError("sample_times must be a dict, but it was a %s" % str(type(sample_times)))
    time = dict(); ID = 0; root = dict(); leaves = dict(); infected_by = dict(); to_visit = set(); infection_time = dict()
    for i in range(len(transmission_network)-1,-1,-1):
        check_transmission_event(transmission_network[i])
        if i != 0 and transmission_network[i][2] < transmission_network[i-1][2]:
            raise ValueError("transmission_network must be sorted in ascending order of time")
        u,v,t = transmission_network[i]
        if v in infection_time:
            raise ValueError("Encountered duplicate transmission recipient: %s" % str(v))
        else:
            infection_time[v] = t
        if u not in infected_by:
            infected_by[u] = list()
        if v not in infected_by:
            infected_by[v] = list()
        if v not in sample_times:
            raise KeyError("Individual not in sample_times: %s" % str(v))
        if not isinstance(sample_times[v],list):
            if isinstance(sample_times[v],float) or isinstance(sample_times[v],int):
                sample_times[v] = [sample_times[v]]
            elif isinstance(sample_times[v],set):
                sample_times[v] = list(sample_times[v])
            else:
                raise TypeError("Values in sample_times must be list")
        if u is not None and u != 'None':
            infected_by[u].append(v); to_visit.add(u)
        leaves[v] = list()
        for w in infected_by[v]:
            if w not in root:
                raise ValueError("Missing links in transmission_network")
            leaves[v].append(root[w]); del root[w]
        for st in sample_times[v]:
            if not isinstance(st,float) and not isinstance(st,int):   
                raise TypeError("Values in sample_times must be list of float")
            newnode = Node(label='%d|%s|%f' % (ID,str(v),st)); ID += 1; time[newnode] = st; leaves[v].append(newnode)
        leaves[v].sort(key=lambda x: time[x], reverse=True); lineages = Set(); curr_time = time[leaves[v][0]]
        for w in leaves[v]:
            if time[w] < curr_time:
                while len(lineages) > 1:
                    L = rate*len(lineages)*(len(lineages)-1)/2.; coal_time = curr_time - exponential(1./L)
                    if coal_time >= time[w]:
                        c1 = lineages.pop(); c2 = lineages.pop(); newnode = Node(); time[newnode] = coal_time; curr_time = coal_time; newnode.add_child(c1); newnode.add_child(c2); lineages.add(newnode)
                curr_time = time[w]
            lineages.add(w)
        while len(lineages) != 1:
            L = rate*len(lineages)*(len(lineages)-1)/2.; coal_time = curr_time - truncexpon.rvs(curr_time-t, scale=1./L)
            c1 = lineages.pop(); c2 = lineages.pop(); newnode = Node(); time[newnode] = coal_time; curr_time = coal_time; newnode.add_child(c1); newnode.add_child(c2); lineages.add(newnode)
        root[v] = lineages.pop(); to_visit.discard(v); del leaves[v]
    if len(to_visit) != 0:
        raise ValueError("Malformed transmission network. Missing the following seeds:\n%s" % '\n'.join(str(v) for v in to_visit))
    out = list()
    for k,r in root.items():
        if r.is_root():
            tmp = Tree(); tmp.root = r; out.append(tmp)
            for node in tmp.traverse_preorder():
                if node.is_root():
                    node.edge_length = time[node] - infection_time[k]
                else:
                    node.edge_length = time[node] - time[node.parent]
    return out
