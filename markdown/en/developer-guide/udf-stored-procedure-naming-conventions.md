# Naming and overloading procedures and UDFs

When you create or call stored procedures or user-defined functions (UDF), you’ll need to be aware of the naming conventions that
Snowflake allows and enforces for them.

You can also overload stored procedures and UDFs, providing different signatures for a given procedure or function.

Note

The length of a user-defined function’s name – the combined length of its name, return type, and the names of all of its
parameters – must not exceed 10,000 bytes. Attempting to create a function whose name exceeds this limit will result in the following
error message:

```
Function name (including parameter and return type) too long.
```

## Choosing a name for a procedure or UDF

Names for procedures and UDFs must conform to the rules for [Object identifiers](/sql-reference/identifiers).

Note

Snowflake does not allow creating functions with the same name as any of the system-defined functions.

## Calling a procedure or UDF

When you create a stored procedure or UDF, you create it in a specified database and schema. Procedures and UDFs have a
fully-qualified name defined by their namespace in the form of `db.schema.procedure_or_function_name`.

The following statement uses the fully-qualified name to call a stored procedure:

Copy code

```
CALL mydatabase.myschema.myprocedure();
```

When called without their fully-qualified name, procedures and UDFs are
[resolved according to the database and schema in use for the session](/sql-reference/name-resolution). If
[you specified a search path](/sql-reference/name-resolution#label-object-name-resolution-search-path), that search path is used to
[determine the function or procedure to call](#label-procedure-function-name-search-path).

In contrast, many of the built-in, system-defined functions provided by Snowflake have no namespace. As a result, you can call
them from anywhere.

## Overloading procedures and functions

Snowflake supports [overloading procedures and functions](https://en.wikipedia.org/wiki/Function_overloading). In a given
schema, you can define multiple procedures or functions that have the same name but different signatures. The signatures must
differ by the number of arguments, the types of the arguments, or both.

For example, for UDFs:

Copy code

```
CREATE OR REPLACE FUNCTION myudf (number_argument NUMBER) ...
```

Copy code

```
CREATE OR REPLACE FUNCTION myudf (varchar_argument VARCHAR) ...
```

Copy code

```
CREATE OR REPLACE FUNCTION myudf (number_argument NUMBER, varchar_argument VARCHAR) ...
```

For stored procedures:

Copy code

```
CREATE OR REPLACE PROCEDURE myproc (number_argument NUMBER) ...
```

Copy code

```
CREATE OR REPLACE PROCEDURE myproc (varchar_argument VARCHAR) ...
```

Copy code

```
CREATE OR REPLACE PROCEDURE myproc (number_argument NUMBER, varchar_argument VARCHAR) ...
```

If multiple signatures use the same number of arguments but have different types of arguments, you can use different names for
the arguments to indicate which signature to use when you call the function or procedure.

Copy code

```
CREATE OR REPLACE FUNCTION echo_input (numeric_input NUMBER)
  RETURNS NUMBER
  AS 'numeric_input';
```

Copy code

```
CREATE OR REPLACE FUNCTION echo_input (varchar_input VARCHAR)
  RETURNS VARCHAR
  AS 'varchar_input';
```

Copy code

```
SELECT echo_input(numeric_input => 10);
```

Copy code

```
SELECT echo_input(varchar_input => 'hello world');
```

Note

For commands other than those that call the function or procedure (e.g. executing [DESCRIBE FUNCTION](/sql-reference/sql/desc-function),
[DROP PROCEDURE](/sql-reference/sql/drop-procedure), [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege), etc.), you must use the data types of the
arguments to identify the signature to use.

### Calling overloaded procedures and functions

As is the case with calling any other [procedure](/developer-guide/stored-procedure/stored-procedures-calling) or
[function](/developer-guide/udf/udf-calling-sql), you can specify the arguments by name or by position.

Copy code

```
SELECT myudf(text_input => 'hello world');
```

Copy code

```
SELECT myudf('hello world');
```

If you omit the argument names or if you use the same argument name for arguments of different types, Snowflake uses the number of
arguments and the types of the arguments to determine the signature to use. In these cases,
[automatic type conversion (coercion)](/sql-reference/data-type-conversion#label-when-coercion-occurs) can affect the signature that is selected. For details,
refer to [Caveat about relying on the argument data type to identify the signature to call](#label-procedure-function-name-overloading-caveat).

### Caveat about relying on the argument data type to identify the signature to call

If you are relying on the data type of the argument (rather than the argument name) to identify the signature of the function or
procedure to call, note that the combination of automatic type conversion and overloading makes it easy for minor user errors to
cause unexpected results.

Consider the following examples, which create two SQL UDFs named `add5`:

Copy code

```
CREATE OR REPLACE FUNCTION add5 (n NUMBER)
  RETURNS NUMBER
  AS 'n + 5';

CREATE OR REPLACE FUNCTION add5 (s VARCHAR)
  RETURNS VARCHAR
  AS
  $$
    s || '5'
  $$;
```

If you call `add5` and specify a numeric argument without the argument name, then the first implementation is called. If you
specify a string-typed argument instead, the second implementation called.

If the argument is neither a number nor a string, then the implementation depends on
[Snowflake’s implicit type conversion rules](/sql-reference/data-type-conversion#label-when-coercion-occurs).
For example, a date-typed argument is converted to a string because conversion from DATE to NUMBER is not supported. As a result,
the string implementation is called.

For example:

Copy code

```
SELECT add5(1);
```

```
+---------+
| ADD5(1) |
|---------|
|       6 |
+---------+
```

Copy code

```
SELECT add5('1');
```

```
+-----------+
| ADD5('1') |
|-----------|
| 15        |
+-----------+
```

Copy code

```
SELECT add5('hello');
```

```
+---------------+
| ADD5('HELLO') |
|---------------|
| hello5        |
+---------------+
```

Copy code

```
SELECT add5(TO_DATE('2014-01-01'));
```

```
+-----------------------------+
| ADD5(TO_DATE('2014-01-01')) |
|-----------------------------|
| 2014-01-015                 |
+-----------------------------+
```

To avoid potential confusion, assign different argument names for different signatures, and use the argument names when calling
the function.

In the example above, the two signatures use different argument names (`n` for the NUMBER argument and `s` for the VARCHAR
argument). You can specify which signature to use by specifying the argument name:

Copy code

```
SELECT add5(n => 1);
```

Copy code

```
SELECT add5(s => '1');
```

## How the search path determines which function or procedure to call

If you [specified a search path](/sql-reference/name-resolution#label-object-name-resolution-search-path), then each schema appearing in the search path
is searched for a matching function, in the order that the schema appears in the search path. For each searched schema, Snowflake
attempts to find a matching function, using implicit type conversions if necessary. If no match is found in a schema, then the
next schema is considered. Consider again the `add5` functions, if they were defined in different schemas:

Copy code

```
USE SCHEMA s1;
CREATE OR REPLACE FUNCTION add5 ( n number)
  RETURNS number
  AS 'n + 5';
```

Copy code

```
USE SCHEMA s2;
CREATE OR REPLACE FUNCTION add5 ( s string)
  RETURNS string
  AS 's || ''5''';
```

The choice of which function to use for a numeric or string argument would depend on the search path:

Copy code

```
USE SCHEMA s3;
ALTER SESSION SET SEARCH_PATH='s1,s2';

SELECT add5(5);
```

```
+---------+
| ADD5(5) |
+---------+
| 10      |
+---------+
```

Copy code

```
ALTER SESSION SET SEARCH_PATH='s2,s1';

SELECT add5(5);

+---------+
| ADD5(5) |
*---------+
| 55      |
+---------+
```

With the search path set to search schema `s2` first, the function in `s2` is used, even though it requires that an
implicit type conversion is applied to the argument.
