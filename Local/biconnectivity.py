"""Biconnectivity Augmentation Module

This module allows user to check if the graph is biconnected and can
make it biconnected.

This module contains the following functions:

    * is_biconnected - returns a boolean representing whether the graph
        is biconnected or not.
    * biconnect - checks if a graph needs to be biconnected 
        and returns edges to be added to make it biconnected
"""
from os import remove
import numpy as np
import networkx as nx


def is_Edge_Biconnected(nxgraph):
    """returns a boolean representing whether the graph
     is edge biconnected or not.

    Args:
        nxgraph: An instance of NetworkX Graph object.

    Returns:
        boolean: indicating TRUE if biconnected, FALSE otherwise.
    """
    return nx.is_k_edge_connected(nxgraph, k=2)

def is_Vertex_Biconnected(nxgraph):
    """returns a boolean representing whether the graph 
    is vertex biconnected or not.
    
    Args:
        nxgraph: An instance of NetworkX Graph object.
    
    Returns:
        boolean: indicating TRUE if biconnected, FALSE otherwise.
    """
    return nx.is_biconnected(nxgraph)

def edge_Biconnect(nxgraph):
    """ checks if a graph needs to be biconnected 
    and returns edges to be added to make it biconnected
    
    Args:
        # matrix: Adjacency matrix of the said graph.
        nxgraph(for testing): an instance of NetworkX graph object.
    
    Returns:
        ebicon_edges: Edges to be added to make the graph edge biconnected
    """
    # nxgraph = nx.from_numpy_matrix(matrix)
    bicon_edges = []
    if not is_Edge_Biconnected(nxgraph):
        ebicon_edges = sorted((nx.k_edge_augmentation(nxgraph, k=2)))
    return ebicon_edges

def get_Cutvertices(nxgraph):
    """
    Args:
        nxgraph: an instance of NetworkX graph object.
    
    Returns:
        articulation_list: List of all articulation points in the graph
    """
    articulation_list = list(nx.articulation_points(nxgraph))
    return articulation_list

def get_Biconnected_Components(nxgraph):
    """
    Args:
        nxgraph: an instance of NetworkX graph object.
    
    Returns:
        components: Set of biconnected components.
    """
    components = nx.biconnected_components(nxgraph)
    return components

def same_Component(nxgraph,u,v):
    """
    Args: 
        nxgraph: an instance of Networkx graph object
        u,v: vertices to be checked
    
    Returns:
        boolean: TRUE if vertices are in the same biconnected component else FALSE.
    """
    components = list(get_Biconnected_Components(nxgraph))
    for itr in range(len(components)):
        if (u in components[itr]) and (v in components[itr]):
            return True
    return False

def biconnect(nxgraph):
    """
    Args:
        # matrix: Adjacency matrix of the said graph.
        nxgraph(for testing): an instance of NetworkX graph object.
    
    Returns:
        bicon_edges: Edges to be added to make the graph biconnected
    """
    # nxgraph = nx.from_numpy_matrix(matrix)
    articulation_points = get_Cutvertices(nxgraph)
    bicon_edges = set()
    added_edges = set()
    removed_edges = set()
    for i in range(len(articulation_points)): 
        neighbors = list(nx.neighbors(nxgraph,articulation_points[i]))
        for j in range(0,len(neighbors)-1):
            if not same_Component(nxgraph,neighbors[j],neighbors[j+1]):
                added_edges.add((neighbors[j],neighbors[j+1]))
                if(articulation_points[i], neighbors[j]) in added_edges\
                    or (neighbors[j],articulation_points[i]) in added_edges:
                    removed_edges.add((articulation_points[i],neighbors[j]))
                    removed_edges.add((neighbors[j],articulation_points[i]))
                if (articulation_points[i],neighbors[j+1]) in added_edges\
                    or (neighbors[j+1],articulation_points[i]) in added_edges:
                    removed_edges.add((articulation_points[i],neighbors[j+1]))
                    removed_edges.add((neighbors[j+1],articulation_points[i]))
    bicon_edges = added_edges - removed_edges
    return bicon_edges
