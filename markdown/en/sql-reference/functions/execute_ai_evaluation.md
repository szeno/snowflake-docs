Categories:
:   [System functions](/sql-reference/functions-system) (Control)

# EXECUTE\_AI\_EVALUATION

Start, retrieve the status of, cancel, or delete a Cortex Agent evaluation run.

For more information on Cortex Agent evaluations, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations).

See also:
:   [SYSTEM$CREATE\_EVALUATION\_DATASET](/sql-reference/functions/system_create_evaluation_dataset) , [GET\_AI\_RECORD\_TRACE (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_record_trace-snowflake-local) , [GET\_AI\_EVALUATION\_DATA (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_evaluation_data-snowflake-local) , [GET\_AI\_OBSERVABILITY\_LOGS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_logs-snowflake-local)

## Syntax

Copy code

```
EXECUTE_AI_EVALUATION( <evaluation_job> , <run_parameters> , <config_file_path> )
```

## Arguments

`evaluation_job`
:   One of the following values:

    > - ‘START’: Starts an evaluation
    > - ‘STATUS’: Retrieves the status of an evaluation
    > - ‘CANCEL’: Cancels an in-progress evaluation run
    > - ‘DELETE’: Deletes an evaluation run

`run_parameters`
:   A SQL [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value that contains the following key:

    > - `run_name`: The name of the run to perform the `evaluation_job` operation on.

`config_file_path`
:   A stage file path pointing to an agent evaluation configuration. This path can’t be a signed URL. For the full configuration YAML specification, see [Agent Evaluation YAML specification](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-cortex-agent-evaluation-yaml-spec).

## Returns

The return value of this function depends on the `evaluation_job`:

> - ‘START’ returns a single string message, indicating whether the SQL execution succeeded or failed.
> - ‘STATUS’ returns a table containing information on the current state of the evaluation run.
> - ‘CANCEL’ returns a single string message, indicating whether the SQL execution succeeded or failed.
> - ‘DELETE’ returns a single string message, indicating whether the SQL execution succeeded or failed.

The table returned by the ‘STATUS’ evaluation job has the following columns:

| Name | Type | Description |
| --- | --- | --- |
| RUN\_NAME | VARCHAR | The name of the evaluation run. |
| AGENT\_NAME | VARCHAR | The (unqualified) name of the agent being evaluated. |
| AGENT\_TYPE | VARCHAR | The type of agent being evaluated. |
| STATUS | VARCHAR | The current status of the evaluation run. |
| STATUS\_DETAILS | ARRAY | An array of error messages that occurred during this run. |

Expand

Show lessSee more

Values in the STATUS column are one of:

**Run status**

| Status | Description |
| --- | --- |
| CREATED | The run has been created but not started. |
| INVOCATION\_IN\_PROGRESS | The run invocation is in the process of generating the output and the traces. |
| INVOCATION\_COMPLETED | The run invocation completed with all outputs and traces created. |
| INVOCATION\_PARTIALLY\_COMPLETED | The run invocation is partially completed due to failures in application invocation and trace generation. |
| COMPUTATION\_IN\_PROGRESS | The metric computation is in progress. |
| COMPLETED | The metric computation is completed with detailed outputs and traces. |
| PARTIALLY\_COMPLETED | The run is partially completed due to failures during the metric computation. |
| CANCELLED | The run has been cancelled. |

Expand

Show lessSee more

## Access control requirements

For the full access control requirements to conduct a Cortex Agent evaluation, see [Cortex Agent evaluations – Access control requirements](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-agent-evaluation-access-control).

## Examples

The following example starts a run called `run-1` using the agent evaluation configuration from `@eval_db.eval_schema.metrics/agent_evaluation_config.yaml`:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'START',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```

The following example queries the status of the evaluation run `run-1` using the agent configuration from `@eval_db.eval_schema.metrics/agent_evaluation_config.yaml`:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'STATUS',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```

The following example cancels the in-progress evaluation run `run-1` using the agent configuration from `@eval_db.eval_schema.metrics/agent_evaluation_config.yaml`:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'CANCEL',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```

The following example deletes the evaluation run `run-1` using the agent configuration from `@eval_db.eval_schema.metrics/agent_evaluation_config.yaml`:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'DELETE',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```
