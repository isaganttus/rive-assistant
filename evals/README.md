# Answer-Quality Evals

This directory contains static rubrics for evaluating Rive assistant answers. These are not automated LLM judgments. They define the quality bar that a human reviewer, future scripted evaluator, or model-eval harness can use.

Each case in `evals/cases/` is a JSON object with:

- `id`: Stable case identifier
- `question`: Representative user question
- `tags`: Topic labels
- `expected_reference_files`: Local files the assistant should consult or route through
- `expected_source_paths`: Official Rive docs paths to verify exact details when needed
- `required_concepts`: Concepts a good answer must include
- `red_flags`: Incorrect or risky answer patterns
- `ideal_answer_shape`: Suggested answer structure

Run the validator before opening a PR that changes evals:

```bash
python3 scripts/validate_answer_evals.py
```
