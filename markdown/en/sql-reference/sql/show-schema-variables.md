# SHOW SCHEMA VARIABLES IN SCHEMA

Lists all [schema variables](/sql-reference/schema-variables) in the specified schema for
which you have access privileges.

To list [session variables](/sql-reference/session-variables), use [SHOW VARIABLES](/sql-reference/sql/show-variables).

See also:
:   [VARIABLES view](/sql-reference/info-schema/variables) (Information Schema) , [CREATE VARIABLE](/sql-reference/sql/create-variable) , [ALTER VARIABLE](/sql-reference/sql/alter-variable) , [DROP VARIABLE](/sql-reference/sql/drop-variable) ,
    [DESCRIBE VARIABLE](/sql-reference/sql/desc-variable)

## Syntax

Copy code

```
SHOW SCHEMA VARIABLES [ LIKE '<pattern>' ]
  IN SCHEMA { <schema_name> | <database_name>.<schema_name> }
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN SCHEMA { schema_name | database_name.schema_name }`
:   Specifies the schema whose variables to list. Either a bare schema name (relative to
    the current database) or a fully qualified `database.schema` name can be used.

## Output

The command returns the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| created\_on | TIMESTAMP\_LTZ | Date and time when the variable was created |
| name | VARCHAR | Name of the variable |
| schema\_name | VARCHAR | Schema that the variable belongs to |
| database\_name | VARCHAR | Database that the variable belongs to |
| owner | VARCHAR | Role that owns the variable |
| data\_type | VARCHAR | Declared data type of the variable |
| value | VARCHAR | Current value of the variable, or NULL if no value has been set |
| default\_value | VARCHAR | Default value of the variable, or NULL if no default was declared |
| version | NUMBER | Monotonically increasing version number, incremented each time the variable is set |
| comment | VARCHAR | Comment for the variable |

Expand

Show lessSee more

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

- Only variables for which the current role has been granted `OWNERSHIP`, `READ`, or `WRITE`
  privilege are returned.

## Examples

List all schema variables in the current database’s `myschema` schema:

Copy code

```
SHOW SCHEMA VARIABLES IN SCHEMA myschema;
```

List schema variables matching a pattern:

Copy code

```
SHOW SCHEMA VARIABLES LIKE 'tax%' IN SCHEMA myschema;
```

List schema variables using a fully qualified schema name:

Copy code

```
SHOW SCHEMA VARIABLES IN SCHEMA mydb.myschema;
```
