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


def save_graph(graph, file):
    with open(file, "w") as f:
        for node in graph:
            for neighbor in graph[node]:
                if node < neighbor:
                    print(f"{node}\t{neighbor}", file=f)


def compact(idx, nodes, graph, annotations):
    new_node = f"m_{idx}"
    graph[new_node] = []
    annotations[new_node] = annotations[list(nodes)[0]]

    for node in nodes:
        # Modify the graph
        for neighbor in graph[node]:
            if neighbor not in nodes:
                # adding external neighbor to new_node
                graph[new_node].append(neighbor)
                # remove old node from neighbor
                graph[neighbor].remove(node)
                # adding new_node to external neighbor
                if new_node not in graph[neighbor]:
                    graph[neighbor].append(new_node)

        # Modify the annotations
        del annotations[node]
        del graph[node]
    
    return new_node


arity_too_large = 0
node_already_seen = 0
different_annotation = 0


def breadth_first_search(node, graph, annotations, already_seen, verbose=False):
    stack = [node]
    already_seen[node] = True
    local_nodes = set()
    local_annotation = annotations[node]

    # Stats for verbose
    global arity_too_large
    global node_already_seen
    global different_annotation

    while len(stack) > 0:
        current_node = stack.pop()
        local_nodes.add(current_node)

        for neighbor in graph[current_node]:
            if (neighbor in already_seen) and (not already_seen[neighbor]) and (annotations[neighbor] == local_annotation):
                already_seen[neighbor] = True
                stack.append(neighbor)
            elif verbose:
                if neighbor not in already_seen:
                    arity_too_large += 1
                elif already_seen[neighbor]:
                    node_already_seen += 1
                else:
                    different_annotation += 1

    return local_nodes



def reduce(annotations, graph, compact_index):
    # prepare all the nodes with arity <= 2
    already_seen = {}
    for node in graph:
        if len(graph[node]) <= 2:
            already_seen[node] = False
    print("number of nodes inside already_seen", len(already_seen))

    with open(compact_index, "w") as ci:
        print (f"compacted_node\tcompacted_list", file=ci)
        # Walk
        idx = 0
        for node in already_seen:
            if already_seen[node]:
                continue
            local_nodes = breadth_first_search(node, graph, annotations, already_seen, verbose=True)
            if len(local_nodes) > 1:
                new_node = compact(idx, local_nodes, graph, annotations)
                local_nodes = list(local_nodes)
                local_nodes.sort()
                print(f"{new_node}\t{','.join(local_nodes)}", file=ci)
                idx += 1

        # Stats for verbose
        global arity_too_large
        global node_already_seen
        global different_annotation
        print(arity_too_large, different_annotation, node_already_seen)

    return graph, annotations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Propagate annotation')
    parser.add_argument('--graph', '-g', type=str, dest='graph_file', required=True, help='Graph file (edge centric) [tsv]')
    parser.add_argument('--annotations', '-a', type=str, dest='annotations_file', required=True, help='Annotation file [tsv]')
    parser.add_argument('--outprefix', '-o', type=str, dest='outprefix', required=True, help='Prefix for all the output files.')


    args = parser.parse_args()
    print(args)

    annotations = parse_annotations(args.annotations_file,haslen=True)
    graph = parse_graph(args.graph_file, verbose=True)
    print(len(annotations), len(graph))

    #print(annotations.get('1'))
    #print(annotations.get(1))

    compact_index = f"{args.outprefix}_compact_index.tsv"
    reduced_graph, reduced_annotations = reduce(annotations, graph, compact_index)

    # Output the annotations
    annotations_file = f"{args.outprefix}_annotations.tsv"
    save_annotations(reduced_annotations, annotations_file)

    # Output the reduced graph
    graph_file = f"{args.outprefix}_edges.tsv"
    print(len(graph))
    save_graph(reduced_graph, graph_file)
