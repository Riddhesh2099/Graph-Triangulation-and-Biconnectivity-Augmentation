""" Planarity module

This module allows user to check if a graph is planar and provides ways 
to make a non-planar graph planar.

This module contains the following functions:
    *is_Planar: Checks if given graph is planar.
    *make_Planar: Converts the non-planar graph to planar.

"""

import numpy as np
import networkx as nx

def is_Planar(nxgraph):
    """returns a boolean representing whether the graph
     is Planar or not.

    Args:
        nxgraph: An instance of NetworkX Graph object.

    Returns:
        boolean: indicating TRUE if Planar, FALSE otherwise.
    """
    return nx.check_planarity(nxgraph)

def make_Planar(nxgraph):
    """
    Args:
        nxgraph: An instance og NetworkX Graph object.

    Returns: 
        planar_graph: A planar graph which is derived from the input graph
    """
    

