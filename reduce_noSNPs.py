import argparse

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

def remove_snp(starting_node,graph,nodes_length,snp_len=1,max_parallel_nodes=3,verbose=False):
    stack=[starting_node]
    to_remove={} # true->remove; false->already seen but not remove.
    removed_num=0

    while len(stack)>0:

        current_node = stack.pop()
        #print(f'visiting {current_node}')

        if to_remove.get(current_node) != None:
            for neighbor in graph[current_node]:
                #print(f'might add {neighbor}')
                if to_remove.get(neighbor) == None:
                    stack.append(neighbor)
            continue

        stack.extend(graph[current_node])
        
        local_nodes=set()
        for neighbor in graph[current_node]:
            if to_remove.get(neighbor) == None:
                local_nodes.add(neighbor)

        print(f"local_nodes {local_nodes} , to_remove_len {len(to_remove)}")

        if (len(local_nodes) <= max_parallel_nodes) and (len(local_nodes)>0):
            if all(nodes_length[node]<= snp_len for node in local_nodes) and (all(len(graph[node])==2 for node in local_nodes)):
                Keeping_node=local_nodes.pop()
                if (all(graph[node]==graph[Keeping_node] for node in local_nodes)):
                    to_remove[Keeping_node]=False
                    for node in local_nodes:
                        to_remove[node]=True
                        removed_num+=1


        to_remove[current_node]=False

    return removed_num, to_remove

def printgraph(gfaFile,outfile,to_remove):
    with open(outfile, 'w') as out:
        with open(gfaFile, 'r') as gfa:
            for line in gfa:
                elements = line.strip().split('\t')
                if elements[0] == 'S':
                    if not to_remove.get(elements[1]):
                        print(line,file=out,end='')
                elif elements[0] == 'L':
                    if (not to_remove.get(elements[1])) and (not to_remove.get(elements[3])):
                        print(line,file=out,end='')





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Disrupt SNPs')
    parser.add_argument('--graph', '-g', type=str, dest='graph_file', required=True, help='Graph file in GFA format.')
    parser.add_argument('--outfile', '-o', type=str, dest='outfile', required=True, help='Graph file with one of the two snps removed.')

    args = parser.parse_args()
    print(args)

    graph, nodes_length, firstnode = parse_graph(args.graph_file,verbose=True)
    print('input finished')
    #nodes_to_remove = breadth_first_search_removing_snp(firstnode,graph,nodes_length,verbose=True)
    num_removed, nodes_to_remove = remove_snp(firstnode,graph,nodes_length,snp_len=5,verbose=True)
    print('removed finished')
    printgraph(args.graph_file,args.outfile,nodes_to_remove)

    print(num_removed)