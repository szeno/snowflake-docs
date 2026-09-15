# DESCRIBE WAREHOUSE

Describes a [virtual warehouse](/user-guide/warehouses-overview). For example, shows the date that the warehouse was created.

You can abbreviate DESCRIBE to DESC.

See also:
:   [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) , [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse), [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse) , [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses)

## Syntax

Copy code

```
DESC[RIBE] WAREHOUSE <name>
```

## Parameters

`name`
:   Specifies the [identifier](/sql-reference/identifiers) of the warehouse to describe.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | Warehouse |  |

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

## Examples

This demonstrates the DESCRIBE WAREHOUSE command:

Copy code

```
CREATE WAREHOUSE temporary_warehouse WAREHOUSE_SIZE=XSMALL;
```

Copy code

```
DESCRIBE WAREHOUSE temporary_warehouse;
```

```
+-------------------------------+---------------------+-----------+
| created_on                    | name                | kind      |
|-------------------------------+---------------------+-----------|
| 2022-06-23 00:00:00.000 -0700 | TEMPORARY_WAREHOUSE | WAREHOUSE |
+-------------------------------+---------------------+-----------+
```
