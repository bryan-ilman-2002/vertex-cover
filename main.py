from graph_generator import generate_tree, visualize_tree
import vertex_cover_bnb as vc_bnb
import vertex_cover_dynamic_programming as vc_dp

if __name__ == '__main__':
    graph_file_dir = 'graphs/'
    output_dir = 'vertex_covers/'

    datasets = [
        ('small_dataset.txt', 10_000, 100),
        ('medium_dataset.txt', 100_000, 300),
        ('large_dataset.txt', 1_000_000, 900)
    ]

    for graph_file_txt, node_count, bnb_param in datasets:
        graph_file = graph_file_dir + graph_file_txt
        # generate_tree(node_count, graph_file_dir, graph_file_txt)

        # print(f'dataset size: {node_count}')
        # print(f'dataset size: {bnb_param}')

        vc_bnb.main(graph_file, output_dir + 'bnb_results', bnb_param, 600)
        vc_dp.main(graph_file, output_dir + 'dynamic_programming_results')
