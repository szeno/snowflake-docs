Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# SEMANTIC\_VIEW\_MATERIALIZATION\_REFRESH\_HISTORY

Preview Feature — Open

Available to all accounts.

Returns the refresh history for a [semantic view materialization](/user-guide/views-semantic/materializations),
including the state, timing, and action taken for each refresh.

See also:
:   [Materializing dimensions and metrics in semantic views](/user-guide/views-semantic/materializations)

## Syntax

Copy code

```
SEMANTIC_VIEW_MATERIALIZATION_REFRESH_HISTORY(
  NAME => '<materialization_name>'
)
```

## Arguments

`NAME => 'materialization_name'`
:   The name of the materialization to return history for.

## Output

The function returns a table with the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `name` | TEXT | Name of the materialization. |
| `schema_name` | TEXT | Name of the schema that contains the semantic view. |
| `database_name` | TEXT | Name of the database that contains the semantic view. |
| `state` | TEXT | State of the refresh:   - `ACTIVE`: The materialization is operational and eligible for query rewrite. - `SUSPENDED`: The materialization is suspended due to a refresh failure. |
| `state_message` | TEXT | Error or status message from the refresh. |
| `refresh_start_time` | TIMESTAMP\_LTZ | Time when the refresh started. |
| `refresh_end_time` | TIMESTAMP\_LTZ | Time when the refresh completed. |
| `warehouse` | TEXT | Warehouse used for the refresh. |
| `refresh_action` | TEXT | Action taken during the refresh: `INITIALIZE`, `REINITIALIZE`, `REFRESH`, or `NO_DATA`. |

Expand

Show lessSee more

## Usage notes

- Call this function using the `TABLE()` keyword in the FROM clause.
- You must use a role that has been granted SELECT on the semantic view.

## Examples

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.SEMANTIC_VIEW_MATERIALIZATION_REFRESH_HISTORY(
  NAME => 'revenue_by_customer'
));
```
