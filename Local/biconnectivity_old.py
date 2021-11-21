"""Biconnectivity Augmentation Module

This module allows user to check if the graph is biconnected and can
make it biconnected with minimum number of extra adjacencies.
(Refer documentation)

This module contains the following functions:

    * is_biconnected - returns a boolean representing whether the graph
     is biconnected or not.
    * 
"""
import numpy as np
import networkx as nx

def utilfnc_bccsets(graph, u, bccsets, parent, low, disc, st):
    """Utility function for bcc sets.

    Args:
        graph: An instance of InputGraph object.
        * To be finished...

    Returns:
        None
    """
    children = 0
    disc[u] = graph.time
    low[u] = graph.time
    graph.time += 1
    for v in range(graph.nodecnt):
        if graph.matrix[u][v] == 1:
            if disc[v] == -1:
                parent[v] = u
                children += 1
                st.append((u, v))
                utilfnc_bccsets(graph
                    , v
                    , bccsets
                    , parent
                    , low
                    , disc
                    , st)
                low[u] = min(low[u], low[v])
                if parent[u] == -1 and children > 1\
                 or parent[u] != -1 and low[v] >= disc[u]:
                    graph.bcccnt += 1  
                    graph.articulationpts[u] = True
                    w = -1
                    while w != (u, v):
                        w = st.pop()
                        bccsets[(graph.bcccnt) - 1].add(w[0])
                        bccsets[(graph.bcccnt) - 1].add(w[1])
            elif v != parent[u] and low[u] > disc[v]:
                low[u] = min(low[u], disc[v])
                st.append((u, v))

def init_bccsets(graph):
    """Initializes biconnected sets in the graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    disc = [-1] * (graph.nodecnt)
    low = [-1] * (graph.nodecnt)
    parent = [-1] * (graph.nodecnt)
    st = []
    
    graph.bcccnt = 0
    for i in range(graph.nodecnt):
        if disc[i] == -1:
            utilfnc_bccsets(graph
                , i
                , graph.bccsets
                , parent
                , low
                , disc
                , st)
        if st:
            graph.bcccnt = graph.bcccnt + 1
            while st:
                w = st.pop()
                graph.bccsets[(graph.bcccnt)-1].add(w[0])
                graph.bccsets[(graph.bcccnt)-1].add(w[1])
    graph.bccsets = [x for x in graph.bccsets if x]
    

def find_articulationpnts(graph):
    """Finds artculation points in the graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    for i in range(graph.nodecnt):
        if graph.articulationpts[i]:
            graph.articulationptscnt += 1
            graph.articulationpts_val.append(i)
            graph.articulationpts_sets[i].add(i)
    graph.articulationpts_sets = [x for x in graph.articulationpts_sets if x]

def find_neighbours(graph, node):
    """Finds neighbour of a given node.

    Args:
        graph: An instance of InputGraph object.
        node: An integer representng node whose 
              neighbours are to be evaluated.

    Returns:
        None
    """
    nxgraph = nx.from_numpy_matrix(graph.matrix)
    nbrs = []
    for n in nxgraph.neighbors(node):
        nbrs.append(n)
    return nbrs

def make_biconnected(graph):
    """Finds edges to be added to make graph biconnected.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    for i in range(len(graph.articulationpts_val)):
        nbrs =find_neighbours(graph,graph.articulationpts_val[i])
        for j in range(0, (len(nbrs) - 1)):
            if not in_sameblock(graph,nbrs[j], nbrs[j+1]):
                graph.matrix[nbrs[j]][nbrs[j+1]] = 1
                graph.matrix[nbrs[j+1]][nbrs[j]] = 1
                graph.added_edges.add((nbrs[j], nbrs[j+1]))
                if (graph.articulationpts_val[i], nbrs[j]) in graph.added_edges or\
                        (nbrs[j], graph.articulationpts_val[i]) in graph.added_edges:
                    graph.matrix[graph.articulationpts_val[i]][nbrs[j]] = 0
                    graph.matrix[nbrs[j]][graph.articulationpts_val[i]] = 0
                    graph.removed_edges.add((graph.articulationpts_val[i], nbrs[j]))
                    graph.removed_edges.add((nbrs[j], graph.articulationpts_val[i]))
                if (graph.articulationpts_val[i], nbrs[j+1]) in graph.added_edges or\
                        (nbrs[j+1], graph.articulationpts_val[i]) in graph.added_edges:
                    graph.matrix[graph.articulationpts_val[i]][nbrs[j+1]] = 0
                    graph.matrix[nbrs[j+1]][graph.articulationpts_val[i]] = 0
                    graph.removed_edges.add((graph.articulationpts_val[i], nbrs[j+1]))
                    graph.removed_edges.add((nbrs[j+1], graph.articulationpts_val[i]))
    graph.bcn_edges = graph.added_edges - graph.removed_edges
    graph.edgecnt += len(graph.bcn_edges)
    

def remove_articulation_points_from_bcc_sets(graph):
    for i in graph.articulationpts_val:
        for j in range(graph.articulationptscnt + 1):
            if i in graph.bccsets[j]:
                graph.bccsets[j].remove(i)

def in_sameblock(graph, node1, node2):
    """Finds if two vertices are in same block in the graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        boolean: A boolean representing if two nodes
                 are in the same block.
    """
    for i in range(len(graph.bccsets)):
        if (node1 in graph.bccsets[i]) and (node2 in graph.bccsets[i]):
            return True
    return False



