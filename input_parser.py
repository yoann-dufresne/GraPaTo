import argparse

def parseGfa(gfa_file):
    edges = []
    nodes_length={}

    with open(gfa_file, 'r') as gf:
        for line in gf:
            elements = line.strip().split('\t')
            if elements[0] == 'S':
                nodes_length[elements[1]] = [len(elements[2])]
            elif elements[0] == 'L':
                edges.append([elements[1],elements[3]])
            
    return edges,nodes_length

def parseAnn(ann_file, nodes_length):
    with open(ann_file, 'r') as af:
        for line in af:
            chrom_info = line.strip().split('\t')
            node = chrom_info[0]
            if nodes_length.get(node) != None:
                nodes_length[node].extend(chrom_info[1:])

    return nodes_length

def printGraph(out_graph,edgeList):
     with open(out_graph, "w") as out_file:
        for edge in edgeList:
            print(f"{edge[0]}\t{edge[1]}\n",end='',file=out_file)

def printAnnotations(out_ann,nodes):
     with open(out_ann, "w") as out_file:
        print(f'Node\tLength\tChromosome(s)', file=out_file)
        for node in nodes:
            out=''
            for el in nodes[node]:
                out+=str(el)+'\t'
            print(f"{node}\t{out[:-1]}", file=out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse input')
    parser.add_argument('--graph', '-g', type=str, dest='graph_file', required=True, help='Pangenome graph file [gfa]')
    parser.add_argument('--annotations', '-a', type=str, dest='annotations_file', required=True, help='Annotation file : node,length,chromosome [tsv]')
    parser.add_argument('--outfile', '-o', type=str, dest='outfile', required=True, help='Output file prefix. Do not put extension. 1 [tsv] file with the edge centric graph & one [tsv] file with nodes annotation file.')

    args = parser.parse_args()
    print(args)

    edg , nodes = parseGfa(args.graph_file)

    nodes_info = parseAnn(args.annotations_file,nodes)

    printGraph(args.outfile+'_graph.tsv',edg)

    printAnnotations(args.outfile+'_node_annotation.tsv',nodes_info)