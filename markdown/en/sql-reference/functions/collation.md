Categories:
:   [String & binary functions](/sql-reference/functions-string)

# COLLATION

Returns the collation specification of the expression.

## Syntax

Copy code

```
COLLATION(<expression>)
```

## Arguments

`expression`
:   The expression for which you want to know the collation specification.
    Typically, this is a column name.

## Returns

Returns a VARCHAR value that contains the collation specification of the expression.

## Examples

This example shows how to get the collation specification of a specified column.

First, create the table and insert data:

Copy code

```
CREATE OR REPLACE TABLE collation1 (v VARCHAR COLLATE 'es');
INSERT INTO collation1 (v) VALUES ('ñ');
```

Second, show the collation of the column:

Copy code

```
SELECT COLLATION(v)
  FROM collation1;
```

```
+--------------+
| COLLATION(V) |
|--------------|
| es           |
+--------------+
```
