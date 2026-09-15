# DESCRIBE ONLINE FEATURE TABLE

Describes the columns in an [online feature table](/sql-reference/sql/create-online-feature-table).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE ONLINE FEATURE TABLE](/sql-reference/sql/create-online-feature-table) , [ALTER ONLINE FEATURE TABLE](/sql-reference/sql/alter-online-feature-table), [DROP ONLINE FEATURE TABLE](/sql-reference/sql/drop-online-feature-table) , [SHOW ONLINE FEATURE TABLES](/sql-reference/sql/show-online-feature-tables)

## Syntax

Copy code

```
{ DESC | DESCRIBE } ONLINE FEATURE TABLE <name>
```

## Parameters

`name`
:   Specifies the identifier for the online feature table to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | Online feature table | Role that has the MONITOR privilege on the online feature table. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

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
