import json
import random

def process_file(output_list_path, sequences_path, output_path):
    """
    Reorganizes step sequences in the output_list based on the given sequences of logical steps.

    Args:
        output_list_path (str): Path to the JSON file containing the extracted steps (output_list).
        sequences_path (str): Path to the JSON file containing the generated reasonable step sequences.
        output_path (str): Path to the output JSON file where the reorganized data will be saved.

    Returns:
        None (Generates a processed JSON file at `output_path`).
    """
    with open(output_list_path, 'r', encoding='utf-8') as file_list, open(sequences_path, 'r', encoding='utf-8') as file_sequences:
        output_list_data = json.load(file_list)
        sequences_data = json.load(file_sequences)

    new_data = []

    for list_entry, sequence_entry in zip(output_list_data, sequences_data):
        instruction = list_entry.get('instruction', '')
        original_output_list = list_entry.get('output_list', [])

        sequences = sequence_entry.get('Reasonable sequence of steps', {}).get('Sequences', [])
        num_sequences = sequence_entry.get('Reasonable sequence of steps', {}).get('Number of sequences', 0)

        if not sequences or len(original_output_list) < 2:
            print(f"Skipping entry due to missing sequences or insufficient steps: {instruction[:50]}...")
            continue

        selected_sequences = [sequences[0]]

        if num_sequences > 2:
            valid_sequences = [seq for seq in sequences[1:] if int(seq[-1].split()[1]) == len(seq)]
            selected_sequences += random.sample(valid_sequences, 1) if valid_sequences else random.sample(sequences[1:], 1)
        else:
            selected_sequences = sequences  

        for sequence in selected_sequences:
            modified_output_list = original_output_list.copy()

            steps_text = []
            for step in sequence:
                step_index = int(step.split()[1])
                if step_index < len(modified_output_list):
                    steps_text.append(modified_output_list[step_index])
                else:
                    print(f"Warning: Step {step_index} exceeds available steps ({len(modified_output_list)}). Skipping.")
                    continue

            if len(steps_text) == len(sequence):
                modified_output_list[1:-1] = steps_text 
                new_entry = {
                    "instruction": instruction,
                    "output_list": modified_output_list
                }
                new_data.append(new_entry)
            else:
                print("Warning: Some steps could not be found, skipping this configuration.")

    print(f"Successfully generated {len(new_data)} reorganized entries.")
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)

    print(f"Processed file saved at: {output_path}")

if __name__ == "__main__":
    output_list_path = 'data/answer/process/folio_steps_only.json'
    sequences_path = 'data/answer/process/folio_step_sequences.json'
    output_path = 'data/answer/process/folio_reorganized_steps.json'

    process_file(output_list_path, sequences_path, output_path)
