# Work File for new ideas or rough functions.

""" Idea is to try generate ALL possible biconnected graphs from given one connected, or non-connected graph.
    Currently trying to get all possible biconnected graphs on given n vertices.
"""
import numpy as np
import networkx as nx
import tkinter as tk
import matplotlib.pyplot as plt
import time

def make_graphs(n=2, i=None, j=None):
    """Make a graph recursively, by either including, or skipping each edge.

    Edges are given in lexicographical order by construction."""
    out = []
    if i is None: # First call

        out  = [[(0,1)]+r for r in make_graphs(n=n, i=0, j=1)]
    elif j<n-1:
        out += [[(i,j+1)]+r for r in make_graphs(n=n, i=i, j=j+1)]
        out += [          r for r in make_graphs(n=n, i=i, j=j+1)]
    elif i<n-1:
        out = make_graphs(n=n, i=i+1, j=i+1)
    else:
        out = [[]]
    return out

# def connected(g):
#     """Check if the graph is fully connected, with Union-Find."""
#     nodes = set([i for e in g for i in e])
#     roots = {node: node for node in nodes}

#     def _root(node, depth=0):
#         if node==roots[node]: return (node, depth)
#         else: return _root(roots[node], depth+1)

#     for i,j in g:
#         ri,di = _root(i)
#         rj,dj = _root(j)
#         if ri==rj: continue
#         if di<=dj: roots[ri] = rj
#         else:      roots[rj] = ri
#     return len(set([_root(node)[0] for node in nodes]))==1

def perm(n, s=None):
    """All permutations of n elements."""
    if s is None: return perm(n, tuple(range(n)))
    if not s: return [[]]
    return [[i]+p for i in s for p in perm(n, tuple([k for k in s if k!=i]))]

def permute(g, n):
    """Create a set of all possible isomorphic codes for a graph,

    as nice hashable tuples. All edges are i<j, and sorted lexicographically."""
    ps = perm(n)
    out = set([])
    for p in ps:
        out.add(tuple(sorted([(p[i],p[j]) if p[i]<p[j]
                              else (p[j],p[i]) for i,j in g])))
    return list(out)

def filter(gs, target_nv):
    """Filter all improper graphs: those with not enough nodes,

    those not fully connected, and those isomorphic to previously considered."""
    mem = set({})
    gs2 = []
    for g in gs:
        nv = len(set([i for e in g for i in e]))
        if nv != target_nv:
            continue
        if not is_planar_bicon(g):
            continue
        if tuple(g) not in mem:
            gs2.append(g)
            mem |= set(permute(g, target_nv))
    return gs2

def is_planar_bicon(g):
    G = nx.Graph()
    G.add_edges_from(g)
    if(nx.is_biconnected(G) and nx.check_planarity(G)):
        return True
    else:
        return False

def my_plot(graphs, figsize = 14 , dotsize = 20):
    num = len(graphs)
    fig = plt.figure()

    k = int(np.sqrt(num)) #for sub-plotting
    i = 1                 #for sub-plotting
    
    for g in graphs:
        plt.subplot(k+1,k+1,i+1)
        gnx = nx.Graph()
        gnx.add_edges_from(g)
        nx.draw_kamada_kawai(gnx, node_size = dotsize)
        print('.', end='')
        i+=1
    

def driver():
    start_time = time.time()
    NV = 5
    gs = make_graphs(NV)
    gs = filter(gs, NV)
    my_plot(gs)
    print(time.time()-start_time)
    plt.show()

if __name__ == "__main__":
    driver()



######
# def all_biconnected(gs):
#     """Filter all graphs for biconnectivity."""
#     gs_bicon = []
#     for g in gs:
#         if (is_bicon(g)):
#             gs_bicon.append(g)

# def plot_graphs(graphs, figsize=14, dotsize=20):
#     """Utility to plot a lot of graphs from an array of graphs.

#     Each graphs is a list of edges; each edge is a tuple."""
#     n = len(graphs)
#     fig = plt.figure(figsize=(figsize,figsize))
#     fig.patch.set_facecolor('white') # To make copying possible (white background)

#     k = int(np.sqrt(n))
#     for i in range(n):
#         plt.subplot(k+1,k+1,i+1)
#         g = nx.Graph() # Generate a Networkx object

#         for e in graphs[i]:            
#             g.add_edge(e[0],e[1])
#         nx.draw_kamada_kawai(g, node_size=dotsize)
#         print('.', end='')
# _______________________________________________________________________
