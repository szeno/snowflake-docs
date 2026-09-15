# DROP DYNAMIC TABLE

Removes a [dynamic table](/user-guide/dynamic-tables/overview) from the current/specified schema.

See also:
:   [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table), [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table), [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table),
    [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables), [UNDROP DYNAMIC TABLE](/sql-reference/sql/undrop-dynamic-table)

## Syntax

Copy code

```
DROP DYNAMIC TABLE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the dynamic table to drop. If the identifier contains spaces, special characters, or mixed-case
    characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive
    (e.g. `"My Object"`).

    If the table identifier is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the table in the current schema for the session.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | The dynamic table that you want to drop. |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To drop a dynamic table, you must be using a role that has OWNERSHIP privilege on that dynamic table.
- You can also drop a dynamic table using the [DROP TABLE](/sql-reference/sql/drop-table) command.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop `my_dynamic_table`:

> Copy code
>
> ```
> DROP DYNAMIC TABLE my_dynamic_table;
> ```
>
> Copy code
>
> ```
> DROP TABLE my_dynamic_table;
> ```
