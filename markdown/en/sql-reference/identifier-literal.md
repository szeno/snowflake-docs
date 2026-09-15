# Literals and variables as identifiers with IDENTIFIER() syntax

In Snowflake SQL statements, in addition to referring to objects by name (see [Identifier requirements](/sql-reference/identifiers-syntax)), you can
also use a string literal, session variable, bind variable, or
[Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables) to refer to an object. For example, you can
use a session variable that is set to the name of a table in the FROM clause of a SELECT statement. To use an object name
specified in a literal or variable, use IDENTIFIER() syntax.

Using IDENTIFIER() to identify database objects is a best practice because it can make
code more reusable and help to prevent [SQL injection](/developer-guide/stored-procedure/stored-procedures-usage#label-sql-injection) risks.

## Syntax

Copy code

```
IDENTIFIER( { string_literal | session_variable | bind_variable | snowflake_scripting_variable } )
```

`string_literal`
:   String identifying the name of the object:

    - The string must either be enclosed by single quotes (`'name'`) or start with a dollar sign (`$name`).
    - The string literal can be a fully-qualified object name (e.g. `'db_name.schema_name.object_name'` or `$db_name.schema_name.object_name`).

`session_variable`
:   A [SQL variable](/sql-reference/session-variables) that has been set for the session.

`bind_variable`
:   A [bind variable](/sql-reference/bind-variables), in the form of `?` or `:variable`, which can be used by clients/programmatic interfaces that support binding (JDBC, ODBC, Python, etc.).

`snowflake_scripting_variable`
:   A [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables) that has been set.

## Usage notes

- You can use literals and variables (session or bind) in some cases when you need to identify an object by name (queries, DML,
  DDL, and so on).
- You can use bind variables for object identifiers and bind variables for values in the same query.
- In a FROM clause, you can use
  `TABLE( { string_literal | session_variable | bind_variable | snowflake_scripting_variable } )` as a synonym for
  `IDENTIFIER( { string_literal | session_variable | bind_variable | snowflake_scripting_variable } )`.
- Although IDENTIFIER() uses the syntax of a function, it isn’t a true function and isn’t returned by commands such as
  SHOW FUNCTIONS.

## Examples

The following examples use the IDENTIFIER() syntax.

### Using the IDENTIFIER() syntax with string literals

These examples show you how to refer to an object when a string literal contains the
object identifier.

Create a database:

Copy code

```
CREATE OR REPLACE DATABASE IDENTIFIER('my_db');
```

```
+--------------------------------------+
| status                               |
|--------------------------------------|
| Database MY_DB successfully created. |
+--------------------------------------+
```

Create a schema:

Copy code

```
CREATE OR REPLACE SCHEMA IDENTIFIER('my_schema');
```

```
+----------------------------------------+
| status                                 |
|----------------------------------------|
| Schema MY_SCHEMA successfully created. |
+----------------------------------------+
```

Create a table using a case-insensitive table name specified in a string that contains the fully-qualified name:

Copy code

```
CREATE OR REPLACE TABLE IDENTIFIER('my_db.my_schema.my_table') (c1 number);
```

```
+--------------------------------------+
| status                               |
|--------------------------------------|
| Table MY_TABLE successfully created. |
+--------------------------------------+
```

Create a table using a case-sensitive table name specified in a double-quoted string:

Copy code

```
CREATE OR REPLACE TABLE IDENTIFIER('"my_table"') (c1 number);
```

```
+--------------------------------------+
| status                               |
|--------------------------------------|
| Table my_table successfully created. |
+--------------------------------------+
```

Show the tables in a schema:

Copy code

```
SHOW TABLES IN SCHEMA IDENTIFIER('my_schema');
```

```
+-------------------------------+----------+---------------+-------------+-------+---------+---------+
| created_on                    | name     | database_name | schema_name | kind  | comment | ...     |
|-------------------------------+----------+---------------+-------------+-------+---------+---------|
| 2024-07-03 08:55:11.992 -0700 | MY_TABLE | MY_DB         | MY_SCHEMA   | TABLE |         | ...     |
| 2024-07-03 08:56:00.604 -0700 | my_table | MY_DB         | MY_SCHEMA   | TABLE |         | ...     |
+-------------------------------+----------+---------------+-------------+-------+---------+---------+
```

### Using the IDENTIFIER() syntax with session variables

These examples show you how to use a [session variable](/sql-reference/session-variables) that has
a table name or schema name.

Set a session variable for a schema name:

Copy code

```
SET schema_name = 'my_db.my_schema';
```

Set a session variable for a table name:

Copy code

```
SET table_name = 'my_table';
```

Specify the schema for the current session:

Copy code

```
USE SCHEMA IDENTIFIER($schema_name);
```

Insert values into a table:

Copy code

```
INSERT INTO IDENTIFIER($table_name) VALUES (1), (2), (3);
```

Query a table:

Copy code

```
SELECT * FROM IDENTIFIER($table_name) ORDER BY 1;
```

```
+----+
| C1 |
|----|
|  1 |
|  2 |
|  3 |
+----+
```

This example shows how to use a session variable that has a function name.

1. Create the function `speed_of_light`:

   > Copy code
   >
   > ```
   > CREATE FUNCTION speed_of_light()
   > RETURNS INTEGER
   > AS
   >   $$
   >   299792458
   >   $$;
   > ```
2. Call the function by name:

   > Copy code
   >
   > ```
   > SELECT speed_of_light();
   > ```
   >
   > ```
   > +------------------+
   > | SPEED_OF_LIGHT() |
   > |------------------|
   > |        299792458 |
   > +------------------+
   > ```
3. Call the function by using the IDENTIFIER() syntax:

   > Copy code
   >
   > ```
   > SET my_function_name = 'speed_of_light';
   > ```
   >
   > Copy code
   >
   > ```
   > SELECT IDENTIFIER($my_function_name)();
   > ```
   >
   > ```
   > +---------------------------------+
   > | IDENTIFIER($MY_FUNCTION_NAME)() |
   > |---------------------------------|
   > |                       299792458 |
   > +---------------------------------+
   > ```

### Using the IDENTIFIER() syntax with bind variables

These examples show you how to use [bind variables](/sql-reference/bind-variables) to identify objects.

This example shows you how to bind a function name in JDBC. The function is named `speed_of_light`.

Copy code

```
String sql_command;

// Create a Statement object to use later.
System.out.println("Create JDBC statement.");
Statement statement = connection.createStatement();
System.out.println("Create function.");
sql_command = "CREATE FUNCTION speed_of_light() RETURNS INTEGER AS $$ 299792458 $$";
statement.execute(sql_command);

System.out.println("Create prepared statement.");
sql_command = "SELECT IDENTIFIER(?)()";
PreparedStatement ps = connection.prepareStatement(sql_command);
// Bind
ps.setString(1, "speed_of_light");
ResultSet rs = ps.executeQuery();
if (rs.next()) {
  System.out.println("Speed of light (m/s) = " + rs.getInt(1));
}

//
```

The following examples show a variety of SQL statements that can use binding, and a variety of database objects
that can be bound (including schema names and table names):

Copy code

```
USE SCHEMA IDENTIFIER(?);

CREATE OR REPLACE TABLE IDENTIFIER(?) (c1 NUMBER);

INSERT INTO IDENTIFIER(?) values (?), (?), (?);

SELECT t2.c1
  FROM IDENTIFIER(?) AS t1,
       IDENTIFIER(?) AS t2
  WHERE t1.c1 = t2.c1 AND t1.c1 > (?);

DROP TABLE IDENTIFIER(?);
```

### Using the IDENTIFIER() syntax with Snowflake Scripting variables

This example shows how to use a [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables)
for a table name in a SELECT statement:

Copy code

```
BEGIN
  LET res RESULTSET := (SELECT COUNT(*) AS COUNT FROM IDENTIFIER(:table_name));
  ...
```
