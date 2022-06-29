import argparse
from platform import node

def parse_graph(gfaFile, verbose=False):
    graph = {}
    nodelength = {}

    with open(gfaFile, 'r') as gfa:
        for line in gfa:
            elements = line.strip().split('\t')

            if elements[0] == 'S':
                nodelength[elements[1]] = len(elements[2])

            if elements[0] == 'L':
                node1 = elements[1]
                node2 = elements[3]

                if node1 not in graph:
                    graph[node1] = []
                graph[node1].append(node2)

                if node2 not in graph:
                    graph[node2] = []
                graph[node2].append(node1)

    if verbose:
        print(f'Number of nodes {len(graph)}')


    
    return graph, nodelength


def breadth_first_search(graph,nodeslength,already_seen,verbose=False):
