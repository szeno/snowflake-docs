# UNDROP DYNAMIC TABLE

Restores the most recent version of a dropped [dynamic table](/user-guide/dynamic-tables/overview).

See also:
:   [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table), [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table), [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table),
    [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables), [DROP DYNAMIC TABLE](/sql-reference/sql/drop-dynamic-table)

## Syntax

Copy code

```
UNDROP DYNAMIC TABLE <name>
```

## Parameters

`name`
:   Specifies the identifier for the dynamic table to restore.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | The dynamic table that you want to undrop. |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To undrop a dynamic table, you must be using a role that has OWNERSHIP privilege
  on that dynamic table.
- If a table with the same name already exists, an error is returned.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Examples

Restore the most recent version of a dropped dynamic table:

Copy code

```
UNDROP DYNAMIC TABLE my_dynamic_table;
```
