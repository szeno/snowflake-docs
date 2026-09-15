# Passing references for objects and queries to stored procedures

In cases in which you call a stored procedure and pass an identifier for a table, view, function, or procedure to a stored
procedure, you might need to:

- Allow the stored procedure to perform SQL actions on the object, even if the stored procedure uses
  [owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights).
- Allow the stored procedure to resolve the fully qualified name of the object, if the identifier is not qualified or is
  partially qualified.

In these cases, you can create and pass in a reference to the object (for example, the table, view, function, or procedure). A
reference is a unique identifier for an object. Within the stored procedure, when you execute SQL actions on a reference
to an object, the actions are performed using the active role or secondary roles of the user who created the reference. In
addition, if the object identifier is not fully qualified, the name of the object is resolved by using the current database and
schema when the reference was created (in other words, the database and schema of the user who created the reference).

Similarly, if you need to pass in a query to a stored procedure and
[use that query in the FROM clause of a SELECT statement](#label-reference-object-query-references), you can create and pass
in a query reference. Within the stored procedure, the query is performed using the active role or secondary roles of the
user who created the query reference. As is the case with references to objects, if the object name in the query is not fully
qualified, the name of the object is resolved by using the database and schema that were in use when the query reference was
created.

This topic explains how to create and use references.

## Background: The problem with passing objects and queries to stored procedures

Suppose that an owner’s rights stored procedure is designed to insert rows into a table specified by an input argument. The
following are examples written in Snowflake Scripting and JavaScript:

Snowflake ScriptingJavaScript

Copy code

```
USE ROLE stored_proc_owner;

CREATE OR REPLACE PROCEDURE insert_row(table_identifier VARCHAR)
RETURNS TABLE()
LANGUAGE SQL
AS
$$
BEGIN
  LET stmt VARCHAR := 'INSERT INTO ' || table_identifier || ' VALUES (10)';
  LET res RESULTSET := (EXECUTE IMMEDIATE stmt);
  RETURN TABLE(res);
END;
$$;
```

Copy code

```
USE ROLE stored_proc_owner;

CREATE OR REPLACE PROCEDURE insert_row(table_identifier VARCHAR)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
AS
$$
  let res = snowflake.execute({
    sqlText: "INSERT INTO IDENTIFIER(?) VALUES (10);",
    binds : [TABLE_IDENTIFIER]
  });
  res.next()
  return res.getColumnValue(1);
$$;
```

Suppose that you need to call this procedure for a table that is owned by a different role:

Copy code

```
USE ROLE table_owner;

CREATE OR REPLACE TABLE table_with_different_owner (x NUMBER) AS SELECT 42;
```

If you call the stored procedure and pass in the name of the table, the stored procedure will fail because the owner of the
stored procedure does not have sufficient privileges to access the table:

Copy code

```
USE ROLE table_owner;

CALL insert_row('table_with_different_owner');
```

```
002003 (42S02): Uncaught exception of type 'STATEMENT_ERROR' on line 4 at position 25 : SQL compilation error:
Table 'TABLE_WITH_DIFFERENT_OWNER' does not exist or not authorized.
```

To enable the stored procedure to perform SQL actions on the table as the caller,
[create a reference](#label-reference-object-creating) to the table and pass in that reference, rather than the table name.

## Creating a reference

To create the reference, call the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function. For example:

Copy code

```
USE ROLE table_owner;

CALL insert_row(SYSTEM$REFERENCE('TABLE', 'table_with_different_owner', 'SESSION', 'INSERT'));
```

The example above passes in the following arguments to the SYSTEM$REFERENCE function:

- `'TABLE'` for the type of the object.
- `'table_with_different_owner'` for the name of the table.
- `'SESSION'` to indicate that the reference should be [scoped to the session](#label-reference-object-scope).
- `'INSERT'` as the
  [privilege needed to perform the action on the object](#label-reference-object-additional-privileges).

Note

If you need to create a reference to an object that you don’t plan to modify (for example, if you are passing in a table that
the stored procedure will query) and you want that reference to be valid for the scope of the call (rather than for the entire
session), you can use the TABLE keyword instead of calling SYSTEM$REFERENCE. For details, see
[Using the TABLE keyword to create a reference to a table, view, or query](#label-reference-object-table-keyword).

## Specifying the scope of the reference

The reference is valid for either the duration of the call in which the reference is passed or the duration of the session. The
context in which the reference is created determines the scope:

- If you create and pass a reference to a stored procedure in a single statement, the reference has the same visibility as a
  variable declared in the outermost block of the stored procedure:

  Copy code

  ```
  CALL select_from_table(SYSTEM$REFERENCE('TABLE', 'my_table');
  ```
- If you create a reference and assign the reference to a [session variable](/sql-reference/session-variables), the
  reference is valid for the duration of the session, even if you unset the session variable:

  Copy code

  ```
  SET tableRef = (SELECT SYSTEM$REFERENCE('TABLE', 'my_table'));

  SELECT * FROM IDENTIFIER($tableRef);
  ```

To specify that the scope of the reference should be the duration of the session, regardless of the context in which the
reference is created, pass `'SESSION'` for the third argument (`session_scope`) of the SYSTEM$REFERENCE function:

Copy code

```
CALL insert_row(SYSTEM$REFERENCE('TABLE', 'table_with_different_owner', 'SESSION', 'INSERT'));
```

## Conferring additional privileges in a reference

By default, a reference confers a subset of privileges, based on the type of the object being referenced. For example, a
reference to a table confers the SELECT privilege on that table for the active role or secondary role of the user who created the
reference. The default privileges depend on the object type. For the list of supported objects, privileges, and default privileges,
see [Supported object types and privileges for references](/sql-reference/references#label-references-supported-objects-and-privileges).

To confer additional privileges, specify those privileges as additional arguments to the
[SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function. For example, to confer the INSERT, UPDATE, and TRUNCATE privileges on
a table:

Copy code

```
SELECT SYSTEM$REFERENCE('TABLE', 'table_with_different_owner', 'SESSION', 'INSERT', 'UPDATE', 'TRUNCATE');
```

Note that you cannot specify OWNERSHIP or ALL as privileges.

After a reference is created, changes to the privileges of the creator of the reference are reflected in the privileges
associated with the reference. For example, if the INSERT privilege is revoked for the creator of a reference, the INSERT
privilege is no longer associated with the reference.

## Using references to tables and views with masking policies

When you use a reference to a table or view that has a masking policy, the reference role is the invoker role (the role returned
by [INVOKER\_ROLE](/sql-reference/functions/invoker_role)), regardless of whether the reference is used in a query, stored procedure, or
user-defined function.

Using a reference does not change the current role (the role returned by [CURRENT\_ROLE](/sql-reference/functions/current_role)).

## Creating references in stored procedures

If you are writing an [owner’s rights stored procedure](/developer-guide/stored-procedure/stored-procedures-rights), do not create a
reference within the body of the stored procedure.

A reference created in an owner’s rights stored procedure uses the role of the owner of the stored procedure. References should
use the role of the user calling the stored procedure. For an owner’s rights stored procedure, the user calling the stored
procedure should create the reference and pass it in to the stored procedure.

If you are writing a caller’s rights stored procedure, you can create a reference within the body of the stored procedure.

## Using query references

If you need to pass in a query that is used in the FROM clause of a SELECT statement in a stored procedure, create and pass in a
query reference.

For example, suppose that a stored procedure passes in a SELECT statement that is intended to be used in the FROM clause of
another SELECT statement. In the example below, the query argument is intended to be a SELECT statement. These examples are in
Snowflake Scripting and JavaScript:

Snowflake ScriptingJavaScript

Copy code

```
USE ROLE stored_proc_owner;

CREATE OR REPLACE PROCEDURE get_num_results(query VARCHAR)
  RETURNS INTEGER
  LANGUAGE SQL
  AS
  DECLARE
    row_count INTEGER DEFAULT 0;
    stmt VARCHAR DEFAULT 'SELECT COUNT(*) FROM (' || query || ')';
    res RESULTSET DEFAULT (EXECUTE IMMEDIATE :stmt);
    cur CURSOR FOR res;
  BEGIN
    OPEN cur;
    FETCH cur INTO row_count;
    RETURN row_count;
  END;
```

Copy code

```
USE ROLE stored_proc_owner;

CREATE OR REPLACE PROCEDURE get_num_results(query VARCHAR)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
AS
$$
  let res = snowflake.execute({
    sqlText: "SELECT COUNT(*) FROM (" + QUERY + ");",
  });
  res.next()
  return res.getColumnValue(1);
$$;
```

The stored procedure uses owner’s rights. If the stored procedure owner does not have the privileges to query the table in the
SELECT statement, the call to the stored procedure fails.

Copy code

```
USE ROLE table_owner;
CREATE OR REPLACE TABLE table_with_different_owner (x NUMBER) AS SELECT 42;

CALL get_num_results('SELECT x FROM table_with_different_owner');
```

```
002003 (42S02): Uncaught exception of type 'STATEMENT_ERROR' on line 4 at position 29 : SQL compilation error:
Object 'TABLE_WITH_DIFFERENT_OWNER' does not exist or not authorized.
```

To enable the stored procedure to execute the query as the caller, create a query reference for the SELECT statement, and pass in
that reference, rather than the SELECT statement.

To create the query reference, you can call the [SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference) function.

Note

If you need to create a query reference that is valid for the scope of the call (rather than for the entire session), you can
use the TABLE keyword instead of calling SYSTEM$QUERY\_REFERENCE. For details, see [Using the TABLE keyword to create a reference to a table, view, or query](#label-reference-object-table-keyword).

If you call the SYSTEM$QUERY\_REFERENCE function, pass in:

- `'SELECT x FROM table_with_different_owner'` as the query.

  Note that if the SELECT statement contains any single quotes or other special characters (e.g. newlines), you must
  [escape those characters with backslashes](/sql-reference/data-types-text#label-single-quoted-string-constants-escape-sequences).
- `true` to indicate that the query reference should be scoped to the session.

For example:

Copy code

```
USE ROLE table_owner;

CALL get_num_results(
  SYSTEM$QUERY_REFERENCE('SELECT x FROM table_with_different_owner', true)
);
```

```
+-----------------+
| GET_NUM_RESULTS |
|-----------------|
|               1 |
+-----------------+
```

Within the stored procedure, you can add a query reference to the FROM clause of a query. For example:

Copy code

```
snowflake.execute({
  sqlText: "SELECT COUNT(*) FROM (" + QUERY + ");"
});
```

For details on this function, refer to [SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference).

For the limitations with creating and using query references, refer to [Current limitations](#label-reference-object-limitations).

## Using the TABLE keyword to create a reference to a table, view, or query

If you need to create reference to a table, view, or secure view that you are not modifying that the stored procedure should
query, and you want the reference to be valid for the scope of the call (rather than for the entire session), use the TABLE
keyword with the following syntax:

Copy code

```
TABLE( [[<database_name>.]<schema_name>.]<object_name> )
```

Copy code

```
TABLE("<object_name_that_requires_double_quotes>")
```

Copy code

```
TABLE(IDENTIFIER('string_literal_for_object_name'))
```

The TABLE keyword provides a simpler syntax for calling the SYSTEM$REFERENCE function for a table or view without having to
specify the argument for the object type. When you use the TABLE keyword, the reference just confers the SELECT privilege, and
the scope of the reference is the call (not the session).

The following examples call the stored procedure `my_procedure` and pass in references to tables and views:

Copy code

```
CALL my_procedure(TABLE(my_table));
```

Copy code

```
CALL my_procedure(TABLE(my_database.my_schema.my_view));
```

Copy code

```
CALL my_procedure(TABLE("My Table Name"));
```

Copy code

```
CALL my_procedure(TABLE(IDENTIFIER('my_view')));
```

Note

You cannot use the TABLE keyword with the name of a function or procedure.

If you want to create a reference to a query, you can use the TABLE keyword as an alternative to calling the
SYSTEM$QUERY\_REFERENCE function, if the reference just needs to be valid for the scope of the call (rather than for the entire
session). To use the TABLE keyword, use the following syntax:

Copy code

```
TABLE(<select_statement>)
```

For example:

Copy code

```
CALL my_procedure(TABLE(SELECT * FROM my_view));
```

Copy code

```
CALL my_procedure(TABLE(WITH c(s) as (SELECT $1 FROM VALUES (1), (2)) SELECT a, count(*) FROM T, C WHERE s = a GROUP BY a));
```

Note the following:

- You cannot use bind variables in the object name or query.
- The reference created by the TABLE keyword is valid for the duration of the call. You cannot specify a different scope for the
  reference.
- The reference has the
  [default privileges conferred for the type of object](/sql-reference/references#label-references-supported-objects-and-privileges).

## Current limitations

Currently, references have the following limitations:

- [GET\_DDL](/sql-reference/functions/get_ddl) and [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) do not support references as input
  arguments.
- You can only create references to tables, views, functions, and procedures.
- In queries that contain references, plan cache and result caching are not used.
- For query references:
  - You can only create query references for SELECT statements that serve as inline views.
  - When you create a query reference, you cannot specify a bind variable or session variable.
  - In your stored procedure, you can only use a query reference in the FROM clause of a SELECT statement.
