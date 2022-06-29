import argparse

def parse_annotations(annotations_file, haslen=False):
    annotations = {}

    with open(annotations_file, 'r') as af:
        af.readline()
        for line in af:
            sp = line.strip().split('\t')
            if haslen==True: # the second element in the tsv is the length of the node. So for now we don't want it
                if len(sp)>2:
                    annotations[sp[0]] = sp[2]
                else:
                    annotations[sp[0]] = ['']
            else:
                annotations[sp[0]] = sp[1:]
            
    return annotations


def save_annotations(annotations, file):
    with open(file, "w") as f:
        print("node\tannotation", file=f)

        for node in annotations:
            print(f"{node}\t{annotations[node]}", file=f)


def parse_graph(edges_file, verbose=False):
    graph = {}

    arities = [0] * 4

    with open(edges_file, 'r') as ef:
        for line in ef:
            node1, node2 = line.strip().split('\t')

            if node1 not in graph:
                graph[node1] = []
            graph[node1].append(node2)

            if node2 not in graph:
                graph[node2] = []
            graph[node2].append(node1)

    if verbose:
        for node in graph:
            arity = len(graph[node])
            if arity > 2:
                arity = 3
            arities[arity] += 1

        print("Graph arities")
        print(arities[0], arities[1], arities[2], arities[3])
    #me
    #print(graph.get(1))
    #print(graph.get('1'))
    return graph