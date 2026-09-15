# Dynamic tables: Changes to ACCOUNT\_USAGE.TABLES and INFORMATION\_SCHEMA.TABLES

## New column added

The ACCOUNT\_USAGE.TABLES and INFORMATION\_SCHEMA.TABLES views include the following new column:

| Column name | Data type | Description |
| --- | --- | --- |
| `is_dynamic` | Text | Indicates whether the table is a dynamic table. Valid values are YES or NO. |

Expand

Show lessSee more

## Changes to ACCOUNT\_USAGE.TABLES

Beginning with the **8.9** release, the following changes to ACCOUNT\_USAGE.TABLES are enabled:

Before the change:
:   Dynamic tables are not included in this view. For rows that represent dynamic tables, the
    value for the `is_insertable_into` column is `YES`.

    The ACCOUNT\_USAGE.TABLES view doesn’t include the `is_dynamic` column.

After the change:
:   Dynamic tables are included in this view. For rows that represent dynamic tables, the values
    of the `table_type` and `is_insertable_into` columns are `BASE TABLE` and `NO`,
    respectively.

    The ACCOUNT\_USAGE.TABLES view includes the `is_dynamic` column, defined above.

## Changes to INFORMATION\_SCHEMA.TABLES

Beginning with the **8.9** release, the following changes to INFORMATION\_SCHEMA.TABLES are enabled:

Before the change:
:   For rows that represent dynamic tables, the values of the `table_type` and `is_insertable_into`
    columns are `NULL` and `YES`, respectively.

    The INFORMATION\_SCHEMA.TABLES view doesn’t include the `is_dynamic` column.

After the change:
:   For rows that represent dynamic tables, the values of the `table_type` and `is_insertable_into`
    columns are `BASE TABLE` and `NO`, respectively.

    The INFORMATION\_SCHEMA.TABLES view includes the `is_dynamic` column, defined above.
