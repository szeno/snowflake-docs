# September 21, 2026: Cortex AI Function Evaluation for measuring quality (*Public Preview*)

Snowflake Cortex AI Function Evaluation is now available in public preview, enabling customers to measure
the output quality, cost, and token usage of custom AI Functions and Cortex AI calls against labeled
datasets. Using the [AI\_FUNCTION\_EVALUATION](/sql-reference/functions/ai_function_evaluation) experiment
type, customers can establish repeatable baselines and compare prompts, models, or function
implementations using consistent datasets and evaluation criteria. Evaluations can be configured directly
in SQL or through the guided
[Cortex AI Function Studio](/user-guide/snowflake-cortex/ai-function-studio) workflow.

Key use cases include:

- **Establish a measurable quality baseline:** Evaluate an AI function against representative inputs and
  expected outputs before using it in production workflows.
- **Compare prompts, models, and implementations:** Measure different configurations using the same
  dataset version, ground-truth labels, metric, and metric configuration to produce directly comparable
  results.
- **Evaluate different output types:** Use rule-based metrics for classifications and constrained outputs,
  `llm_judge` for open-ended outputs, or a custom metric UDF for task-specific criteria.
- **Measure output consistency:** Repeat an evaluation to understand variation across nondeterministic
  model outputs.
- **Prepare evaluation data with AI Function Studio:** Use an existing labeled dataset, generate labels
  for existing inputs, or create synthetic evaluation examples through a guided workflow.

For more information, see
[Evaluate an AI function](/user-guide/snowflake-cortex/ai-function-studio#label-cortex-ai-function-studio-evaluate).
