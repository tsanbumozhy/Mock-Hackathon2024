import json
from queue import PriorityQueue

def find_path(graph, start_node):
    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((0, start_node))
    path = []
    cost = 0

    while not priority_queue.empty():
        current_cost, current_node = priority_queue.get()

        if current_node in visited:
            continue

        cost += current_cost

        path.append(current_node)

        visited.add(current_node)

        for neighbor, cost in graph[current_node].items():
            if neighbor not in visited:
                priority_queue.put((cost, neighbor))
    
    return path


if __name__ == "__main__":
    with open('Input data\level0.json') as file:
        data = json.load(file)

    graph = dict()
    start = data['vehicles']['v0']['start_point']

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

        distances = dict()
        temp_key = 0
        distances.update([(start, data['restaurants'][start]['neighbourhood_distance'][key])])
        for distance in neighbourhood['distances']:
            distances.update([(f"n{temp_key}", distance)])
            temp_key += 1

        distances = {k: v for k, v in distances.items() if v != 0}

        graph.update([(f"n{key}", distances)])
        key += 1


    path = find_path(graph, 'r0')

    result = {"v0": {"path": path}}

    output_filename = 'level0_output.json'
    with open(output_filename, 'w') as output_file:
        json.dump(result, output_file, indent=2)

    print(f"Result saved in {output_filename}")
