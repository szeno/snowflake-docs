Categories:
:   [Table functions](/sql-reference/functions-table)

# VALIDATE

Validates the files loaded in a past execution of the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command and returns all the errors encountered during the load, rather than just the first error.

## Syntax

Copy code

```
VALIDATE( [<namespace>.]<table_name> , JOB_ID => { '<query_id>' | '_last' } )
```

## Arguments

`[namespace.]table_name`
:   Specifies the fully-qualified name of the table that was the target of the load.

    Namespace is the database and/or schema in which the table resides, in the form of `database_name.schema_name` or `schema_name`. It is optional if a database and schema
    are currently in use within the user session; otherwise, it is required.

`JOB_ID => query_id | _last`
:   The ID for the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command to be validated:

    - The ID can be obtained from the **Query ID** column in the **Query History** page in Snowsight. The specified query ID must have been for the specified target table.
    - If `_last` is specified instead of `query_id`, the function validates the last load executed during the current session, regardless of the specified target table.

## Usage notes

- The validation returns no results for COPY statements that specify `ON_ERROR = ABORT_STATEMENT` (default value).
- Validation fails if:

  - [SELECT](/sql-reference/sql/select) statements are used to transform data during a [COPY INTO <table>](/sql-reference/sql/copy-into-table) operation.
  - The current user does not have access to `table_name`.
  - The current user is not the user who executed `query_id` and does not have access control privileges on this user.
  - The copy history metadata has expired. For more information, refer to [Load metadata](/user-guide/data-load-considerations-load#label-copy-load-metadata).
- If new files have been added to the stage used by `query_id` since the load was executed, the new files added are ignored during the validation.
- If files have been removed from the stage used by `query_id` since the load was executed, the files removed are reported as missing.

## Examples

Return errors for the last executed COPY command:

> Copy code
>
> ```
> SELECT * FROM TABLE(VALIDATE(t1, JOB_ID => '_last'));
> ```

Return errors by specifying a query ID obtained from the **Query History** page in Snowsight or the **Query History** page in Snowsight:

> Copy code
>
> ```
> SELECT * FROM TABLE(VALIDATE(t1, JOB_ID=>'5415fa1e-59c9-4dda-b652-533de02fdcf1'));
> ```

Same query as above, but save the results to a table for future reference:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE save_copy_errors AS SELECT * FROM TABLE(VALIDATE(t1, JOB_ID=>'5415fa1e-59c9-4dda-b652-533de02fdcf1'));
> ```
