import argparse


def parseGfa(gfa_file):
    edges = []
    nodes_length={}

    with open(gfa_file, 'r') as gf:
        for line in gf:
            elements = line.strip().split('\t')
            if elements[0] == 'S':
                nodes_length[elements[1]] = len(elements[2])
            elif elements[0] == 'P':
                edges.append([elements[1],elements[3]])
            
    return edges,nodes_length

def parseAnn(ann_file, nodes_length):
    with open(ann_file, 'r') as af:
        for line in af:
            node , chr = line.strip().split('\t')
            nodes_length[node].append(chr)

    return nodes_length

def printGraph(out_graph,edgeList):
     with open(out_graph, "w") as out:
        for edge in edgeList:
            print("%d\t%d"%(edge[0],edge[1]), file=out)

def printAnnotations(out_ann,nodes):
     with open(out_ann, "w") as out:
        for node in nodes:
            print("%d\t%d\t%d"%(node[0],node[1],node[2]), file=out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse input')
    parser.add_argument('--graph', '-g', type=str, dest='graph_file', required=True, help='Pangenome graph file [gfa]')
    parser.add_argument('--annotations', '-a', type=str, dest='annotations_file', required=True, help='Annotation file : node,length,chromosome [tsv]')
    parser.add_argument('--outfile', '-o', type=str, dest='outfile', required=True, help='Output file prefix. Do not put extension. 1 [tsv] file with the edge centric graph & one [tsv] file with nodes annotation file.')

    args = parser.parse_args()
    print(args)

    edges , nodes_len = parseGfa(args.graph_file)

    nodes_info = parseAnn(args.annotations_file,nodes_len)

    printGraph(args.outfile+'graph.tsv',edges)

    printAnnotations(args.outfile+'node_annotation.tsv',nodes_info)

