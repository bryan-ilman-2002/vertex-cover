import argparse
import math
import networkx as nx
import os
import time
import tracemalloc


def parse_graph_file(graph_file, constrained_num_nodes):
    with open(graph_file) as file:
        num_nodes = int(file.readline().split()[2])
        num_nodes = constrained_num_nodes if constrained_num_nodes is not None else num_nodes
        adjacency_list = [[] for _ in range(num_nodes + 1)]
        for index, line in enumerate(file):
            node = index + 1
            neighbors = [int(neighbor.replace(',', '')) for neighbor in line.split()[2:]]
            intended_neighbors = [neighbor for neighbor in neighbors if neighbor <= num_nodes]
            for neighbor in intended_neighbors:
                adjacency_list[node].append(neighbor)
            if node == num_nodes:
                break

    return adjacency_list


def create_graph(adjacency_list):
    graph = nx.Graph()
    for index, edges in enumerate(adjacency_list):
        for edge in edges:
            graph.add_edge(index + 1, edge)
    return graph


def find_max_degree(graph):
    degree_list = graph.degree()
    sorted_degree_list = sorted(degree_list, key=lambda x: x[1], reverse=True)
    return sorted_degree_list[0]


def calculate_vertex_cover_size(vertex_cover):
    return sum(state for node, state in vertex_cover)


def branch_and_bound(graph, cutoff_time):
    current_graph = graph.copy()
    node = find_max_degree(current_graph)
    frontier = [(node[0], state, (-1, -1)) for state in [0, 1]]

    upper_bound = graph.number_of_nodes()
    optimal_vertex_cover = []
    current_vertex_cover = []

    start_time = time.time()

    while frontier and time.time() - start_time < cutoff_time:
        node, state, parent = frontier.pop()
        backtrack = False

        if state == 0:
            neighbors = list(current_graph.neighbors(node))
            current_vertex_cover.extend((neighbor, 1) for neighbor in neighbors)
            current_graph.remove_nodes_from(neighbors)
        if state == 1:
            current_graph.remove_node(node)

        current_vertex_cover.append((node, state))
        current_vertex_cover_size = calculate_vertex_cover_size(current_vertex_cover)

        if current_graph.number_of_edges() == 0:
            if current_vertex_cover_size < upper_bound:
                optimal_vertex_cover = current_vertex_cover.copy()
                upper_bound = current_vertex_cover_size
            backtrack = True
        else:
            lower_bound = current_graph.number_of_edges() / find_max_degree(current_graph)[1]
            lower_bound = math.ceil(lower_bound) + calculate_vertex_cover_size(current_vertex_cover)
            if lower_bound < upper_bound:
                next_node = find_max_degree(current_graph)
                frontier.extend((next_node[0], next_state, (node, state)) for next_state in [0, 1])
            else:
                backtrack = True

        if backtrack and frontier:
            next_node_parent = frontier[-1][2]
            if next_node_parent in current_vertex_cover:
                vertex_cover_len_limit = current_vertex_cover.index(next_node_parent) + 1
                while vertex_cover_len_limit < len(current_vertex_cover):
                    restored_node, _ = current_vertex_cover.pop()
                    current_graph.add_node(restored_node)
                    current_vertex_cover_nodes = [node for node, state in current_vertex_cover]
                    for neighbor in graph.neighbors(restored_node):
                        if neighbor in current_graph.nodes() and neighbor not in current_vertex_cover_nodes:
                            current_graph.add_edge(neighbor, restored_node)
            elif next_node_parent == (-1, -1):
                current_vertex_cover.clear()
                current_graph = graph.copy()
            else:
                print('Error in backtracking step')

    if time.time() - start_time > cutoff_time:
        print('cutoff time time reached')

    return optimal_vertex_cover


def main(graph_file, output_dir, constrained_num_nodes, cutoff_time):
    adjacency_list = parse_graph_file(graph_file, constrained_num_nodes)
    graph = create_graph(adjacency_list[1:])

    # Start tracing memory allocations
    tracemalloc.start()

    # Record the start time
    start_time = time.time()

    minimum_vertex_cover = branch_and_bound(graph, cutoff_time)

    # Record the end time
    end_time = time.time()

    # Stop tracing memory allocations
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Calculate the execution time
    execution_time = end_time - start_time

    minimum_vertex_cover = [node for node, state in minimum_vertex_cover if state == 1]
    print(f'minimum vertex cover size: {len(minimum_vertex_cover)}')
    print(f'branch and bound execution time: {execution_time} seconds')
    print(f'peak memory usage was {peak / 10**6}MB\n')

    input_file = os.path.splitext(os.path.basename(graph_file))[0]
    with open(os.path.join(output_dir, f'{os.path.splitext(input_file)[0]}_vertex_cover.txt'), 'w') as file:
        file.write(f'minimum vertex cover size: {len(minimum_vertex_cover)}\n')
        file.write(f'execution time: {execution_time} seconds\n')
        file.write(f'peak memory usage was {peak / 10**6}MB\n')
        file.write(f'vertices: {", ".join(map(str, minimum_vertex_cover))}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input parser for BnB')
    parser.add_argument('-inst', action='store', type=str, help='input graphs graph file')
    parser.add_argument('-size', action='store', default=None, type=int, help='number of nodes')
    parser.add_argument('-time', action='store', default=512, type=int, help='cutoff time running time for algorithm')

    args = parser.parse_args()
    graph_file_inst = args.inst if args.inst is not None else 'graphs/medium_dataset.txt'
    output_dir_inst = 'vertex_covers/bnb_results'
    constrained_num_nodes_inst = args.size
    cutoff_time_inst = args.time

    main(graph_file_inst, output_dir_inst, constrained_num_nodes_inst, cutoff_time_inst)
