# Order-Centric-Data-Augmentation

## Overview
This repository contains the official implementation of the paper **"Order Doesn't Matter, But Reasoning Does: Training LLMs with Order-Centric Augmentation"**.[📄 Read the full paper](https://arxiv.org/abs/2502.19907)

We propose an **order-centric data augmentation framework** to enhance logical reasoning in large language models (LLMs) by leveraging the **commutativity** of premises and structured reordering of reasoning steps. Our experiments demonstrate that this approach significantly improves LLMs' ability to generalize across different logical reasoning structures.

## Methodology
We introduce two key augmentations:
- **Condition Order Augmentation**: Randomly shuffling independent premises to teach models the logical equivalence of condition order.
- **Answer Order Augmentation**: Using a **directed acyclic graph (DAG)** to identify valid step reorderings while maintaining logical dependencies.

This framework allows LLMs to develop a more **flexible** and **generalized** reasoning process, overcoming biases from fixed sequential patterns.

## Overview

This repository provides a structured pipeline for transforming and processing logical reasoning datasets. The workflow is divided into three major components:

1. **Condition Processing**: Prepares and refines condition-based logical reasoning datasets.
2. **Answer Transformation**: Reorders reasoning steps and restructures responses for diverse logical reasoning.
3. **Testing and Evaluation**: Runs validation tests to ensure data integrity and correctness.

---


## Code Structure

```
order_centric/
│── code/
│   ├── condition/    # Prepares input conditions
│   │   ├── condition_ran.py
│   │
│   ├── answer/       # Processes and organizes step-by-step reasoning answers
│   │   ├── extract_answer_steps.py
│   │   ├── extract_steps_only.py
│   │   ├── format_random_cot.py
│   │   ├── generate_step_sequences.py
│   │   ├── renumber_steps.py
│   │   ├── reorganize_steps.py
│   │
│   ├── test/         # Evaluates the model performance
│   │   ├── accuracy/       # Accuracy evaluation
│   │   │   ├── folio_acc.py
│   │   │   ├── logicnli_acc.py
│   │   │   ├── ruletaker_acc.py
│   │   │
│   │   ├── inference/      # Inference scripts
│   │   │   ├── folio_vllm.py
│   │   │   ├── logicnli_vllm.py
│   │   │   ├── ruletaker_vllm.py
```

---

## Execution 

### 1️⃣ Condition Order Augmentation (`condition/`)

- Prepares the dataset by modifying input conditions before answer processing.

### 2️⃣ Answer Order Augmentation (`answer/`)

This stage processes answer data, ensuring logical order, formatting, and restructuring.

1. **Extract Steps**:
   - `extract_answer_steps.py`: Extracts step-by-step reasoning paths from the dataset.
   - `extract_steps_only.py`: Isolates only the reasoning steps without additional text.
2. **Generate Logical Sequences**:
   - `generate_step_sequences.py`: Creates different orderings of reasoning steps.
3. **Reorganize and Format**:
   - `reorganize_steps.py`: Reorders steps based on logical dependencies.
   - `renumber_steps.py`: Renumbers steps after reorganization.
   - `format_random_cot.py`: Converts reasoning steps into a structured format for training.

### 3️⃣ Testing (`test/`)

#### **Inference :**

- `folio_vllm.py`: Runs inference on the FOLIO dataset.
- `logicnli_vllm.py`: Runs inference on the LogicNLI dataset.
- `ruletaker_vllm.py`: Runs inference on the RuleTaker dataset.


#### **Accuracy Evaluation :**

- `folio_acc.py`: Evaluates accuracy on the FOLIO dataset.
- `logicnli_acc.py`: Evaluates accuracy on LogicNLI dataset.
- `ruletaker_acc.py`: Evaluates accuracy on RuleTaker dataset.

---

## Notes

- Ensure dependencies (such as Python libraries) are installed before running the scripts.

---
