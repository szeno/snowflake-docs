Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$GET\_TAG

Returns the tag value associated with the specified Snowflake object or column. Returns NULL if a tag is not set on the specified
Snowflake object or column.

## Syntax

Copy code

```
SYSTEM$GET_TAG( '<tag_name>' , '<obj_name>' , '<obj_domain>' )
```

## Arguments

`'tag_name'`
:   The name of the tag as a string.

    The name is the `key` in the key-value pair of the tag. For example, in the tag `cost_center = 'sales'`, `cost_center` is the
    key-name of the tag. For this argument, use `'cost_center'`.

`'obj_name'`
:   The name of the object as a string.

    For example, if a table name is `my_table`, use `'my_table'` as the name of the object.

    To specify a column, use the format `<table_name>.<column_name>`. For example, `my_table.revenue`.

    To identify a logical table, dimension, fact, or metric in a [semantic view](/user-guide/views-semantic/overview):

    - Use an exclamation mark (`!`) between the name of the semantic view and the name of the logical table.
    - Use a period (`.`) between the name of the logical table and the name of the dimension, fact, or metric.
    - For a [derived metric](/user-guide/views-semantic/sql#label-semantic-views-create-derived-metrics), use a period (`.`) between the name of the semantic
      view and the name of the derived metric.

    For example:

    - `'my_semantic_view!my_logical_table'`
    - `'my_semantic_view!my_logical_table.my_dimension'`
    - `'my_semantic_view!my_logical_table.my_fact'`
    - `'my_semantic_view!my_logical_table.my_metric'`
    - `'my_semantic_view.my_derived_metric'`

    For more information, see [Object identifiers](/sql-reference/identifiers).

`'object_domain'`
:   Domain of the reference object, such as a table or view, if the tag association is on the object. For columns, the domain is `COLUMN`
    if the tag association is on a column.

    Use one of the following values:

    > - `'ACCOUNT'`
    > - `'ALERT'`
    > - `'BACKUP POLICY'`
    > - `'BACKUP SET'`
    > - `'COLUMN'`
    > - `'COMPUTE POOL'`
    > - `'CORTEX AGENT'`
    > - `'CORTEX SEARCH SERVICE'`
    > - `'DATABASE'`
    > - `'DATABASE ROLE'`
    > - `'FAILOVER GROUP'`
    > - `'FUNCTION'`
    > - `'INTEGRATION'`
    > - `'INSTANCE'`
    > - `'NETWORK POLICY'`
    > - `'PROCEDURE'`
    > - `'REPLICATION GROUP'`
    > - `'ROLE'`
    > - `'SCHEMA'`
    > - `'SHARE'`
    > - `'SNAPSHOT POLICY'` (deprecated; prefer `'BACKUP POLICY'`)
    > - `'SNAPSHOT SET'` (deprecated; prefer `'BACKUP SET'`)
    > - `'SNOWFLAKE INTELLIGENCE'`
    > - `'STAGE'`
    > - `'STREAM'`
    > - `'TABLE'`: Use this for all table-like objects such as views, materialized views, and external tables.
    > - `'TASK'`
    > - `'USER'`
    > - `'WAREHOUSE'`

## Usage notes

- Using this function requires:

  - The privileges to run a [DESCRIBE <object>](/sql-reference/sql/desc) operation on the specified object name.
  - USAGE on the database and schema in which the tag exists.

    For more information, see [Tag Privilege & DDL Summary](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
  - IMPORTED PRIVILEGES on the shared SNOWFLAKE database if you specify a [system classification tag](/user-guide/classify-intro#label-classify-classification-tags).
- If the tag is a [multi-value tag](/user-guide/object-tagging/multi-value-tags) and more than one value is assigned, this function
  returns an error. Use [SYSTEM$TAG\_VALUE\_CONTAINS](/sql-reference/functions/system_tag_value_contains) to test for a specific value.

## Examples

Returns `NULL` if a tag is not associated to the specified object:

> Copy code
>
> ```
> select system$get_tag('cost_center', 'my_table', 'table');
>
> +-----------------------------------------------------+
> | SYSTEM$GET_TAG('COST_CENTER', 'MY_TABLE', 'TABLE')  |
> +-----------------------------------------------------+
> | NULL                                                |
> +-----------------------------------------------------+
> ```

Returns the tag value for the specified table. The tag value is the string component of the `key = 'value'` pair in the tag:

> Copy code
>
> ```
> select system$get_tag('cost_center', 'my_table', 'table');
>
> -----------------------------------------------------+
> | SYSTEM$GET_TAG('COST_CENTER', 'MY_TABLE', 'TABLE') |
> +----------------------------------------------------+
> | sales                                              |
> +----------------------------------------------------+
> ```

Returns the tag value for the specified column:

> Copy code
>
> ```
> select system$get_tag('fiscal_quarter', 'my_table.revenue', 'column');
>
> +----------------------------------------------------------------+
> | SYSTEM$GET_TAG('FISCAL_QUARTER', 'MY_TABLE.REVENUE', 'COLUMN') |
> +----------------------------------------------------------------+
> | Q1                                                             |
> +----------------------------------------------------------------+
> ```
