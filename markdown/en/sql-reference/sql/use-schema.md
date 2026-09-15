# USE SCHEMA

Specifies the active/current schema for the session:

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
:   [CREATE SCHEMA](/sql-reference/sql/create-schema) , [ALTER SCHEMA](/sql-reference/sql/alter-schema) , [DROP SCHEMA](/sql-reference/sql/drop-schema) , [SHOW SCHEMAS](/sql-reference/sql/show-schemas)

## Syntax

Copy code

```
USE [ SCHEMA ] [<db_name>.]<name>
```

## Parameters

`[db_name.]name`
:   Specifies the identifier for the schema to use for the session. If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    The SCHEMA keyword is optional if the schema name is fully qualified (in the form of `db_name.schema_name`).

    The database name (`db_name`) is optional if the database is specified in the user session and the SCHEMA keyword
    is included.

## Examples

Use the `myschema` schema with the database specified in the user session:

Copy code

```
USE SCHEMA myschema;
```

Use the `myschema` schema in the `mydb` database:

Copy code

```
USE mydb.myschema;
```

The following example shows how commands that refer to objects using unqualified names
produce different output after a USE command to switch schemas. The tables, table data,
views, user-defined functions, and so on can differ from one schema to another.

When the [SHOW TABLES](/sql-reference/sql/show-tables) command is run in the context of `schema_one`,
it produces output reflecting the objects in that schema:

Copy code

```
USE SCHEMA schema_one;
SHOW TABLES ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";
```

```
+-------------------------------+-----------+
| created_on                    | name      |
|-------------------------------+-----------|
| 2025-07-13 23:48:49.129 -0700 | TABLE_ABC |
| 2025-07-13 23:49:50.329 -0700 | TABLE_DEF |
+-------------------------------+-----------+
```

After a USE command switches to the `schema_two` schema, the SHOW TABLES command
produces output reflecting a different set of objects:

Copy code

```
USE SCHEMA schema_two;
SHOW TABLES ->> SELECT "created_on", "name" FROM $1 ORDER BY "created_on";
```

```
+-------------------------------+-----------+
| created_on                    | name      |
|-------------------------------+-----------|
| 2025-07-13 23:52:06.144 -0700 | TABLE_IJK |
| 2025-07-13 23:53:29.851 -0700 | TABLE_XYZ |
+-------------------------------+-----------+
```

The following example changes from one schema to another, then back to
the original schema. The name of the original schema is stored in a
variable. Run the following commands:

Copy code

```
SELECT CURRENT_SCHEMA();
SET original_schema = (SELECT CURRENT_SCHEMA());
USE SCHEMA schema_two;
SELECT CURRENT_SCHEMA();
USE SCHEMA IDENTIFIER($original_schema);
SELECT CURRENT_SCHEMA();
```

The output for these commands shows how the current schema value changes:

```
>SELECT CURRENT_SCHEMA();
+------------+
| SCHEMA_ONE |
+------------+

>SET original_schema = (SELECT CURRENT_SCHEMA());

>USE SCHEMA schema_two;
>SELECT CURRENT_SCHEMA();
+------------+
| SCHEMA_TWO |
+------------+

>USE SCHEMA IDENTIFIER($original_schema);
>SELECT CURRENT_SCHEMA();
+------------+
| SCHEMA_ONE |
+------------+
```
