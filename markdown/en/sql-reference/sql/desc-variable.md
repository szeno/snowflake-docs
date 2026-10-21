# DESCRIBE VARIABLE

Describes a [schema variable](/sql-reference/schema-variables), including its type, current
value, default, and metadata.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE VARIABLE](/sql-reference/sql/create-variable) , [ALTER VARIABLE](/sql-reference/sql/alter-variable) , [DROP VARIABLE](/sql-reference/sql/drop-variable) , [SHOW SCHEMA VARIABLES IN SCHEMA](/sql-reference/sql/show-schema-variables)

## Syntax

Copy code

```
DESC[RIBE] VARIABLE <name>
```

## Parameters

`name`
:   Specifies the identifier for the variable to describe. The identifier can be qualified with
    the schema name or with both the database and schema names.

## Output

The command returns the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| name | VARCHAR | Name of the variable |
| data\_type | VARCHAR | Declared data type of the variable |
| value | VARCHAR | Current value, or NULL if not set |
| default\_value | VARCHAR | Default value, or NULL if no default was declared |
| version | NUMBER | Current version number; incremented on each SET |
| owner | VARCHAR | Role that owns the variable |
| comment | VARCHAR | Comment for the variable |
| created\_on | TIMESTAMP\_LTZ | Date and time when the variable was created |
| updated\_on | TIMESTAMP\_LTZ | Date and time when the variable was last modified |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP, READ, or WRITE | Variable | Any one of these privileges is sufficient. |

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

Copy code

```
DESCRIBE VARIABLE myschema.tax_rate;
```

Copy code

```
DESC VARIABLE mydb.myschema.api_version;
```
