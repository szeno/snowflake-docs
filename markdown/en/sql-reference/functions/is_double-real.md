Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# IS\_DOUBLE , IS\_REAL

Returns TRUE if its [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) argument contains a
[floating-point number, fixed-point number, or integer](/sql-reference/data-types-numeric) value.

These functions are synonymous.

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is) , [IS\_DECIMAL](/sql-reference/functions/is_decimal) , [IS\_INTEGER](/sql-reference/functions/is_integer)

## Syntax

Copy code

```
IS_DOUBLE( <variant_expr> )

IS_REAL( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

Returns a BOOLEAN value or NULL.

- Returns TRUE if the VARIANT value contains a floating-point number, a fixed-point number, or an integer value.
  Otherwise, returns FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Examples

The following examples use the IS\_DOUBLE function.

### Use the IS\_DOUBLE function in a WHERE clause

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

Show the floating-point numbers, fixed-point numbers, and integers in the data by using the
IS\_DOUBLE function in a WHERE clause:

Copy code

```
SELECT * FROM vartab WHERE IS_DOUBLE(v);
```

```
+---+-----------------------+
| N | V                     |
|---+-----------------------|
| 4 | -17                   |
| 5 | 123.12                |
| 6 | 1.912000000000000e+02 |
+---+-----------------------+
```

### Use the IS\_DOUBLE function in a SELECT list

Create and fill the `multiple_types` table. The INSERT statement uses the [To\_Variant](to_variant) function to insert
[VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) values in the columns.

Copy code

```
CREATE OR REPLACE TABLE multiple_types (
  array1 VARIANT,
  array2 VARIANT,
  boolean1 VARIANT,
  varchar1 VARIANT,
  varchar2 VARIANT,
  decimal1 VARIANT,
  double1 VARIANT,
  integer1 VARIANT,
  object1 VARIANT);

INSERT INTO multiple_types
    (array1, array2, boolean1, varchar1, varchar2,
     decimal1, double1, integer1, object1)
  SELECT
    TO_VARIANT(TO_ARRAY('Example')),
    TO_VARIANT(ARRAY_CONSTRUCT('Array-like', 'example')),
    TO_VARIANT(TRUE),
    TO_VARIANT('X'),
    TO_VARIANT('I am a real character'),
    TO_VARIANT(1.23::DECIMAL(6, 3)),
    TO_VARIANT(3.21::DOUBLE),
    TO_VARIANT(15),
    TO_VARIANT(TO_OBJECT(PARSE_JSON('{"Tree": "Pine"}')));
```

Query the data using the [Typeof](typeof) function to show the data types of
the values stored in the VARIANT values.

Copy code

```
SELECT TYPEOF(array1),
       TYPEOF(array2),
       TYPEOF(boolean1),
       TYPEOF(varchar1),
       TYPEOF(varchar2),
       TYPEOF(decimal1),
       TYPEOF(double1),
       TYPEOF(integer1),
       TYPEOF(object1)
  FROM multiple_types;
```

```
+----------------+----------------+------------------+------------------+------------------+------------------+-----------------+------------------+-----------------+
| TYPEOF(ARRAY1) | TYPEOF(ARRAY2) | TYPEOF(BOOLEAN1) | TYPEOF(VARCHAR1) | TYPEOF(VARCHAR2) | TYPEOF(DECIMAL1) | TYPEOF(DOUBLE1) | TYPEOF(INTEGER1) | TYPEOF(OBJECT1) |
|----------------+----------------+------------------+------------------+------------------+------------------+-----------------+------------------+-----------------|
| ARRAY          | ARRAY          | BOOLEAN          | VARCHAR          | VARCHAR          | DECIMAL          | DOUBLE          | INTEGER          | OBJECT          |
+----------------+----------------+------------------+------------------+------------------+------------------+-----------------+------------------+-----------------+
```

Show whether a column contains floating-point numbers, fixed-point numbers, or integers in
the data by using the IS\_DOUBLE function in a SELECT list:

Copy code

```
SELECT IS_DOUBLE(boolean1),
       IS_DOUBLE(decimal1),
       IS_DOUBLE(double1),
       IS_DOUBLE(integer1)
  FROM multiple_types;
```

```
+---------------------+---------------------+--------------------+---------------------+
| IS_DOUBLE(BOOLEAN1) | IS_DOUBLE(DECIMAL1) | IS_DOUBLE(DOUBLE1) | IS_DOUBLE(INTEGER1) |
|---------------------+---------------------+--------------------+---------------------|
| False               | True                | True               | True                |
+---------------------+---------------------+--------------------+---------------------+
```
