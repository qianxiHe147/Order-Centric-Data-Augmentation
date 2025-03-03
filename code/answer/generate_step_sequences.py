import json
import itertools
from collections import deque

def all_topological_sorts(graph):
    """
    Generate all possible topological orderings of a directed acyclic graph (DAG).

    Args:
        graph (dict): A dictionary representing a DAG where keys are step names and values are lists of dependent steps.

    Returns:
        list: A list of all possible topological sequences.
    """
    indegree = {u: 0 for u in graph} 
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1 

    start_nodes = deque([k for k, v in indegree.items() if v == 0]) 
    result = []

    def visit(path):
        if len(path) == len(graph):
            result.append(list(path)) 
            return

        for v in list(start_nodes):
            start_nodes.remove(v)
            path.append(v)
            for nei in graph[v]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    start_nodes.append(nei)

            visit(path)

            for nei in graph[v]:
                if indegree[nei] == 0:
                    start_nodes.remove(nei)
                indegree[nei] += 1
            path.pop()
            start_nodes.appendleft(v)

    visit([])
    return result

def parse_dependencies(steps_used):
    """
    Parse the "Used" structure and build a dependency graph based only on step dependencies.

    Args:
        steps_used (list): A list of dictionaries where each dictionary contains a step and its dependencies.

    Returns:
        dict: A dictionary representing a directed acyclic graph (DAG) of step dependencies.
    """
    graph = {}
    for step_info in steps_used:
        step_name = list(step_info.keys())[0]
        graph[step_name] = []  

    for step_info in steps_used:
        step_name = list(step_info.keys())[0]
        dependencies = [dep for dep in step_info[step_name] if dep.startswith("Step")]
        for dep in dependencies:
            if dep in graph:  
                graph[dep].append(step_name)
            else:
                graph[dep] = [step_name]  

    return graph

def process_json_file(input_file, output_file):
    """
    Reads a JSON file, parses step dependencies, and generates all possible topological orderings.

    Args:
        input_file (str): Path to the input JSON file containing step dependencies.
        output_file (str): Path to the output JSON file to store the generated sequences.

    Returns:
        None (but generates a processed JSON file at `output_file`).
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for entry in data:
        if 'Premises and steps required' in entry:
            steps_used = entry['Premises and steps required']['Used']
            graph = parse_dependencies(steps_used)
            sequences = all_topological_sorts(graph)
            entry['Reasonable sequence of steps'] = {
                "Number of sequences": len(sequences),
                "Sequences": sequences
            }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Processed file saved at: {output_file}")

if __name__ == "__main__":
    input_file_path = 'data/answer/process/folio_step_dependencies.json'
    output_file_path = 'data/answer/process/folio_step_sequences.json'
    
    process_json_file(input_file_path, output_file_path)
