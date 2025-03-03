import json
import re


def extract_last_answer(model_output):
    pattern = re.compile(r'\b(entailment|not entailment)\b', re.IGNORECASE)
    
    matches = pattern.findall(model_output)
    
    if matches:
        last_match = matches[-1].lower()
        return last_match
    return None 

def process_files(result_file_path, test_file_path, accuracy_file_path):
    with open(result_file_path, 'r', encoding='utf-8') as file:
        cot_ori_data = json.load(file)

    with open(test_file_path, 'r', encoding='utf-8') as file:
        folio_test_data = json.load(file)

    correct_count = 0
    total_count = 0
    new_data = []

    for cot_item, folio_item in zip(cot_ori_data, folio_test_data):
        model_output = cot_item.get('model_output', '')
        folio_output = folio_item.get('output', '').lower()

        extracted_answer = extract_last_answer(model_output)
        correct = False

        if extracted_answer and extracted_answer == folio_output:
            correct = True
            correct_count += 1
        
        total_count += 1
        folio_item['model_output'] = model_output
        folio_item['extracted_answer'] = extracted_answer
        folio_item['correct'] = correct

        new_data.append(folio_item)

    accuracy = correct_count / total_count if total_count > 0 else 0

    output_content = {
        "accuracy": accuracy,
        "total": total_count,
        "correct": correct_count,
        "data": new_data
    }

    with open(accuracy_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(output_content, out_file, ensure_ascii=False, indent=4)

    print(f"Processed {total_count} items. Accuracy: {accuracy:.2%}")

if __name__ == "__main__":
    result_file_path = 'results/Sequential/ruletaker.json'
    test_file_path = "data/test/Sequential/ruletaker.json"
    # test_file_path = "data/test/Shuffled/ruletaker.json"
    accuracy_file_path = 'results/Sequential/ruletaker_acc.json'

    process_files(result_file_path, test_file_path, accuracy_file_path)