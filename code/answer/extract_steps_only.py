import json
import re

def process_steps_only(input_file_path, output_file_path):
    """
    Extracts all steps ("Step X") and the "Final Conclusion" from the 'output' field in a JSON file.

    Args:
        input_file_path (str): Path to the input JSON file containing the 'output' field with step-by-step explanations.
        output_file_path (str): Path to the output JSON file where the extracted steps will be saved.

    Returns:
        None (Generates a processed JSON file at `output_file_path`).
    """
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        output_text = item.get('output', '')

        if "Final Conclusion" in output_text:
            steps_part, final_conclusion = output_text.split("Final Conclusion", 1)
            final_conclusion = "Final Conclusion" + final_conclusion.strip()
        else:
            steps_part = output_text
            final_conclusion = None

        steps = re.split(r'(?=Step \d+:)', steps_part)

        item['output_list'] = [step.strip() for step in steps if step.strip().startswith("Step")]

        if final_conclusion:
            item['output_list'].append(final_conclusion)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Processed file saved at: {output_file_path}")

if __name__ == '__main__':
    input_path = '/data/dell/hqx/FOLIO/code/gpt_condition.json' 
    output_path = '/data/dell/hqx/FOLIO/answer_ran_new/folio_steps_only.json' 
    
    process_steps_only(input_path, output_path)
