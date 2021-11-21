import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.algorithms.components import connected_components
from networkx.algorithms.planarity import check_planarity
from networkx.utils import arbitrary_element, not_implemented_for

import biconnectivity as bcn
import triangularity as trng


def make_chordal_graph(G):
    """
    :param G: NetworkX graph
    :return: H : NetworkX graph (The chordal enhancement of G)
            alpha : Dictionary (The elimination ordering of nodes of G)
            added_edges: Edges added to G to make H
    ALGORITHM: MCS-M
    """
    H = G.copy()
    alpha = {node: 0 for node in H}
    if nx.is_chordal(H):
        return H, alpha
    chords = set()
    weight = {node: 0 for node in H.nodes()}
    unnumbered_nodes = list(H.nodes())
    for i in range(len(H.nodes()), 0, -1):
        # get the node in unnumbered_nodes with the maximum weight
        z = max(unnumbered_nodes, key=lambda node: weight[node])
        unnumbered_nodes.remove(z)
        alpha[z] = i
        update_nodes = []
        for y in unnumbered_nodes:
            if G.has_edge(y, z):
                update_nodes.append(y)
            else:
                # y_weight will be bigger than node weights between y and z
                y_weight = weight[y]
                lower_nodes = [
                    node for node in unnumbered_nodes if weight[node] < y_weight
                ]
                if nx.has_path(H.subgraph(lower_nodes + [z, y]), y, z):
                    update_nodes.append(y)
                    chords.add((z, y))
        # during calculation of paths the weights should not be updated
        for node in update_nodes:
            weight[node] += 1
    H.add_edges_from(chords)
    edges_added=chords
    return H, alpha,edges_added


def make_graph(G):
    vertex_count = int(input("Enter the number of vertices in the graph: "))
    edge_count = int(input("Enter the number of edges in the graph: "))
    print("Enter each edge in new line(0-based index)")
    for i in range(edge_count):
        line = input()
        node1 = int(line.split()[0])
        node2 = int(line.split()[1])
        G.add_edge(node1, node2)


def Check_Chordality(G, print_op):
    """
    :param G: G is a networkx graph
    :return: Checks if G is Chordal
    """
    if nx.is_chordal(G):
        if (print_op == 1):
            print("Graph is Chordal")
        return True
    else:
        if (print_op == 1):
            print("Graph is NOT Chordal")
        return False


def Triangulate(G):
    """
    :param G: G is a networkx graph 
    :return: Triangulation of G
    """
    # G_triangulated = nx.Graph(G)
    alpha = {node: 0 for node in G}
    list=[]
    if Check_Chordality(G, 0):
        print("Graph is already Triangulated")
        return G,alpha,list
    else:
        print("Triangulating...")
        G_triangulated,Elim_order, new_edges= make_chordal_graph(G)
        return G_triangulated,Elim_order, new_edges

def compre():
    G = nx.Graph()
    make_graph(G)
    nx.draw(G,with_labels=True)
    plt.show()
    ###Biconnection###
    bcn_edges = bcn.biconnect(G)
    print("Biconnecting...")
    G.add_edges_from(bcn_edges)
    nx.draw(G,with_labels=True)
    plt.show()
    ###Triangulation###
    trng_edges = trng.triangulate(G)
    print("Triangulating...")
    G.add_edges_from(trng_edges)
    nx.draw(G,with_labels=True)
    plt.show()
    ##END###

def main():
    G = nx.Graph()
    make_graph(G)

    # G_triangulated, Elim_order, new_edges = Triangulate(G)
    # # plt.subplot(2, 1, 1)
    # print("Edges in input: ", G.number_of_edges())
    # # check_planarity(G)
    # nx.draw(G,with_labels=True)
    # plt.show()
    # print("Elimination Ordering is:",Elim_order)
    # print("Edges added:", new_edges)
    # print("Total Edges now: ",G_triangulated.number_of_edges())
    # # plt.subplot(2,1,2)
    # nx.draw(G_triangulated,with_labels=True)
    # # check_planarity(G_triangulated)
    # plt.show()

    bcn_edges = bcn.biconnect(G)
    print("Biconnecting...")
    G.add_edges_from(bcn_edges)
    nx.draw(G,with_labels=True)
    plt.show()
    trng_edges = trng.triangulate(G)
    print("Triangulating...")
    G.add_edges_from(trng_edges)
    nx.draw(G,with_labels=True)
    plt.show()
    is_planar, embedding = nx.check_planarity(G, counterexample=False)
    print(is_planar)
    nx.draw(embedding,with_labels = True)
    plt.show()

def midsem():
    G = nx.Graph()
    make_graph(G)
    nx.draw(G,with_labels=True)
    plt.show()
    ###Biconnectivity check###
    print("Is graph biconnected?:" + str(bcn.is_Vertex_Biconnected(G)))
    ###Triangulation###
    trng_edges = trng.triangulate(G)
    print("Triangulating...")
    G.add_edges_from(trng_edges)
    nx.draw(G,with_labels=True)
    plt.show()
    ##END###

def only_bicon():
    G = nx.Graph()
    make_graph(G)
    nx.draw(G,with_labels = True)
    plt.show()
    bcn_edges = bcn.biconnect(G)
    G.add_edges_from(bcn_edges)
    nx.draw(G,with_labels=True)
    plt.show()

def only_trng():
    G = nx.Graph()
    make_graph(G)
    nx.draw(G,with_labels = True)
    plt.show()
    trng_edges = trng.triangulate(G)
    G.add_edges_from(trng_edges)
    nx.draw(G,with_labels=True)
    plt.show()

if __name__ == '__main__':
    # main()
    # midsem()
    only_bicon()

