import json
import re

def extract_conditions_and_steps(output_text):
    """
    Parses the `model_output` field and extracts the dependencies of each step on premises and previous steps.

    Args:
        output_text (str): The content of `model_output`, containing multiple steps and their dependencies.

    Returns:
        dict: 
        {
            "Number of Steps": int,  # The number of parsed steps
            "Used": [                 # Dependencies of each step
                {"Step X": ["Premise Y", "Step Z", ...]},
                ...
            ]
        }
    """
    pattern = r"Step (\d+):.*?Premises and steps required: (.*?)\."
    matches = re.findall(pattern, output_text, re.DOTALL)

    steps_used = []
    for step, conditions in matches:
        # Handle 'and' conjunctions, e.g., "Premise 1 and Premise 2" -> "Premise 1, Premise 2"
        conditions = re.sub(r"\band\b", ",", conditions)
        conditions = re.sub(r"\s*,\s*", ",", conditions)

        # Extract "Premise X" or "Step X" (supports both singular and plural forms)
        cond_steps = re.findall(r"Premises? (\d+(?:,\d+)*),?|Steps? (\d+(?:,\d+)*),?", conditions)

        extracted = []
        for premise_group, step_group in cond_steps:
            if premise_group:
                premises = [f"Premise {x.strip()}" for x in premise_group.split(",")]
                extracted.extend(premises)
            if step_group:
                steps = [f"Step {x.strip()}" for x in step_group.split(",")]
                extracted.extend(steps)

        steps_used.append({f"Step {step}": extracted})

    return {
        "Number of Steps": len(matches),
        "Used": steps_used
    }

def process_json_file(input_file, output_file):
    """
    Reads a JSON file, parses the `model_output` field, and stores the extracted step dependencies.

    Args:
        input_file (str): Path to the input JSON file containing the `model_output` field.
        output_file (str): Path to the output JSON file to store the extracted data.

    Returns:
        None (but generates a processed JSON file at `output_file`)
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for entry in data:
        if 'model_output' in entry:
            conditions_info = extract_conditions_and_steps(entry['model_output'])
            entry['Premises and steps required'] = conditions_info

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Processed file saved at: {output_file}")

if __name__ == "__main__":
    input_file_path = 'data/answer/process/folio_cot.json'
    output_file_path = 'data/answer/process/folio_step_dependencies.json'
    
    process_json_file(input_file_path, output_file_path)
