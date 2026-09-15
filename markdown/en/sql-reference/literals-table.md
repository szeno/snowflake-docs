# Table literals

Table literals are used to pass the name of a table or a placeholder value (instead of a table name) to a query. Table literals appear in the [FROM](/sql-reference/constructs/from) clause of a SQL
statement and consist of either the table name, or a SQL variable or API bind variable in place of the table name.

Informally, when using `TABLE(...)` to construct a table literal, you can think of `TABLE()` as a
[table function](/sql-reference/functions-table). Syntactically, `TABLE()` looks like a function. Semantically,
`TABLE()` behaves similarly to a table function because it:

- Accepts a scalar value as input.
- Returns a set of 0 or more rows.
- Can be used as a source of rows in a [FROM](/sql-reference/constructs/from) clause.

## Syntax

Copy code

```
TABLE( { <string_literal> | <session_variable> | <bind_variable> } )
```

`string_literal`
:   A string literal that contains an [identifier](/sql-reference/identifiers) for a table:

    - The identifier can be fully-qualified in the form of:

      `db_name.schema_name.table_name`
      `schema_name.table_name`
    - Double quotes are supported for individual object identifiers that are case-sensitive or contain spaces and special characters.
    - The entire identifier string must be enclosed in single quotes or `$$`. For example:

      `'mytable'` or `$$mytable$$`
      `'mydb.myschema.mytable'` or `$$mydb.myschema.mytable$$`
      `'"DB 1"."Schema 1".mytable'` or `$$"DB 1"."Schema 1".mytable$$`

`session_variable`
:   A [SQL variable](/sql-reference/session-variables) that has been set for the session.

`bind_variable`
:   A bind variable, in the standard form of `?` or `:name`, for use with APIs that support bindings (Java, Python, etc.).

## Usage notes

- Table literals are supported in the [FROM](/sql-reference/constructs/from) clause only.
- Where `TABLE()` is supported, it is equivalent to using [IDENTIFIER()](/sql-reference/identifier-literal).
- When a bind variable is used to prepare a statement, table metadata is not available after preparing the statement.

## Examples

Query the table `mytable` using a table literal (note that the following two examples are syntactically equivalent):

> Copy code
>
> ```
> SELECT * FROM TABLE('mytable');
>
> SELECT * FROM TABLE($$mytable$$);
> ```

Query the table `mytable` in the schema `myschema` and the database `mydb` using a table literal (note that the following two examples are syntactically equivalent):

> Copy code
>
> ```
> SELECT * FROM TABLE('mydb."myschema"."mytable"');
>
> SELECT * FROM TABLE($$mydb."myschema"."mytable"$$);
> ```

Set a session variable that references a table name and then query the table using the variable passed as a table literal:

> Copy code
>
> ```
> SET myvar = 'mytable';
>
> SELECT * FROM TABLE($myvar);
> ```

Prepare a statement with a binding that represents a table (note that the following two examples are syntactically equivalent):

> Copy code
>
> ```
> SELECT * FROM TABLE(?);
>
> SELECT * FROM TABLE(:binding);
> ```
