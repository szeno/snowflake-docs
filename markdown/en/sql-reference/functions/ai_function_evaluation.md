Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# Evaluate an AI function (AI\_FUNCTION\_EVALUATION)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

AI\_FUNCTION\_EVALUATION measures the output quality of an AI function or Cortex AI call against a labeled
dataset. You specify the expression to evaluate, a dataset containing expected outputs, and a scoring metric.
Snowflake executes the expression for each row, compares the generated output with the expected output, and
reports an aggregate quality score together with cost and token usage.

Use evaluation to compare prompts, models, or function implementations using the same dataset and metric. AI
function optimization uses the same evaluation model to measure candidate implementations.

Evaluation is implemented as an AI\_FUNCTION\_EVALUATION experiment. This page describes the evaluation
specification and workflow. For details about the EXPERIMENT object and related commands, see
[Experiments](/developer-guide/snowflake-ml/experiments).

## Syntax

Evaluation runs in two statements: create the experiment with an evaluation specification, then execute it.

Copy code

```
CREATE [ OR REPLACE ] EXPERIMENT <experiment_name>
  TYPE = 'AI_FUNCTION_EVALUATION'
  FROM SPECIFICATION $$
    <evaluation_specification>
  $$;

EXECUTE EXPERIMENT <experiment_name>;
```

The evaluation specification is a YAML document with this shape:

Copy code

```
query_text: <sql_expression_under_test>
metrics:
  - name: <metric_name>
    # judge_model: <model>   # llm_judge only
    # custom_udf: <udf>      # custom only (required)
dataset:
  name: <dataset_name>
  version: <dataset_version>
  ground_truth: <label_column>
evaluation:                  # optional
  num_eval_runs: <1-20>      # optional; default 1
```

## Arguments

The specification is validated at CREATE EXPERIMENT time. Unknown or misspelled keys are rejected.

### Required

`query_text`
:   The AI call to evaluate, written as a SQL scalar expression that references the dataset’s columns by name. This
    can be a Cortex built-in, for example:

    Copy code

    ```
    query_text: "AI_COMPLETE('claude-sonnet-4-5',
      'Classify the sentiment as POSITIVE, NEGATIVE, or NEUTRAL: ' || review)"
    ```

    or a user-defined AI function invoked inline:

    Copy code

    ```
    query_text: "MY_DB.MY_SCHEMA.CLASSIFY_SENTIMENT(review)"
    ```

    Evaluation does not use the nested `function:` block (that block is optimization-only). The call is named
    directly as `query_text`, and it references dataset columns directly — there is no `argument_mapping`.

`metrics`
:   Exactly one scoring metric — either a single mapping or a one-element list. `name` must be one of:

    | Metric | Scores a row as correct when… |
    | --- | --- |
    | `exact_match` | Output equals the ground-truth label exactly. |
    | `fuzzy_match` | Output approximately matches (normalized string similarity). |
    | `contains_match` | The label is contained in the output (or vice versa). |
    | `redaction_match` | Output matches the expected redaction (redaction/PII tasks). |
    | `llm_judge` | An LLM grades the output against the label. Optional `judge_model` picks the grader. |
    | `custom` | A user UDF scores each row. Requires `custom_udf: <udf_name>`. |

    Expand

    Show lessSee more

    A metric list with more than one entry is rejected — one metric per evaluation.

`dataset`
:   The labeled data. Must be a Snowflake dataset (`SNOWFLAKE.ML.DATASET`); plain tables and views are not
    accepted.

    - `name` — fully-qualified dataset name.
    - `version` — dataset version (for example `v1`). Required.
    - `ground_truth` — the column holding the correct/label value each output is scored against.

### Optional

`evaluation.num_eval_runs`
:   Number of times to repeat the evaluation (integer, 1–20; default 1). Repeat runs let you measure variance
    across identical evaluations (AI outputs are non-deterministic). Each repeat is reported as a separate run
    (`EVAL_1`, `EVAL_2`, …).

## Returns

CREATE EXPERIMENT and EXECUTE EXPERIMENT return status rows. EXECUTE EXPERIMENT runs asynchronously on
serverless compute and returns immediately. Read results once the runs finish:

Copy code

```
SHOW RUNS IN EXPERIMENT <experiment_name>;
SHOW RUN METRICS IN EXPERIMENT <experiment_name> RUN EVAL_1;
SHOW RUN PARAMETERS IN EXPERIMENT <experiment_name> RUN EVAL_1;
```

Each `EVAL_<N>` run reports:

- **Metric:** `score` — the aggregate metric value (0–1).
- **Parameters:** `model`, `function_name`, `rows_evaluated` (rows scored), and `custom_metric_udf` when a
  custom metric is used. The lifecycle status (`FINISHED` / `FAILED` / `RUNNING`) is inside the metadata JSON
  column of `SHOW RUNS`, not a top-level column. See
  [Experiments → Reading results](/developer-guide/snowflake-ml/experiments).

## Usage notes

- **Evaluation is implemented as an AI\_FUNCTION\_EVALUATION experiment.** This page describes the evaluation
  specification and workflow. For details about the EXPERIMENT object and related commands, see
  [Experiments](/developer-guide/snowflake-ml/experiments).
- **Evaluation does not modify your function.** It only measures. To improve a function, use
  [AI\_FUNCTION\_OPTIMIZATION](/sql-reference/functions/ai_function_optimization).
- **`query_text` references dataset columns by name.** The columns referenced in the expression must exist in
  the dataset version; the `ground_truth` column supplies the labels.
- **Dataset size.** A labeled dataset of about 50–200 rows is recommended. The maximum is 1,000 rows.
- **One metric per evaluation.** To compare metrics, run separate evaluations.
- **`num_eval_runs` for stability.** Because model outputs vary, a single run can over- or under-state
  quality. Use `num_eval_runs: 3–5` to see the spread before trusting a number.
- **`llm_judge` default model.** When `judge_model` is omitted, the default judge is `claude-sonnet-4-5`. The
  judge scores each output on a semantic-correctness rubric.
- **Custom metric UDF contract.** A custom metric calls the UDF named by `custom_udf` once per row as
  `custom_udf(EXPECTED, PREDICTED)` — two VARCHAR arguments (ground truth first, model output second). It
  must return a VARIANT/OBJECT with a numeric `score` in 0–1 (optionally a `feedback` string). Create it as a
  normal scalar UDF, not an AI function.
- **Cost.** The experiment runs on serverless compute (metered as `SERVERLESS_EXPERIMENTS`); the underlying
  AI calls are metered as Cortex inference tokens.

## Access control requirements

| Privilege / role | Object | Notes |
| --- | --- | --- |
| CREATE EXPERIMENT | Schema | To create the experiment. |
| Database role `SNOWFLAKE.CORTEX_USER` (or `SNOWFLAKE.AI_FUNCTIONS_USER`) | — | Required to `EXECUTE EXPERIMENT`. |
| USAGE | Dataset’s database + schema | To read the labeled data. |

Expand

Show lessSee more

## Examples

### Evaluate a built-in call with exact match

Copy code

```
CREATE OR REPLACE EXPERIMENT my_db.my_schema.sentiment_eval
  TYPE = 'AI_FUNCTION_EVALUATION'
  FROM SPECIFICATION $$
query_text: "AI_COMPLETE('claude-sonnet-4-5',
  'Reply with exactly one word - POSITIVE, NEGATIVE, or NEUTRAL - '
  || 'for the sentiment of: ' || review)"
metrics:
  - name: exact_match
dataset:
  name: my_db.my_schema.reviews_labeled
  version: v1
  ground_truth: expected_sentiment
$$;

EXECUTE EXPERIMENT my_db.my_schema.sentiment_eval;
```

### Evaluate a user AI function with an LLM judge, repeated 3x

Copy code

```
CREATE OR REPLACE EXPERIMENT my_db.my_schema.summary_eval
  TYPE = 'AI_FUNCTION_EVALUATION'
  FROM SPECIFICATION $$
query_text: "MY_DB.MY_SCHEMA.SUMMARIZE(article)"
metrics:
  - name: llm_judge
    judge_model: claude-sonnet-4-5
dataset:
  name: my_db.my_schema.articles_labeled
  version: v1
  ground_truth: reference_summary
evaluation:
  num_eval_runs: 3
$$;

EXECUTE EXPERIMENT my_db.my_schema.summary_eval;
```

### Score with a custom metric UDF

Create a scalar UDF that returns a score (and optional feedback), then reference it with the `custom` metric:

Copy code

```
CREATE OR REPLACE FUNCTION my_db.my_schema.match_metric(
    EXPECTED VARCHAR, PREDICTED VARCHAR)
  RETURNS VARIANT
  AS $$
    OBJECT_CONSTRUCT(
      'score', IFF(LOWER(EXPECTED) = LOWER(PREDICTED), 1.0, 0.0))
  $$;

CREATE OR REPLACE EXPERIMENT my_db.my_schema.sentiment_custom_eval
  TYPE = 'AI_FUNCTION_EVALUATION'
  FROM SPECIFICATION $$
query_text: "MY_DB.MY_SCHEMA.CLASSIFY_SENTIMENT(review)"
metrics:
  - name: custom
    custom_udf: my_db.my_schema.match_metric
dataset:
  name: my_db.my_schema.reviews_labeled
  version: v1
  ground_truth: expected_sentiment
$$;

EXECUTE EXPERIMENT my_db.my_schema.sentiment_custom_eval;
```

### Read the results

Copy code

```
SHOW RUNS IN EXPERIMENT my_db.my_schema.summary_eval;
SHOW RUN METRICS IN EXPERIMENT my_db.my_schema.summary_eval RUN EVAL_1;
```

## Limitations

- **Dataset size limit.** The dataset can contain at most 1,000 rows (about 50–200 recommended).
- **One metric per evaluation.**
- **`num_eval_runs` range is 1–20.**
- **Model availability.** Models named in `query_text` (and any `judge_model`) must be authorized and served
  in your region.
- **Execution time limit.** An experiment run is limited to 20 hours.

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
