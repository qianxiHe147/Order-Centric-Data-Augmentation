from vllm import LLM, SamplingParams
import os
import json
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

model_path = "model_path"
model = LLM(model_path, dtype='bfloat16', gpu_memory_utilization=0.8)
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model_path)


def process_question(item):
    question = item['instruction']
    return question

def generate_messages(data, batch_size):
    all_batches = []

    num_batches = (len(data) + batch_size - 1) // batch_size

    for i in range(num_batches):
        start_index = i * batch_size
        end_index = min(start_index + batch_size, len(data))
        data_batch = data[start_index:end_index]

        batch_messages = []

        for item in data_batch:
            instruction = process_question(item)
            message = [
                {"role": "user", "content": instruction}
            ]
            batch_messages.append(message)

        all_batches.append(batch_messages)

    return all_batches, num_batches


input_file = "data/test/Sequential/logicnli.json"
# input_file = "data/test/Shuffled/logicnli.json"

with open(input_file, 'r') as file:
    data = json.load(file)

batch_size = 500
messages_all, num = generate_messages(data, batch_size)


all_outputs = []
for i in range(num):
    formatted_prompt =  tokenizer.apply_chat_template(messages_all[i], tokenize=False, add_generation_prompt=True)
    sampling_params = SamplingParams(temperature=0, max_tokens=2048, stop="<|eot_id|>")
    batch_output = model.generate(formatted_prompt, sampling_params)
    for output in batch_output:
        generated_text = output.outputs[0].text
    for output in batch_output:
        generated_text = output.outputs[0].text
        result = {
            'model_output': generated_text
        }
        all_outputs.append(result)

output_file = 'results/Sequential/logicnli.json'
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(all_outputs, file, ensure_ascii=False, indent=4)