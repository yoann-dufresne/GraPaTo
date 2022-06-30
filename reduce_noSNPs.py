import argparse
from platform import node

from yaml import parse

def parse_graph(gfaFile, verbose=False):
    graph = {}
    nodelength = {}
    firstnode = 0

    with open(gfaFile, 'r') as gfa:
        for line in gfa:
            elements = line.strip().split('\t')

            if elements[0] == 'S':
                nodelength[elements[1]] = len(elements[2])
                if firstnode == 0:
                    firstnode=elements[1]

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

    return graph, nodelength, firstnode


def breadth_first_search_removing_snp(node, graph,nodeslength,verbose=False):
    stack = [node]
    to_remove={} 
    already_seen={}

    while len(stack)>0:
        local_nodes = set()
        current_node = stack.pop()
        already_seen[current_node] = True
        

        for neighbor in graph[current_node]:
            if (neighbor in already_seen) and (not already_seen[neighbor]):
                local_nodes.add(neighbor)

        
        if len(local_nodes) != 2:
            if already_seen.get(node) != None:
                    stack.append(node)
            continue
        
        for node in local_nodes:
            if nodeslength[node] != 1:
                if already_seen.get(node) != None:
                    stack.append(node)
                continue
                
        node1 , node2 = local_nodes

        if graph[node1] != graph[node2]:
            if already_seen.get(node) != None:
                    stack.append(node)
            continue
        
        neig_n1 = graph[node1]
        neig_n2 = graph[node2]

        neig_n1.pop(node)
        neig_n2.pop(node)
        if (len(neig_n1) == len(neig_n2)) and (len(neig_n1)==1):
            nextnode=neig_n1.pop()
            to_remove[node1] = True
            stack.append(nextnode)
            continue

        for node in local_nodes:
                if already_seen.get(node) != None:
                    stack.append(node)
    
    return to_remove

def printgraph(gfaFile,outfile,to_remove):
    with open(gfaFile, 'r') as gfa:
        for line in gfa:
            elements = line.strip().split('\t')
            if elements[0] == 'S':
                if to_remove.get(elements[1]) != None:
                    print(line,file=outfile)
            elif elements[0] == 'L':
                if (to_remove.get(elements[1]) != None) and (to_remove.get(elements[3]) != None):
                    print(line,file=outfile)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Disrupt SNPs')
    parser.add_argument('--graph', '-g', type=str, dest='graph_file', required=True, help='Graph file in GFA format.')
    parser.add_argument('--outfile', '-o', type=str, dest='outfile', required=True, help='Graph file with one of the two snps removed.')

    args = parser.parse_args()
    print(args)

    graph, nodes_length, firstnode = parse_graph(args.graph_file,verbose=True)
    print('input finished')
    nodes_to_remove = breadth_first_search_removing_snp(firstnode,graph,nodes_length,verbose=True)
    print('removed finished')
    printgraph(args.graph_file,args.outfile,nodes_to_remove)