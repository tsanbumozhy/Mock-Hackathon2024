import json
from queue import PriorityQueue

def find_path(graph, start_node, order_quantity, capacity):
    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((0, start_node))
    path = []
    cost = 0
    stock = capacity
    paths_list = []

    while not priority_queue.empty():
        current_cost, current_node = priority_queue.get()

        if current_node in visited:
            continue

        cost += current_cost

        if capacity <= 0:
            # Reset cost and add start_node to the path
            capacity = stock
            path.append(start_node)
            paths_list.append(path.copy())
            path = [start_node]

        visited.add(current_node)
        path.append(current_node)

        if current_node != start_node:
            capacity -= order_quantity[current_node]

        for neighbor, edge_cost in graph[current_node].items():
            if neighbor not in visited:
                priority_queue.put((edge_cost, neighbor))
    
    # Add the last path to paths_list
    paths_list.append(path)

    return paths_list

if __name__ == "__main__":
    with open('Mock-Hackathon2024\Input data\level1a.json') as file:
        data = json.load(file)

    graph = dict()
    order_quantity = dict()
    start = data['vehicles']['v0']['start_point']
    capacity = data['vehicles']['v0']['capacity']

    key = 0

    n_neigh = data['n_neighbourhoods']
    n_rest = data['n_restaurants']

    neighbourhoods = data['neighbourhoods']

    
    distances = dict()

    temp_key = 0
    for distance in data['restaurants'][start]['neighbourhood_distance']:
        distances.update([(f"n{temp_key}", distance)])
        temp_key += 1

    graph.update([(start, distances)])

    for i in range(n_neigh):
        neighbourhood = neighbourhoods[f'n{i}']
        order_quantity.update([(f'n{i}', neighbourhoods[f'n{i}']['order_quantity'])])

        distances = dict()
        temp_key = 0
        distances.update([(start, data['restaurants'][start]['neighbourhood_distance'][key])])
        for distance in neighbourhood['distances']:
            distances.update([(f"n{temp_key}", distance)])
            temp_key += 1

        distances = {k: v for k, v in distances.items() if v != 0}

        graph.update([(f"n{key}", distances)])
        key += 1

    path = find_path(graph, start, order_quantity, capacity)
    print(path)

    result = {"v0": {"path1": path[0], "path2": path[1], "path3": path[2]}}

    output_filename = 'level1_output.json'
    with open(output_filename, 'w') as output_file:
        json.dump(result, output_file, indent=2)

    print(f"Result saved in {output_filename}")
