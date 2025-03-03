import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def generate_output(output_list):
    """
    Generate a structured output from the given output list.

    Args:
        output_list (list): List of text elements.

    Returns:
        str: Formatted output string.
    """
    if len(output_list) < 2:
        return output_list[0] if output_list else ""

    first_part = f"{output_list[0]}\n{output_list[1]}"
    middle_parts = "\n\n".join(output_list[2:-1])
    last_part = f"\n{output_list[-1]}"

    return first_part + ("\n\n" + middle_parts if middle_parts else "") + last_part


def process_data(data):
    new_data = []
    for item in data:
        new_item = {
            "instruction": item["instruction"],
            "input": "",
            "output": generate_output(item["output_list"])
        }
        new_data.append(new_item)
    return new_data


def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    input_json_path = 'data/answer/process/folio_renumbered_steps.json'
    output_json_path = 'data/answer/process/folio_cot_ran.json'

    data = load_json(input_json_path)
    processed_data = process_data(data)
    save_json(processed_data, output_json_path)

    print(f"Processed data saved to: {output_json_path}")


if __name__ == "__main__":
    main()
