from selectors import EpollSelector
from numpy import uint8
from sys import argv
from collections import deque

from directed_graph import Node
from directed_graph import Graph

def parsegraph(filename):
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            node1,node2 = line.strip().split(',')
            
            if node1 not in graph:
                graph[node1] = set()
            graph[node1].add(node2)

            if node2 not in graph:
                graph[node2] = set()
            graph[node2].add(node1)
    
    return graph

def parseGfa(filename):
    graph = Graph()
    with open(filename, 'r') as f:
        for line in f:
            l_split = line.strip().split('\t')
            if l_split[0] == 'S':
                graph.addNode(l_split[1],l_split[2])
                #print(f'adding node. name {l_split[1]}, len {l_split[2]}')
            elif l_split[0] == 'L':
                graph.addEdge(l_split[1],l_split[2],l_split[3],l_split[4])
                #print(f'adding edge. {l_split[1]}, {l_split[2]}, {l_split[3]}, {l_split[4]}')
    return graph



def detect_snp(node,graph):

    number_operations=0

    stack=[node]
    visited={}
    snp={}

    for el in graph:
        visited[el]=False
        snp[el]=False

    while len(stack) > 0:
        current_node = stack.pop()

        if visited[current_node] or snp[current_node]:
            print(f'should be skipping {current_node}')
            continue

        adjacents = set()
        adjacents |= graph[current_node]
        
        neighbours = set()

        for neighbour in neighbours:
            
            number_operations+=1

            if graph[neighbour]==graph[current_node] :
                snp[current_node]=True
                snp[neighbour]=True
                print(f'setting {current_node} and {neighbour} as SNPs')
                
            if not visited[neighbour] and not snp[neighbour]:
                stack.append(neighbour)
                #print(f'{current_node} does not have SNPs')

        visited[current_node]=True
        
        print(f'Visited {current_node}')
    print(f'Total nodes checked:{number_operations}')
    return snp

def annotate_level(node,graph):

    number_operations=0
    nodes_visited=0

    stack=deque(node)
    visited={}
    graph.nodes[node].depth=uint8(1)
    number_operations+=3

    for el in graph.nodes:
        visited[el]=False
        number_operations+=1

    while len(stack) > 0:
        current_node = stack.popleft()
        if visited[current_node]:
            continue
        print(f'Visiting {current_node}')

        nodes_visited+=1
        #print(graph.nodes[current_node].in_edg)
        n_pred=len(graph.nodes[current_node].in_edg)

        unvisited_predecessor=False
        for predecessor in graph.nodes[current_node].in_edg:
            number_operations+=1

            if not visited[predecessor]:
                stack.append(current_node)
                print('should skip this node')
                unvisited_predecessor=True
                break
        if unvisited_predecessor:        
            continue

        if n_pred == 0: #it is a source
            graph.nodes[current_node].depth=uint8(1)
            number_operations+=1
            #print(f'N_PRED==0: Node {current_node} assigned depth {graph.nodes[current_node].depth}')
        elif n_pred == 1:
            predecessor=graph.nodes[current_node].in_edg[0]
            if len(graph.nodes[predecessor].out_edg)>1:
                graph.nodes[current_node].depth=uint8(graph.nodes[predecessor].depth+1)
                #print(f'N_PRED==1/>1: Node {current_node} assigned depth {graph.nodes[current_node].depth}')

            else:
                graph.nodes[current_node].depth=uint8(graph.nodes[predecessor].depth)
                #print(f'N_PRED==1/=1: Node {current_node} assigned depth {graph.nodes[current_node].depth}')
        elif n_pred > 1:
            min_depth=-1
            for predecessor in graph.nodes[current_node].in_edg:
                number_operations+=1

                if (min_depth<0) or (min_depth>graph.nodes[predecessor].depth):
                    min_depth=graph.nodes[predecessor].depth
            graph.nodes[current_node].depth=max(1,min_depth-1)
            #print(f'N_PRED>1: Node {current_node} assigned depth {graph.nodes[current_node].depth}')
        
            

        visited[current_node]=True

        for next_node in graph.nodes[current_node].out_edg:
            number_operations+=1
            if not visited[next_node]:
                stack.append(next_node)
        



        number_operations+=3
        

    print(f'Total operations done:{number_operations}')
    print(f'Total nodes accessed:{nodes_visited}')
    return 




if __name__ == "__main__":
    #graph = parsegraph(argv[1])

    #print(graph)


    #snps=detect_snp('1',graph)

    #for node in snps:
    #    if snps[node]:
    #        print(node,end=' ')

    graph=parseGfa(argv[1])

    print(graph)

    annotate_level('1',graph)

    for node in graph.nodes:
        print(f'Node {node}, depth {graph.nodes[node].depth}')
