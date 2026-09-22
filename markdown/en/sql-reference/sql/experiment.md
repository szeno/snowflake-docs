# EXPERIMENT (CREATE / EXECUTE / SHOW / DROP)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An experiment is a schema-level Snowflake object that packages an AI workload — either an evaluation or an
optimization — and records its results as a set of runs. You create an experiment with a specification, execute
it (asynchronously, on serverless compute), then read its runs, metrics, and parameters with `SHOW` commands.

The experiment is the delivery mechanism for AI evaluation and optimization. This page is the command
reference for the object itself:

- [CREATE EXPERIMENT](#label-experiment-create) — define an experiment + its spec.
- [EXECUTE EXPERIMENT](#label-experiment-execute) — run it (async).
- [SHOW RUNS](#label-experiment-show-runs) / [SHOW RUN METRICS](#label-experiment-show-run-metrics-parameters) /
  [SHOW RUN PARAMETERS](#label-experiment-show-run-metrics-parameters) — read results.
- [DESCRIBE](#label-experiment-describe) / [SHOW EXPERIMENTS](#label-experiment-show) /
  [ALTER](#label-experiment-alter-abort) / [DROP](#label-experiment-drop) — manage experiments.

For the contents of the specification (what fields go inside `FROM SPECIFICATION`), see
[Evaluate an AI function](/sql-reference/functions/ai_function_evaluation) and
[Optimize an AI function](/sql-reference/functions/ai_function_optimization) — the spec differs by type.

## CREATE EXPERIMENT

Creates an experiment object. For evaluation and optimization, attach a specification with `FROM SPECIFICATION`.

### Syntax

Copy code

```
CREATE [ OR REPLACE ] EXPERIMENT [ IF NOT EXISTS ] <name>
  [ TYPE = '<experiment_type>' ]
  [ FROM SPECIFICATION $$ <specification> $$ ]
```

### Arguments

**Required:**

`name`
:   The experiment identifier; may be fully qualified (`db.schema.name`).

**Optional:**

`TYPE = 'experiment_type'`
:   The experiment type. Accepted values (case-insensitive):

    | Type | Purpose | Specification |
    | --- | --- | --- |
    | `AI_FUNCTION_EVALUATION` | Measure an AI call against labeled data. | [Evaluate](/sql-reference/functions/ai_function_evaluation) |
    | `AI_FUNCTION_OPTIMIZATION` | Improve an AI function automatically. | [Optimize](/sql-reference/functions/ai_function_optimization) |

    Expand

    Show lessSee more

    If `TYPE` is omitted, a generic (untyped) experiment is created; it holds runs but cannot be executed with
    `EXECUTE EXPERIMENT`.

`FROM SPECIFICATION $$ ... $$`
:   The YAML specification for the experiment, quoted with `$$...$$` (or a normal string literal). The spec is
    validated at create time against the schema for the resolved `TYPE`; unknown or misspelled keys are rejected.

`OR REPLACE`
:   Replace an existing experiment of the same name.

`IF NOT EXISTS`
:   No error if the experiment already exists.

To be executable, an experiment must have both an eval/opt `TYPE` and a non-blank specification.

## EXECUTE EXPERIMENT

Runs a previously-created experiment. The work is scheduled asynchronously on serverless compute and its
results are recorded as [runs](#label-experiment-show-runs).

### Syntax

Copy code

```
EXECUTE EXPERIMENT <name>
```

### Behavior

- **Asynchronous.** `EXECUTE EXPERIMENT` schedules the work as a serverless task and returns a status message
  immediately — it does not block or return run data. Poll `SHOW RUNS` (see
  [Reading results](#label-experiment-show-runs)) until the runs reach a terminal status. Spin-up is typically
  a few minutes.
- **No options.** The statement takes only the experiment name — no arguments, `USING`, or `WITH` clause, and
  no explicit `ASYNC` keyword (async is implicit).
- **One execution per experiment.** Re-executing a completed experiment is rejected
  (`EXPERIMENT_ALREADY_EXECUTED`); re-executing while a run is in flight is a no-op success. To re-run, create
  a new experiment (or `CREATE OR REPLACE`).
- **Time limit.** A run is limited to 20 hours of execution; a run that exceeds this is terminated. Most jobs
  finish well within this limit.
- **Preconditions** (each raises a user-visible error if unmet): the experiment exists, has an eval/opt
  `TYPE`, has a non-blank spec, and the caller holds the required Cortex role (see
  [Access control](#label-experiment-access-control)).

### Cancel a running experiment

Copy code

```
ALTER EXPERIMENT <name> ABORT;
```

## Reading results

An executed experiment records its work as runs. Run naming depends on type:

- **Evaluation** → `EVAL_1`, `EVAL_2`, … (one per `num_eval_runs`).
- **Optimization** → `SEED` (baseline) + `ITER_1`, `ITER_2`, … (candidates).

### SHOW RUNS

Copy code

```
SHOW RUNS [ LIKE '<pattern>' ] IN EXPERIMENT <name>
  [ LIMIT <n> [ FROM '<run_name>' ] ]
```

Lists the runs. The lifecycle status is inside the metadata JSON column
(`{"status":"FINISHED"|"FAILED"|"RUNNING", ...}`), not a separate top-level column. `RUNNING` means the
experiment is still working; optimization runs stay `RUNNING` until the whole search finishes and then commit
in a batch.

### SHOW RUN METRICS / SHOW RUN PARAMETERS

Copy code

```
SHOW RUN METRICS    [ LIKE '<pattern>' ] IN EXPERIMENT <name>
  [ RUN <run_name> ] [ LIMIT <n> ]

SHOW RUN PARAMETERS [ LIKE '<pattern>' ] IN EXPERIMENT <name>
  [ RUN <run_name> ] [ LIMIT <n> ]
```

- `IN EXPERIMENT <name>` — required.
- `RUN <run_name>` — optional; scope to one run. The run name may be unquoted (`RUN SEED`) or quoted
  (`RUN 'SEED'`). Omit `RUN` to list across all runs.

Metrics are numeric — for evaluation runs, `score`; for optimization runs, `val_score`, `test_score`,
`cost_compared_to_seed`, and `is_frontier`. Parameters are string-valued (for example `model`,
`function_name`, `function_impl`, `run_type`, `parent_candidate`, `rows_evaluated`). See the
[Evaluate](/sql-reference/functions/ai_function_evaluation) and
[Optimize](/sql-reference/functions/ai_function_optimization) pages for the fields each type reports.

## Managing experiments

### DESCRIBE EXPERIMENT

Copy code

```
{ DESCRIBE | DESC } EXPERIMENT <name>
```

Returns the experiment’s metadata: `created_on`, `name`, `database_name`, `schema_name`, `owner`, and (when
enabled) `type` and `spec`.

### SHOW EXPERIMENTS

Copy code

```
SHOW EXPERIMENTS [ LIKE '<pattern>' ]
  [ IN { ACCOUNT | DATABASE [ <db> ] | SCHEMA [ <schema> ] } ]
```

### DROP EXPERIMENT

Copy code

```
DROP EXPERIMENT [ IF EXISTS ] <name>
```

Dropping an experiment removes its runs. Do not drop an experiment while `EXECUTE EXPERIMENT` is in flight
unless you intend to abandon the run — use `ALTER EXPERIMENT <name> ABORT` to cancel first.

## Usage notes

- **Async lifecycle.** Because `EXECUTE EXPERIMENT` returns before the work is done, always poll `SHOW RUNS`
  and check the `metadata.status`. A newly executed experiment shows runs transitioning `RUNNING` → `FINISHED`
  (or `FAILED`).
- **Keep objects alive during a run.** The function, dataset, and experiment referenced by a running
  experiment must exist for the duration; dropping them mid-run fails the run.
- **`CREATE OR REPLACE` to iterate.** Since an experiment executes only once, the normal loop is:
  `CREATE OR REPLACE EXPERIMENT ...` with an adjusted spec, then `EXECUTE EXPERIMENT` again.
- **Datasets must be versioned `SNOWFLAKE.ML.DATASET` objects** in both eval and opt specs — plain
  tables/views are not accepted.
- **Dataset size.** A dataset of about 50–200 rows is recommended; the maximum is 1,000 rows (applies to both
  eval and opt specs).

## Billing

`EXECUTE EXPERIMENT` runs on serverless compute, metered under the `SERVERLESS_EXPERIMENTS` service type at
the standard serverless compute-credit rate. The AI inference the experiment performs (`AI_COMPLETE` and
related calls) is metered separately as Cortex AI usage (tokens). Usage is visible in:

- `SNOWFLAKE.ACCOUNT_USAGE.SERVERLESS_EXPERIMENT_HISTORY` — per-experiment credits and times, including the
  experiment name, database, and schema.
- `SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY` / `METERING_DAILY_HISTORY` — filter
  `SERVICE_TYPE = 'SERVERLESS_EXPERIMENTS'`.
- The corresponding `ORGANIZATION_USAGE` views for org-wide reporting.

## Access control requirements

| Privilege / role | Object | Needed for |
| --- | --- | --- |
| CREATE EXPERIMENT | Schema | `CREATE EXPERIMENT`. |
| MODIFY (or OWNERSHIP) | Experiment | `EXECUTE EXPERIMENT`, `ALTER EXPERIMENT ... ABORT` (execution creates runs, which requires MODIFY). |
| OWNERSHIP | Experiment | `DROP EXPERIMENT`. |
| USAGE (or any grant) | Experiment | `DESCRIBE`, `SHOW RUNS` / `SHOW RUN METRICS` / `SHOW RUN PARAMETERS`. |
| Database role `SNOWFLAKE.CORTEX_USER` (or `SNOWFLAKE.AI_FUNCTIONS_USER`) | — | `EXECUTE EXPERIMENT`. |
| USAGE | Referenced function/dataset db + schema | Running the workload. |

Expand

Show lessSee more

## Examples

### Create, execute, and read an optimization experiment

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
      text: text_col
    ground_truth: expected_output
optimization:
  models:
    - claude-haiku-4-5
  reflection_model: claude-sonnet-4-5
  budget: ultra-light
$$;

EXECUTE EXPERIMENT my_db.my_schema.redact_opt_exp;

-- Poll until terminal, then read metrics.
SHOW RUNS IN EXPERIMENT my_db.my_schema.redact_opt_exp;
SHOW RUN METRICS IN EXPERIMENT my_db.my_schema.redact_opt_exp RUN SEED;
SHOW RUN METRICS IN EXPERIMENT my_db.my_schema.redact_opt_exp RUN ITER_1;
```

### List and clean up

Copy code

```
SHOW EXPERIMENTS IN SCHEMA my_db.my_schema;
DESCRIBE EXPERIMENT my_db.my_schema.redact_opt_exp;
DROP EXPERIMENT IF EXISTS my_db.my_schema.redact_opt_exp;
```

## Limitations

- **Public preview.** The AI-function evaluation and optimization capabilities (`FROM SPECIFICATION`,
  `EXECUTE EXPERIMENT`, `DESCRIBE EXPERIMENT`) are in public preview and rolling out to accounts.
- **Executable types only.** Only `AI_FUNCTION_EVALUATION` and `AI_FUNCTION_OPTIMIZATION` experiments can be
  executed.
- **Single execution.** An experiment executes once; re-running requires a new (or replaced) experiment.
- **No `UNDROP`.** A dropped experiment cannot be restored; there is no `UNDROP EXPERIMENT`.
- **Async only.** Results are not returned by `EXECUTE EXPERIMENT`; read them via `SHOW RUNS` /
  `SHOW RUN METRICS` / `SHOW RUN PARAMETERS`.
- **Execution time limit.** A run is limited to 20 hours; a longer run is terminated.
- **Dataset size limit.** The referenced dataset can contain at most 1,000 rows (about 50–200 recommended).
