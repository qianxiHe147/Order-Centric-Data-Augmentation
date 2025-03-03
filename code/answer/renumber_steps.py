import json
import re

def renumber_steps(output_list):
    """
    Extracts and renumbers step identifiers (e.g., 'Step 1', 'Step 2') in the output list.

    Args:
        output_list (list): A list of strings containing step descriptions.

    Returns:
        tuple: A mapping of old step numbers to new step numbers and a list of original step numbers.
    """
    step_pattern = re.compile(r'Step (\d+)')
    original_steps = []

    for item in output_list[1:-1]: 
        match = step_pattern.search(item)
        if match:
            original_steps.append(int(match.group(1)))

    step_map = {old: new for new, old in enumerate(original_steps, start=1)}
    return step_map, original_steps


def process_file(input_path, output_path):
    """
    Reads a JSON file, renumbers the steps in 'output_list', and saves the processed data.

    Args:
        input_path (str): Path to the input JSON file.
        output_path (str): Path to save the processed JSON file.

    Returns:
        None (writes the output to a file)
    """
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    step_pattern = re.compile(r'\bStep (\d+)\b')

    for entry in data:
        output_list = entry.get('output_list', [])
        
        step_map, original_steps = renumber_steps(output_list)

        step_positions = []
        for index, text in enumerate(output_list):
            for match in step_pattern.finditer(text):
                step_num = int(match.group(1))
                if step_num in original_steps:
                    step_positions.append((index, match.start(), step_num))

        for idx, pos, original in step_positions:
            if original in step_map:
                new_step_num = step_map[original]
                current_text = output_list[idx]
                output_list[idx] = (
                    current_text[:pos + 5] + str(new_step_num) + current_text[pos + 5 + len(str(original)):]
                )
            else:
                print(f"Warning: Step number {original} not found in mapping.")

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    input_path = 'data/answer/process/folio_reorganized_steps.json'
    output_path = 'data/answer/process/folio_renumbered_steps.json'
    process_file(input_path, output_path)
