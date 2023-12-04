import collections
import matplotlib.pyplot as plt
import networkx as nx
import os
import random


def generate_tree(node_count, output_dir, output_file):
    # Initialize the tree with each node having no neighbors
    tree = {i: [] for i in range(1, node_count + 1)}

    # Randomly add edges between nodes
    nodes = list(range(2, node_count + 1))
    random.shuffle(nodes)
    for i in nodes:
        # Determine the parent for this node
        parent = random.randint(1, i-1)

        # Add the edge to the tree
        tree[parent].append(i)
        tree[i].append(parent)

    # Normalize the output directory path
    output_dir = os.path.normpath(output_dir)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Write the tree to the output file
    with open(os.path.join(output_dir, output_file), 'w') as f:
        f.write(f"node count: {node_count}\n")
        for node, neighbors in tree.items():
            f.write(f"{node}'s neighbor(s): {', '.join(str(i) for i in neighbors)}\n")


def visualize_tree(input_dir, input_file):
    # Initialize a new directed graph
    graph = nx.DiGraph()

    # Normalize the input directory path
    input_dir = os.path.normpath(input_dir)

    # Read the tree from the input file
    with open(os.path.join(input_dir, input_file), 'r') as f:
        next(f)  # Skip the first line (node count)
        for line in f:
            # Parse the node and its neighbors
            node, neighbors = line.split("'s neighbor(s): ")
            node = int(node)  # Extract the node id
            neighbors = [int(neighbor) for neighbor in neighbors.split(', ') if neighbor != '\n']

            # Add the edges to the graph
            for neighbor in neighbors:
                if neighbor > node:  # Avoid adding edges twice
                    graph.add_edge(node, neighbor)

    # Compute the level of each node using a breadth-first search
    level = {1: 0}
    queue = collections.deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in level:
                level[neighbor] = level[node] + 1
                queue.append(neighbor)

    # Create a layout with each level on its own line and nodes centered
    pos = {node: (i, -level[node]) for i, node in enumerate(graph.nodes)}

    # Draw the graph
    nx.draw(graph, pos, with_labels=True, arrows=False)
    plt.show()
