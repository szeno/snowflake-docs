# USE DATABASE

Specifies the active/current database for the session:

- If a database is not specified for a session, any objects referenced in queries and other SQL statements executed in
  the session must be fully qualified with the database and schema, also known as the *namespace*, for the object
  (in the form of `db_name.schema_name.object_name`). For more information about fully-qualified object names,
  see [Object name resolution](/sql-reference/name-resolution).
- If a database is specified for a session but the schema is not specified for a session, any objects referenced in queries
  and other SQL statements executed in the session must be qualified with the schema for the object (in the form of
  `schema_name.object_name`).
- If the database and schema are specified for a user session, unqualified object names are allowed in SQL statements and
  queries.

See also:
:   [CREATE DATABASE](/sql-reference/sql/create-database) , [ALTER DATABASE](/sql-reference/sql/alter-database) , [DROP DATABASE](/sql-reference/sql/drop-database) , [SHOW DATABASES](/sql-reference/sql/show-databases)

## Syntax

Copy code

```
USE [ DATABASE ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the database to use for the session. If the identifier contains spaces or special characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- The DATABASE keyword does not need to be specified.
- USE DATABASE automatically specifies PUBLIC as the current schema, unless the PUBLIC schema doesn’t exist (e.g. it has been dropped).
  To specify a different schema for a session, use the [USE SCHEMA](/sql-reference/sql/use-schema) command.

## Examples

The following example specifies the database to use for subsequent SQL commands:

Copy code

```
USE DATABASE mydb;
```

The following example shows how commands that refer to objects using unqualified names
produce different output after a USE command to switch databases. The schemas, tables,
table data, and so on can differ from one database to another.

When the [SHOW SCHEMAS](/sql-reference/sql/show-schemas) command is run in the context of `database_one`,
it produces output reflecting the objects in that database:

Copy code

```
USE DATABASE database_one;
SHOW SCHEMAS ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";

+-------------------------------+--------------------+
| 2025-07-11 14:34:24.386 -0700 | PUBLIC             |
| 2025-07-11 14:42:23.509 -0700 | TEST_SCHEMA        |
| 2025-07-11 14:42:29.158 -0700 | STAGING_SCHEMA     |
| 2025-07-11 14:45:43.124 -0700 | INFORMATION_SCHEMA |
+-------------------------------+--------------------+
```

After a USE command switches to the `database_two` database, the SHOW SCHEMAS
command produces output reflecting a different set of objects:

Copy code

```
USE DATABASE database_two;
SHOW SCHEMAS ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";
```

```
+-------------------------------+--------------------+
| 2025-07-11 14:34:31.496 -0700 | PUBLIC             |
| 2025-07-11 14:43:04.394 -0700 | PRODUCTION_SCHEMA  |
| 2025-07-11 14:44:23.006 -0700 | DASHBOARDS_SCHEMA  |
| 2025-07-11 14:45:54.372 -0700 | INFORMATION_SCHEMA |
+-------------------------------+--------------------+
```

The following example changes from one database to another, then back to
the original database. The name of the original database is stored in a
variable. Run the following commands:

Copy code

```
SELECT CURRENT_DATABASE();
SET original_database = (SELECT CURRENT_DATABASE());
USE DATABASE database_two;
SELECT CURRENT_DATABASE();
USE DATABASE IDENTIFIER($original_database);
SELECT CURRENT_DATABASE();
```

The output for these commands shows how the current database value changes:

```
>SELECT CURRENT_DATABASE();
+--------------+
| DATABASE_ONE |
+--------------+

>SET original_database = (SELECT CURRENT_DATABASE());

>USE DATABASE database_two;
>SELECT CURRENT_DATABASE();
+--------------+
| DATABASE_TWO |
+--------------+

>USE DATABASE IDENTIFIER($original_database);
>SELECT CURRENT_DATABASE();
+--------------+
| DATABASE_ONE |
+--------------+
```
