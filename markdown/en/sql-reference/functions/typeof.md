Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# TYPEOF

Returns the type of a value stored in a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) column.

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is) , [SYSTEM$TYPEOF](/sql-reference/functions/system_typeof)

## Syntax

Copy code

```
TYPEOF( <expr> )
```

## Arguments

`expr`
:   The argument can be a column name or a general expression of type VARIANT. If necessary, you can
    [cast](/sql-reference/functions/cast) the `expr` to a VARIANT.

## Returns

Returns a VARCHAR value that contains the data type of the input expression, such as BOOLEAN, DECIMAL, ARRAY,
OBJECT, and so on.

## Usage notes

- The returned string might be DECIMAL even if the input is an exact integer, due to optimizations that change the
  physical storage type of the input.

- This function doesn’t support a [structured type](/sql-reference/data-types-structured) as an input argument.

## Examples

Create and fill the `vartab` table. The INSERT statement uses the [Parse\_Json](parse_json) function to insert
[VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) values in the `v` column of the table.

Copy code

```
CREATE OR REPLACE TABLE vartab (n NUMBER(2), v VARIANT);

INSERT INTO vartab
  SELECT column1 AS n, PARSE_JSON(column2) AS v
    FROM VALUES (1, 'null'),
                (2, null),
                (3, 'true'),
                (4, '-17'),
                (5, '123.12'),
                (6, '1.912e2'),
                (7, '"Om ara pa ca na dhih"  '),
                (8, '[-1, 12, 289, 2188, false,]'),
                (9, '{ "x" : "abc", "y" : false, "z": 10} ')
       AS vals;
```

Query the data. The query uses the [Typeof](typeof) function to show the data types of
the values stored in the VARIANT column.

Copy code

```
SELECT n, v, TYPEOF(v)
  FROM vartab
  ORDER BY n;
```

```
+---+------------------------+------------+
| N | V                      | TYPEOF(V)  |
|---+------------------------+------------|
| 1 | null                   | NULL_VALUE |
| 2 | NULL                   | NULL       |
| 3 | true                   | BOOLEAN    |
| 4 | -17                    | INTEGER    |
| 5 | 123.12                 | DECIMAL    |
| 6 | 1.912000000000000e+02  | DOUBLE     |
| 7 | "Om ara pa ca na dhih" | VARCHAR    |
| 8 | [                      | ARRAY      |
|   |   -1,                  |            |
|   |   12,                  |            |
|   |   289,                 |            |
|   |   2188,                |            |
|   |   false,               |            |
|   |   undefined            |            |
|   | ]                      |            |
| 9 | {                      | OBJECT     |
|   |   "x": "abc",          |            |
|   |   "y": false,          |            |
|   |   "z": 10              |            |
|   | }                      |            |
+---+------------------------+------------+
```

The following example uses the TYPEOF function to determine the data type of a value by
[casting](/sql-reference/functions/cast) the value to a VARIANT.

Create and populate a table:

Copy code

```
CREATE OR REPLACE TABLE typeof_cast(status VARCHAR, time TIMESTAMP);

INSERT INTO typeof_cast VALUES('check in', '2024-01-17 19:00:00.000 -0800');
```

Query the table using the TYPEOF function by casting each value to a VARIANT:

Copy code

```
SELECT status,
       TYPEOF(status::VARIANT) AS "TYPE OF STATUS",
       time,
       TYPEOF(time::VARIANT) AS "TYPE OF TIME"
  FROM typeof_cast;
```

```
+----------+----------------+-------------------------+---------------+
| STATUS   | TYPE OF STATUS | TIME                    | TYPE OF TIME  |
|----------+----------------+-------------------------+---------------|
| check in | VARCHAR        | 2024-01-17 19:00:00.000 | TIMESTAMP_NTZ |
+----------+----------------+-------------------------+---------------+
```
