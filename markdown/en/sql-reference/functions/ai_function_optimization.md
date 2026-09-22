Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# Optimize an AI function (AI\_FUNCTION\_OPTIMIZATION)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

AI\_FUNCTION\_OPTIMIZATION searches for improved implementations of an AI function using a labeled dataset and a
scoring metric. You specify the AI function to optimize, the dataset used to evaluate candidate outputs, the
metric to optimize, and the models available to the optimizer. Snowflake generates candidate implementations by
modifying the function’s prompt and model configuration, evaluates each candidate against the dataset, and
records its quality and cost.

The optimization produces candidate implementations, including candidates on a quality & cost frontier. The
original AI function is not modified. To use an optimized implementation, create a new AI function from the
selected optimization run.

AI\_FUNCTION\_OPTIMIZATION uses the same evaluation model as
[AI function evaluation](/sql-reference/functions/ai_function_evaluation): candidate implementations are
repeatedly evaluated against the specified dataset and metric.

## Syntax

Optimization runs in two statements: create the experiment with an optimization specification, then execute it.

Copy code

```
CREATE [ OR REPLACE ] EXPERIMENT <experiment_name>
  TYPE = 'AI_FUNCTION_OPTIMIZATION'
  FROM SPECIFICATION $$
    <optimization_specification>
  $$;

EXECUTE EXPERIMENT <experiment_name>;
```

The optimization specification is a YAML document with this shape:

Copy code

```
function:
  function_name: "<db.schema.fn(ARG_TYPES)>"   # one of function_name /
  # function_body: "<sql_expression>"          #   function_body
metrics:
  - name: <metric_name>
    # judge_model: <model>    # llm_judge only
    # custom_udf: <udf>       # custom only (required)
dataset:
  name: <dataset_name>
  version: <dataset_version>
  column_mapping:                      # optional
    argument_mapping:
      <function_arg>: <dataset_column>
    ground_truth: <label_column>
optimization:
  models:
    - <candidate_model>          # one or more
  reflection_model: <model>
  strategy: <quality_first|balanced|cost_first>   # optional
  budget: <auto|ultra-light|light|medium|heavy>   # optional
```

## Arguments

The specification is validated at CREATE EXPERIMENT time. Unknown or misspelled keys are rejected.

### Required

`function`
:   The AI function to optimize. Supply exactly one of:

    - `function_name` — a fully-qualified name with its argument-type signature, for example
      `"my_db.my_schema.redact(VARCHAR)"`. The named function must be created with
      [CREATE AI FUNCTION](/sql-reference/sql/create-ai-function) — a plain SQL UDF is rejected.
    - `function_body` — an inline SQL expression to optimize directly (the same form you would put in an AI
      function body).

`metrics`
:   Exactly one scoring metric — a single mapping or a one-element list. Same metric set as evaluation:

    | Metric | Requires |
    | --- | --- |
    | `exact_match` | — |
    | `fuzzy_match` | — |
    | `contains_match` | — |
    | `redaction_match` | — |
    | `llm_judge` | optional `judge_model` |
    | `custom` | `custom_udf: <udf_name>` (required) |

    Expand

    Show lessSee more

    See [Evaluate an AI function](/sql-reference/functions/ai_function_evaluation) for what each metric scores.

`dataset`
:   The labeled data used to score candidates. Must be a versioned Snowflake dataset (`SNOWFLAKE.ML.DATASET`);
    plain tables/views are not accepted.

    - `name` — fully-qualified dataset name. Required.
    - `version` — dataset version (for example `v1`). Required.

`optimization`
:   How to search. Requires at least:

    - `models` — a list of one or more candidate models to try. Each model is optimized in parallel; the best
      implementations across all models form the reported frontier.
    - `reflection_model` — the model used to generate candidate improvements. Use the most capable supported
      model available, because this model drives the optimization process. For example, use a Claude Opus model
      or a latest-generation GPT model.

### Optional

`dataset.column_mapping`
:   Maps the function’s inputs and label to dataset columns. Needed when the function argument names differ from
    the dataset column names.

    - `argument_mapping` — a mapping of `<function_argument>: <dataset_column>` (keys are the AI function’s
      parameter names, or positional markers `$1`, `$2`, …; values are dataset column names).
    - `ground_truth` — the label column candidates are scored against.

`optimization.strategy`
:   The optimization objective (default `quality_first`):

    | Strategy | Optimizes for |
    | --- | --- |
    | `quality_first` | Maximize the metric score (default). |
    | `balanced` | Trade quality against cost. |
    | `cost_first` | Minimize cost while holding quality. |

    Expand

    Show lessSee more

`optimization.budget`
:   Controls how much search effort Snowflake uses to optimize the function. The budget is applied independently
    to each candidate model. For example, if you specify three candidate models with `light`, each model receives
    its own `light` optimization budget. Higher budgets generally generate and evaluate more candidate
    implementations, which can improve optimization results but also increase runtime and credit consumption.

    Use:

    - `ultra-light` for a very small search. For optimizers that use iterative search, this corresponds to
      approximately 4–6 proposal iterations per candidate model.
    - `light` for most optimization runs. This corresponds to approximately 10–15 proposal iterations per
      candidate model.
    - `medium` for a broader search. This corresponds to approximately 18–27 proposal iterations per candidate
      model.
    - `heavy` for the broadest search. This corresponds to approximately 27–40 proposal iterations per candidate
      model.
    - `auto` to let Snowflake choose the budget. Currently, `auto` resolves to `light`.

## Returns

CREATE EXPERIMENT and EXECUTE EXPERIMENT return status rows. EXECUTE EXPERIMENT runs asynchronously on
serverless compute and returns immediately. The experiment produces a tree of runs:

- A single `SEED` run — the evaluation of the input function as-is (the baseline).
- One or more `ITER_<N>` runs — candidate implementations the optimizer proposed and evaluated. Accepted,
  rejected, and frontier candidates are all recorded (distinguished by run metadata, not by name).

Read the runs and their metrics:

Copy code

```
SHOW RUNS IN EXPERIMENT <experiment_name>;
SHOW RUN METRICS IN EXPERIMENT <experiment_name> RUN SEED;
SHOW RUN METRICS IN EXPERIMENT <experiment_name> RUN ITER_7;
SHOW RUN PARAMETERS IN EXPERIMENT <experiment_name> RUN ITER_7;
```

Key run metrics and parameters:

| Field | Kind | Meaning |
| --- | --- | --- |
| `val_score` | metric | Quality on the validation split (0–1). |
| `test_score` | metric | Quality on the held-out test split (frontier runs only). |
| `cost_compared_to_seed` | metric | Candidate cost relative to `SEED` (<1 cheaper, >1 pricier). |
| `is_frontier` | metric | `1` if on the cross-model quality/cost frontier. |
| `run_type` | param | `seed`, `accepted`, or `rejected`. |
| `model` | param | The candidate’s model. |
| `function_impl` | param | The candidate’s tuned implementation. |
| `parent_candidate` | param | The run this candidate was derived from. |
| `rows_evaluated` | param | Number of validation rows scored. |

Expand

Show lessSee more

A healthy result: `SEED` completes with a baseline `val_score`, and one or more `ITER_<N>` runs reach a higher
score with `is_frontier = 1`.

## Usage notes

- **Pick the winner, then materialize it.** Optimization reports candidates; it does not change your function.
  Promote the run you want into a new AI function with
  [CREATE AI FUNCTION … FROM EXPERIMENT](/sql-reference/sql/create-ai-function) `<exp> RUN <run>`.
- **Read the frontier, not just the top score.** With `strategy: balanced` or `cost_first`, the best choice
  may be a slightly lower-quality candidate that costs much less. `is_frontier` marks the non-dominated set.
- **Read `test_score`, not just `val_score`.** `val_score` can overfit to the validation split; `test_score`
  (on the held-out test split) is the more honest estimate.
- **`llm_judge` default model.** When `judge_model` is omitted, the default judge is `claude-sonnet-4-5`. On
  the optimization path the judge scores each row on a 0–1 semantic-correctness scale.
- **Custom metric UDF contract.** A custom metric calls the UDF named by `custom_udf` once per row as
  `custom_udf(EXPECTED, PREDICTED)` — two VARCHAR arguments (ground truth first, model output second). It
  must return a VARIANT/OBJECT with a numeric `score` in 0–1 (optionally a `feedback` string). Create it as a
  normal scalar UDF, not an AI function.
- **Use a powerful `reflection_model`.** It performs agentic proposal of new candidates, so use a model at
  least as capable as Claude Sonnet (for example `claude-sonnet-4-5`). Smaller or weaker models often fail to
  produce usable candidates.
- **Multiple candidate models compete.** Listing several models in `models` lets optimization compare, for
  example, a cheaper model that reaches the same quality — surfaced via `cost_compared_to_seed`.
- **Use at most 5 candidate models.** Each model in `models` is optimized separately, so more models means a
  slower run. Keep to five or fewer (use fewer for quick iterations).
- **Dataset size.** A labeled dataset of about 50–200 rows is recommended — enough signal to optimize
  reliably without long runtimes; the maximum is 1,000 rows.
- **Start with `ultra-light`.** Confirm the pipeline works end-to-end on a small budget before spending on
  `medium`/`heavy`.
- **Cost.** The experiment runs on serverless compute (metered as `SERVERLESS_EXPERIMENTS`); the many AI
  calls it makes are metered as Cortex inference tokens. Heavier budgets and more models cost more. See
  [Experiments → Billing](/developer-guide/snowflake-ml/experiments).

## Access control requirements

| Privilege / role | Object | Notes |
| --- | --- | --- |
| CREATE EXPERIMENT | Schema | To create the experiment. |
| Database role `SNOWFLAKE.CORTEX_USER` (or `SNOWFLAKE.AI_FUNCTIONS_USER`) | — | Required to `EXECUTE EXPERIMENT`. |
| USAGE | Function + dataset database/schema | To read the function and labeled data. |

Expand

Show lessSee more

## Examples

### Optimize a redaction function (quality first)

Copy code

```
CREATE OR REPLACE EXPERIMENT my_db.my_schema.redact_opt_exp
  TYPE = 'AI_FUNCTION_OPTIMIZATION'
  FROM SPECIFICATION $$
function:
  function_name: "my_db.my_schema.redact(VARCHAR)"
metrics:
  - name: redaction_match
dataset:
  name: my_db.my_schema.redaction_ds
  version: v1
  column_mapping:
    argument_mapping:
      text: text_col          # function arg -> dataset column
    ground_truth: expected_output
optimization:
  models:
    - claude-haiku-4-5
  reflection_model: claude-sonnet-4-5
  strategy: quality_first
  budget: ultra-light
$$;

EXECUTE EXPERIMENT my_db.my_schema.redact_opt_exp;
```

### Compare models for cost (balanced)

Copy code

```
CREATE OR REPLACE EXPERIMENT my_db.my_schema.classify_opt_exp
  TYPE = 'AI_FUNCTION_OPTIMIZATION'
  FROM SPECIFICATION $$
function:
  function_name: "my_db.my_schema.classify_ticket(VARCHAR)"
metrics:
  - name: exact_match
dataset:
  name: my_db.my_schema.tickets_ds
  version: v1
  column_mapping:
    argument_mapping:
      body: ticket_body
    ground_truth: expected_label
optimization:
  models:
    - openai-gpt-5-nano
    - claude-haiku-4-5
  reflection_model: claude-sonnet-4-5
  strategy: balanced
  budget: medium
$$;

EXECUTE EXPERIMENT my_db.my_schema.classify_opt_exp;
```

### Inspect the frontier, then promote the winner

Copy code

```
SHOW RUNS IN EXPERIMENT my_db.my_schema.redact_opt_exp;
SHOW RUN METRICS IN EXPERIMENT my_db.my_schema.redact_opt_exp RUN ITER_7;

CREATE OR REPLACE AI FUNCTION my_db.my_schema.redact_tuned(text VARCHAR)
  RETURNS VARCHAR
  FROM EXPERIMENT my_db.my_schema.redact_opt_exp RUN ITER_7;
```

## Limitations

- **Public preview.** Optimization is in public preview and is rolling out to accounts.
- **Target must be an AI function or an inline body.** `function_name` must reference a
  [CREATE AI FUNCTION](/sql-reference/sql/create-ai-function) object; a plain UDF is rejected.
- **Exactly one AI\_COMPLETE call.** Optimization tunes a single `AI_COMPLETE` call: the function (or
  `function_body`) must call `AI_COMPLETE` exactly once, and every optimized candidate contains exactly one
  `AI_COMPLETE` call. Functions with zero or multiple `AI_COMPLETE` calls are not supported for optimization.
- **Dataset objects only.** The dataset must be a versioned `SNOWFLAKE.ML.DATASET` object.
- **Dataset size limit.** The dataset can contain at most 1,000 rows (about 50–200 recommended).
- **One metric per optimization.**
- **Model allowlist.** Candidate and reflection models must be authorized/priced for optimization in your
  account and served in your region. A rejected model fails the experiment.
- **`mode` / `optimize_mode` / `validation_fraction` are not supported** and are rejected by spec validation.
- **Execution time limit.** An experiment run is limited to 20 hours; a longer run is terminated. Reduce
  runtime with a smaller dataset, fewer candidate models, or a lighter budget.

## Legal

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
