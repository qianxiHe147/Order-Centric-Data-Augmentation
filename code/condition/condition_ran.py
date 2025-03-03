import json
import random
import argparse
import os

def process_instruction(instruction: str) -> str:
    """
    处理 instruction 字段，打乱中间部分的语句顺序，并保持开头和结尾不变。
    
    Args:
        instruction (str): 原始 instruction 字符串
    
    Returns:
        str: 处理后的 instruction 字符串
    """
    split_point = instruction.find(
        "Please determine whether the conclusion is true, false, or uncertain based on these premises.\n\nPremises:\n"
    )
    if split_point == -1:
        return instruction  
    
    intro = instruction[:split_point + len(
        "Please determine whether the conclusion is true, false, or uncertain based on these premises.\n\nPremises:\n"
    )]
    remaining_text = instruction[split_point + len(
        "Please determine whether the conclusion is true, false, or uncertain based on these premises.\n\nPremises:\n"
    ):]

    parts = remaining_text.split("\n")

    if len(parts) < 2:
        return instruction 
    # 获取需要打乱的部分（除最后两行有关hypothesis的部分）
    body_parts = parts[:-2]
    last_two_parts = parts[-2:]  

    processed_parts = [part.split(". ", 1)[-1] for part in body_parts]
    random.shuffle(processed_parts)
    numbered_parts = [f"{i+1}. {part}" for i, part in enumerate(processed_parts)]
    
    return intro + "\n".join(numbered_parts) + "\n" + "\n".join(last_two_parts)

def process_json(input_file: str, output_file: str):
    """
    处理 JSON 文件，修改 instruction 字段，并输出新的 JSON 文件。
    
    Args:
        input_file (str): 输入 JSON 文件路径
        output_file (str): 输出 JSON 文件路径
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            if "instruction" in item:
                item["instruction"] = process_instruction(item["instruction"])

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Processed file has been saved to: {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    """
    主函数，使用 argparse 解析命令行参数，并执行 JSON 处理。
    """
    parser = argparse.ArgumentParser(description="Process a JSON file to shuffle instruction data.")
    parser.add_argument("input_file", type=str, help="Path to the input JSON file")
    parser.add_argument("output_file", type=str, help="Path to save the processed JSON file")
    args = parser.parse_args()

    process_json(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
