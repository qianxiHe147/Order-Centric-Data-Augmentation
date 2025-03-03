# Order-Centric-Data-Augmentation
# Order-Centric Processing Pipeline

## Overview

This repository provides a structured pipeline for transforming and processing logical reasoning datasets. The workflow is divided into three major components:

1. **Condition Processing**: Prepares and refines condition-based logical reasoning datasets.
2. **Answer Transformation**: Reorders reasoning steps and restructures responses for diverse logical reasoning.
3. **Testing and Evaluation**: Runs validation tests to ensure data integrity and correctness.

---

## Repository Structure

```
order_centric/
│── condition/          # Preprocess conditions and steps
│── answer/             # Step-wise transformations and logical restructuring
│── test/               # Validation and evaluation scripts
│── data/               # (Not included) Expected input and output datasets
│── README.md           # Documentation
```

---

## 1️⃣ Condition Processing

Located in the `condition/` directory, this part prepares the conditions and logical dependencies for reasoning tasks.

### Files:

- **extract\_conditions.py**: Extracts premise and step dependencies from dataset outputs.
- **generate\_topological\_orders.py**: Computes valid topological orderings for logical steps.
- **split\_steps.py**: Segments complex steps into structured step-by-step reasoning.

### Execution Order:

1. Run `extract_conditions.py` to parse logical dependencies.
2. Run `generate_topological_orders.py` to compute step orderings.
3. Run `split_steps.py` to segment reasoning steps.

---

## 2️⃣ Answer Transformation

Located in the `answer/` directory, this step focuses on restructuring answer sequences for enhanced logical reasoning.

### Files:

- **reorder\_answers.py**: Randomizes step order based on valid dependency graphs.
- **renumber\_steps.py**: Reassigns step numbers after reordering.
- **format\_final\_output.py**: Generates final structured output.

### Execution Order:

1. Run `reorder_answers.py` to reorder logical steps.
2. Run `renumber_steps.py` to adjust step numbering.
3. Run `format_final_output.py` to generate structured responses.

---

## 3️⃣ Testing and Evaluation

Located in the `test/` directory, this step verifies the integrity of transformed datasets.

### Files:

- **validate\_ordering.py**: Ensures logical consistency of reordered steps.
- **compare\_with\_ground\_truth.py**: Compares generated outputs with reference data.

### Execution Order:

1. Run `validate_ordering.py` to check logical step order validity.
2. Run `compare_with_ground_truth.py` to evaluate correctness.

---

## Running the Pipeline

### Example Commands:

```bash
# Step 1: Process conditions
python condition/extract_conditions.py
python condition/generate_topological_orders.py
python condition/split_steps.py

# Step 2: Transform answers
python answer/reorder_answers.py
python answer/renumber_steps.py
python answer/format_final_output.py

# Step 3: Run tests
python test/validate_ordering.py
python test/compare_with_ground_truth.py
```

Ensure that the necessary input datasets are available in the `data/` directory before executing the scripts.

---

## Notes

- The **condition processing** ensures that logical dependencies are well-structured before answer transformation.
- The **answer transformation** creates diverse logical reasoning sequences while maintaining validity.
- The **testing phase** guarantees correctness and robustness of the processed data.

For any issues, refer to the respective script comments or open an issue in the repository. 🚀

