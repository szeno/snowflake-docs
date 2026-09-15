Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# CONCAT , `||`

Concatenates one or more strings, or concatenates one or more binary values.

The `||` operator provides alternative syntax for CONCAT and requires at least two arguments.

See also:
:   [CONCAT\_WS](/sql-reference/functions/concat_ws)

## Syntax

Copy code

```
CONCAT( <expr> [ , <expr> ... ] )

<expr> || <expr> [ || <expr> ... ]
```

## Arguments

`expr`
:   The input expressions must be all strings, or all binary values.

## Returns

The data type of the returned value is the same as the data type of the input values.

If any input value is NULL, the function returns NULL.

## Usage notes

Metadata functions such as [GET\_DDL](/sql-reference/functions/get_ddl) accept only constants as input. Concatenated
input generates an error.

## Collation details

- The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.
- The collation of the result of the function is the highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of the inputs.

## Examples

Concatenate two strings:

Copy code

```
SELECT CONCAT('George Washington ', 'Carver');
```

```
+----------------------------------------+
| CONCAT('GEORGE WASHINGTON ', 'CARVER') |
|----------------------------------------|
| George Washington Carver               |
+----------------------------------------+
```

Concatenate five strings, using [session variables](/sql-reference/session-variables)
for three of them:

Copy code

```
SET var_first_name = 'George';
SET var_middle_name = 'Washington';
SET var_last_name = 'Carver';

SELECT CONCAT($var_first_name, ' ', $var_middle_name, ' ', $var_last_name) AS concat_name;
```

```
+--------------------------+
| CONCAT_NAME              |
|--------------------------|
| George Washington Carver |
+--------------------------+
```

Concatenate two VARCHAR columns. First, create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE concat_function_example (s1 VARCHAR, s2 VARCHAR, s3 VARCHAR);
INSERT INTO concat_function_example (s1, s2, s3) VALUES
  ('co', 'd', 'e'),
  ('Colorado ', 'River ', NULL);
```

Run a query:

Copy code

```
SELECT CONCAT(s1, s2)
  FROM concat_function_example;
```

```
+-----------------+
| CONCAT(S1, S2)  |
|-----------------|
| cod             |
| Colorado River  |
+-----------------+
```

Concatenate more than two strings:

Copy code

```
SELECT CONCAT(s1, s2, s3)
  FROM concat_function_example;
```

```
+--------------------+
| CONCAT(S1, S2, S3) |
|--------------------|
| code               |
| NULL               |
+--------------------+
```

Use the [IFF](/sql-reference/functions/iff) function with the CONCAT function to concatenate strings that are
not NULL:

Copy code

```
SELECT CONCAT(
    IFF(s1 IS NULL, '', s1),
    IFF(s2 IS NULL, '', s2),
    IFF(s3 IS NULL, '', s3)) AS concat_non_null_strings
  FROM concat_function_example;
```

```
+-------------------------+
| CONCAT_NON_NULL_STRINGS |
|-------------------------|
| code                    |
| Colorado River          |
+-------------------------+
```

Use the `||` concatenation operator instead of the function:

Copy code

```
SELECT 'This ' || 'is ' || 'another ' || 'concatenation ' || 'technique.';
```

```
+--------------------------------------------------------------------+
| 'THIS ' || 'IS ' || 'ANOTHER ' || 'CONCATENATION ' || 'TECHNIQUE.' |
|--------------------------------------------------------------------|
| This is another concatenation technique.                           |
+--------------------------------------------------------------------+
```
