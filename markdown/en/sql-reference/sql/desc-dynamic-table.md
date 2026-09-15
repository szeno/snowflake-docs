# DESCRIBE DYNAMIC TABLE

Describes the columns in a [dynamic table](/user-guide/dynamic-tables/overview).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table), [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table), [DROP DYNAMIC TABLE](/sql-reference/sql/drop-dynamic-table), [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables)

## Syntax

Copy code

```
DESC[RIBE] DYNAMIC TABLE <name>
```

## Parameters

`name`
:   Specifies the identifier for the dynamic table to describe. If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| SELECT | The dynamic table that you want to describe. | Some metadata is hidden if you don’t have the MONITOR privilege. For more information, see [Grant MONITOR to view metadata](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-view-metadata). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To DESCRIBE a dynamic table, you must be using a role that has MONITOR privilege on the table.

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

Describe the columns in `my_dynamic_table`:

> Copy code
>
> ```
> DESC DYNAMIC TABLE my_dynamic_table;
> ```
