# DESCRIBE CORTEX SEARCH SERVICE

Describes the properties of a [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview).

DESCRIBE can be abbreviated to DESC.

## Syntax

Copy code

```
{ DESC | DESCRIBE } CORTEX SEARCH SERVICE <name>;
```

## Parameters

`name`
:   Specifies the identifier for the Cortex Search service.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command output provides the Cortex Search service properties and metadata in the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `name` | TEXT | Name of the service. |
| `database_name` | TEXT | The database in which the service resides. |
| `schema_name` | TEXT | The schema in which the service resides. |
| `target_lag` | TEXT | The maximum amount of time that the service’s content should lag behind updates to the base tables. |
| `warehouse` | TEXT | The warehouse used for service refreshes. |
| `search_column` | TEXT | Name of the search column. |
| `attribute_columns` | TEXT | Comma-separated list of attribute columns in the service. |
| `columns` | TEXT | Comma-separated list of columns in the service. |
| `definition` | TEXT | SQL query used to create the service. |
| `comment` | TEXT | Any comments associated with the service. |
| `service_query_url` | TEXT | URL for querying the service. |
| `source_data_num_rows` | NUMBER | Current number of rows in the materialized source data. |
| `indexing_state` | TEXT | Indexing state of the service; one of SUSPENDED or RUNNING. |
| `indexing_error` | TEXT | Error encountered in the last indexing pipeline, if one exists. |
| `serving_state` | TEXT | Serving state of the Cortex Search Service; one of SUSPENDED or RUNNING. |
| `created_on` | TIMESTAMP\_LTZ | Creation time of the Cortex Search Service. |
| `data_timestamp` | TIMESTAMP\_LTZ | Time at which the source data was checked for changes resulting in the currently serving index. |
| `embedding_model` | TEXT | The vector embedding model used by the service. |
| `primary_key_columns` | TEXT | Comma-separated list of [primary key column](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) names defined on the service. Empty if no primary key is set. |
| `scoring_profile_count` | NUMBER | The number of [named scoring profiles](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-named-scoring-profiles) defined in the service. |
| `full_index_build_interval_days` | NUMBER | The target interval, in days, between full index rebuilds that compact incremental refresh segments. Only applicable to services with [primary keys](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) defined. NULL if not set. |

Expand

Show lessSee more

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

The following example describes the Cortex Search service named `mysvc`:

Copy code

```
DESCRIBE CORTEX SEARCH SERVICE mysvc;
```
