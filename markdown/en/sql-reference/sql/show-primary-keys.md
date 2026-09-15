# SHOW PRIMARY KEYS

Lists primary keys for one or more tables. You can specify the following options:

- A single table
- All tables in the current or specified schema
- All tables in the current or specified database
- All tables in the current account

## Syntax

Copy code

```
SHOW [ TERSE ] PRIMARY KEYS
    [ IN { ACCOUNT | DATABASE [ <database_name> ] | SCHEMA [ <schema_name> ] | TABLE | [ TABLE ] <table_name> } ]
```

## Parameters

`TERSE`
:   This clause is accepted in the syntax but has no effect on the output.

`IN { ACCOUNT | DATABASE [ <database_name> ] | SCHEMA [ <schema_name> ] | TABLE | [ TABLE ] <table_name> }`
:   Specifies the scope of the command, which determines whether the command lists records only for the current or specified database,
    schema, table, or account.

    If you specify the keyword `ACCOUNT`, then the command retrieves records for all schemas in all databases
    of the current account.

    If you specify the keyword `DATABASE`, then:

    - If you specify a `db_name`, then the command retrieves records for all schemas of the specified database.
    - If you don’t specify a `db_name`, then:
      - If there is a current database, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and schemas in the account.

    If you specify the keyword `SCHEMA`, then:

    - If you specify a qualified schema name (for example, `my_database.my_schema`), then the command
      retrieves records for the specified database and schema.
    - If you specify an unqualified `schema_name`, then:

      - If there is a current database, then the command retrieves records for the specified schema in the current database.
      - If there is no current database, then the command displays the error
        `SQL compilation error: Object does not exist, or operation cannot be performed`.
    - If you don’t specify a `schema_name`, then:

      - If there is a current database, then:

        - If there is a current schema, then the command retrieves records for the current schema in the current database.
        - If there is no current schema, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    If you specify the keyword `TABLE` without a `table_name`, then:

    - If there is a current database, then:

      - If there is a current schema, then the command retrieves records for the current schema in the current database.
      - If there is no current schema, then the command retrieves records for all schemas in the current database.
    - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    If you specify a `table_name` (with or without the keyword `TABLE`), then:

    - If you specify a fully-qualified `table_name` (e.g. `my_database_name.my_schema_name.my_table_name`),
      then the command retrieves all records for the specified table.
    - If you specify a schema-qualified `table_name` (e.g. `my_schema_name.my_table_name`), then:

      - If a current database exists, then the command retrieves all records for the specified table.
      - If no current database exists, then the command displays an error similar to
        `Cannot perform SHOW object_type. This session does not have a current database...`.
    - If you specify an unqualified `table_name`, then:

      - If a current database and current schema exist, then the command retrieves records for the specified table in the current
        schema of the current database.
      - If no current database exists or no current schema exists, then the command displays an error similar to:
        `SQL compilation error: object does not exist or not authorized.`.

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (that is, the command returns the objects you have privileges to view in the database).
    - No database: `ACCOUNT` is the default (that is, the command returns the objects you have privileges to view in your account).

## Usage notes

- For each single-column primary key, the output contains one row.
- For each multi-column primary key, the output contains one row for each column in the primary key.
- If an account (or database or schema) has a large number of tables, searching the entire account (or table or schema)
  can consume a significant amount of compute resources.

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

Important

For standard tables, Snowflake does not enforce PRIMARY KEY constraints; however, they are enforced on
[hybrid tables](/user-guide/tables-hybrid).

## Output

The command output provides primary key properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the table was created. |
| `database_name` | Database in which the table is stored. |
| `schema_name` | Schema in which the table is stored. |
| `table_name` | Name of the table. |
| `column_name` | Name of the column in the primary key. |
| `key_sequence` | If the primary key is composed of multiple columns, the number in the `key_sequence` column indicates the order of those columns in the primary key. For example, if the primary key is defined as `CONSTRAINT pkey1 PRIMARY KEY (column_x, column_y)`, the `key_sequence` number for `column_x` is 1 and the key\_sequence number for `column_y` is 2. |
| `comment` | The comment (if any) specified for the constraint when the constraint was created. |
| `constraint_name` | The name of the constraint. |

Expand

Show lessSee more

## Examples

Copy code

```
SHOW PRIMARY KEYS;

SHOW PRIMARY KEYS IN ACCOUNT;

SHOW PRIMARY KEYS IN DATABASE;

SHOW PRIMARY KEYS IN DATABASE my_database;

SHOW PRIMARY KEYS IN SCHEMA;

SHOW PRIMARY KEYS IN SCHEMA my_schema;

SHOW PRIMARY KEYS IN SCHEMA my_database.my_schema;

SHOW PRIMARY KEYS IN my_table;

SHOW PRIMARY KEYS IN my_database.my_schema.my_table;
```
