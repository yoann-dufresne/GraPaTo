import argparse




def parse_annotations(annotations_file):
    annotations = {}

    with open(annotations_file, 'r') as af:
        for line in af:
            sp = line.strip().split('\t')
            annotations[sp[0]] = sp[2]
            
    return annotations


def parse_graph(edges_file):
    graph = {}

    with open(edges_file, 'r') as ef:
        for line in ef:
            node1, node2 = line.strip().split('\t')

            if node1 not in graph:
                graph[node1] = []
            graph[node1].append(node2)

            if node2 not in graph:
                graph[node2] = []
            graph[node2].append(node1)

    return graph


def propagate(graph, annotations):
    # Create dictionaries for unanotated nodes
    new_annotations = {}
    already_seen = {}
    for node in graph:
        if node not in annotations:
            new_annotations[node] = set()
            already_seen[node] = False

    # Walk
    for node in already_seen:
        if already_seen[node]:
            continue
        local_nodes, local_annotations = breadth_first_search(node, graph, annotations, already_seen)
        for new_node in local_nodes:
            new_annotations[new_node] = local_annotations

    return new_annotations


def breadth_first_search(node, graph, annotations, already_seen):
    stack = [node]

    local_annotations = set()
    local_nodes = set()

    while len(stack) > 0:
        current_node = stack.pop()
        already_seen[current_node] = True
        local_nodes.add(current_node)

        for neighbor in graph[current_node]:
            # Is it annotated ?
            if neighbor in annotations:
                local_annotations.add(annotations[neighbor])
            # Previously seen ?
            elif not already_seen[neighbor]:
                stack.append(neighbor)

    return local_nodes, local_annotations


def output_annotations(out_file, annotations, new_annotations):
    multi_annotation = 0

    with open(out_file, "w") as out:
        print("node\tannotation\tpropagated", file=out)

        # Previously annotated
        for node in annotations:
            print(f"{node}\t{annotations[node]}\tF", file=out)

        # Newly annotated
        for node in new_annotations:
            lst_annotations = list(new_annotations[node])
            if len(lst_annotations) > 1:
                multi_annotation += 1
            lst_annotations.sort()
            str_annotations = ",".join(lst_annotations)
            print(f"{node}\t{str_annotations}\tT", file=out)

    print("Number of nodes multi annotated", multi_annotation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Propagate annotation')
    parser.add_argument('--graph', '-g', type=str, dest='graph_file', required=True, help='Graph file (edge centric) [tsv]')
    parser.add_argument('--annotations', '-a', type=str, dest='annotations_file', required=True, help='Annotation file [tsv]')
    parser.add_argument('--outfile', '-o', type=str, dest='outfile', required=True, help='All nodes annotated.')

    args = parser.parse_args()
    print(args)

    annotations = parse_annotations(args.annotations_file)
    graph = parse_graph(args.graph_file)
    print(len(graph))

    new_annotations = propagate(graph, annotations)
    output_annotations(args.outfile, annotations, new_annotations)
