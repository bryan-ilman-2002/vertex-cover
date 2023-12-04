import argparse
import os
import time
import tracemalloc


def parse_graph_file(graph_file):
    with open(graph_file) as file:
        num_vertices = int(file.readline().split()[2])
        adjacency_list = [[] for _ in range(num_vertices + 1)]
        for index, line in enumerate(file):
            vertex = index + 1
            neighbors = [int(neighbor.replace(',', '')) for neighbor in line.split()[2:] if neighbor != '-']
            for neighbor in neighbors:
                adjacency_list[vertex].append(neighbor)

    return adjacency_list


def depth_first_search(graph, min_vertex_cover, vertex, root):
    # Melakukan DFS pada graf
    for neighbor in graph[vertex]:
        if neighbor != root:
            depth_first_search(graph, min_vertex_cover, neighbor, vertex)

    # Menghitung ukuran minimum vertex cover
    for neighbor in graph[vertex]:
        if neighbor != root:
            min_vertex_cover[vertex][0] += min_vertex_cover[neighbor][1]
            min_vertex_cover[vertex][1] += min(min_vertex_cover[neighbor])


def get_minimum_vertex_cover_size(graph, num_vertices):
    # Inisialisasi array untuk menyimpan ukuran minimum vertex cover
    min_vertex_cover = [[0, 1] for _ in range(num_vertices + 1)]

    # Menghitung ukuran minimum vertex cover dengan DFS
    depth_first_search(graph, min_vertex_cover, 1, -1)

    return min(min_vertex_cover[1])


def main(graph_file, output_dir):
    adjacency_list = parse_graph_file(graph_file)

    # Start tracing memory allocations
    tracemalloc.start()

    # Record the start time
    start_time = time.time()

    minimum_vertex_cover_size = get_minimum_vertex_cover_size(adjacency_list, len(adjacency_list) - 1)

    # Record the end time
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time

    # Stop tracing memory allocations
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f'minimum vertex cover size: {minimum_vertex_cover_size}')
    print(f'dynamic programming execution time: {execution_time} seconds')
    print(f'peak memory usage was {peak / 10**6}MB\n')

    filename = os.path.splitext(os.path.basename(graph_file))[0]
    with open(os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_vertex_cover.txt'), 'w') as file:
        file.write(f'minimum vertex cover size: {minimum_vertex_cover_size}\n')
        file.write(f'execution time: {execution_time} seconds\n')
        file.write(f'peak memory usage was {peak / 10**6}MB\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input parser for BnB')
    parser.add_argument('-inst', action='store', type=str, help='input graph file')

    args = parser.parse_args()
    graph_file_inst = args.inst if args.inst is not None else 'graphs/medium_dataset.txt'
    output_dir_inst = 'vertex_covers/dynamic_programming_results/'

    main(graph_file_inst, output_dir_inst)
