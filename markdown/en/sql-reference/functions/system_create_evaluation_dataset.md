Categories:
:   [System functions](/sql-reference/functions-system) (Control)

# SYSTEM$CREATE\_EVALUATION\_DATASET

Creates a Snowflake [dataset](/developer-guide/snowflake-ml/dataset) for [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) from an existing table. The new dataset is registered in the same database and schema as given in the dataset name argument.

Use this function when you want to create an evaluation dataset with SQL (for example, following the [Getting Started with Cortex Agent Evaluations](https://www.snowflake.com/en/developers/guides/getting-started-with-cortex-agent-evaluations/) guide). You can instead create a dataset from a table in Snowsight when you start an evaluation, or define a `dataset` block in your evaluation YAML file. For the table and column requirements for evaluation data, see [Dataset format](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-agent-evaluation-dataset-format).

See also:
:   [EXECUTE\_AI\_EVALUATION](/sql-reference/functions/execute_ai_evaluation) , [GET\_AI\_EVALUATION\_DATA (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_evaluation_data-snowflake-local)

## Syntax

Copy code

```
CALL SYSTEM$CREATE_EVALUATION_DATASET(
  '<agent_dataset_type>' ,
  '<source_table_name>' ,
  '<dataset_name>' ,
  <column_mapping>
);
```

## Arguments

`'agent_dataset_type'`
:   The dataset type for Cortex Agent evaluations. Use the string `Cortex Agent`. This value is case-insensitive.

`'source_table_name'`
:   The fully qualified name of the source table that contains evaluation inputs and ground truth columns (for example, `MY_DB.MY_SCHEMA.MY_EVAL_TABLE`).

`'dataset_name'`
:   The fully qualified name for the dataset Snowflake creates (for example, `MY_DB.MY_SCHEMA.MY_EVAL_DATASET`). The dataset is created in the database and schema you specify.

`column_mapping`
:   A SQL [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that maps evaluation fields to source column names. Include:

    - `query_text`: The name of the column that contains the input query (VARCHAR).
    - `expected_tools`: The name of the VARIANT column that contains the expected behavior (ground truth) JSON for each row.

    Note

    The `SYSTEM$CREATE_EVALUATION_DATASET` column mapping keys differ from the Agent Evaluation YAML specification. In YAML, the dataset `column_mapping` uses the key `ground_truth`. When you call this system function, use `expected_tools` to map your source table’s ground truth VARIANT column.

## Returns

A string message indicating whether the dataset was created successfully.

## Access control requirements

You need [permissions to create a dataset from an input table](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-agent-evaluation-access-control), including `CREATE DATASET ON SCHEMA` for the schema where the dataset is created.

## Examples

The following example creates the dataset `MARKETING_CAMPAIGNS_DB.AGENTS.MARKETING_CAMPAIGN_EVALSET` from the table `MARKETING_CAMPAIGNS_DB.AGENTS.EVALS_TABLE`, using `INPUT_QUERY` as the query column and `GROUND_TRUTH_DATA` as the ground truth column:

Copy code

```
CALL SYSTEM$CREATE_EVALUATION_DATASET(
  'Cortex Agent',
  'MARKETING_CAMPAIGNS_DB.AGENTS.EVALS_TABLE',
  'MARKETING_CAMPAIGNS_DB.AGENTS.MARKETING_CAMPAIGN_EVALSET',
  OBJECT_CONSTRUCT(
    'query_text', 'INPUT_QUERY',
    'expected_tools', 'GROUND_TRUTH_DATA'
  )
);
```

Confirm the dataset exists:

Copy code

```
SHOW DATASETS IN SCHEMA MARKETING_CAMPAIGNS_DB.AGENTS;
```
