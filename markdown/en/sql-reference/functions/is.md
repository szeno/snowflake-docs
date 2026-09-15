Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Type Predicates)

# IS\_\_<object\_type>\_

This family of functions serves as Boolean predicates that can be used to determine the data type of a value stored in a VARIANT column:

- [IS\_ARRAY](/sql-reference/functions/is_array)
- [IS\_BINARY](/sql-reference/functions/is_binary)
- [IS\_BOOLEAN](/sql-reference/functions/is_boolean)
- [IS\_CHAR , IS\_VARCHAR](/sql-reference/functions/is_char-varchar)
- [IS\_DATE , IS\_DATE\_VALUE](/sql-reference/functions/is_date-value)
- [IS\_DECIMAL](/sql-reference/functions/is_decimal)
- [IS\_DOUBLE , IS\_REAL](/sql-reference/functions/is_double-real)
- [IS\_INTEGER](/sql-reference/functions/is_integer)
- [IS\_NULL\_VALUE](/sql-reference/functions/is_null_value)
- [IS\_OBJECT](/sql-reference/functions/is_object)
- [IS\_TIME](/sql-reference/functions/is_time)
- [IS\_TIMESTAMP\_\*](/sql-reference/functions/is_timestamp)

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as) , [TYPEOF](/sql-reference/functions/typeof)

## General usage notes

- All the functions are unary, taking a VARIANT expression as the only argument.
- All the functions return FALSE if the input is SQL NULL or the VARIANT expression contains NULL.

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

Count all rows in `vartab` table where the VARIANT column `v` contains a string value:

Copy code

```
SELECT COUNT(*) FROM vartab WHERE IS_VARCHAR(v);
```

```
+----------+
| COUNT(*) |
|----------|
|        1 |
+----------+
```

Select rows in `vartab` table where the VARIANT column `v` contains the specified data type:

Copy code

```
SELECT * FROM vartab WHERE IS_NULL_VALUE(v);
```

```
+---+------+
| N | V    |
|---+------|
| 1 | null |
+---+------+
```

Copy code

```
SELECT * FROM vartab WHERE IS_BOOLEAN(v);
```

```
+---+------+
| N | V    |
|---+------|
| 3 | true |
+---+------+
```

Copy code

```
SELECT * FROM vartab WHERE IS_INTEGER(v);
```

```
+---+-----+
| N | V   |
|---+-----|
| 4 | -17 |
+---+-----+
```

Copy code

```
SELECT * FROM vartab WHERE IS_DECIMAL(v);
```

```
+---+--------+
| N | V      |
|---+--------|
| 4 | -17    |
| 5 | 123.12 |
+---+--------+
```

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

Copy code

```
SELECT * FROM vartab WHERE IS_VARCHAR(v);
```

```
+---+------------------------+
| N | V                      |
|---+------------------------|
| 7 | "Om ara pa ca na dhih" |
+---+------------------------+
```

Copy code

```
SELECT * FROM vartab WHERE IS_ARRAY(v);
```

```
+---+-------------+
| N | V           |
|---+-------------|
| 8 | [           |
|   |   -1,       |
|   |   12,       |
|   |   289,      |
|   |   2188,     |
|   |   false,    |
|   |   undefined |
|   | ]           |
+---+-------------+
```

Copy code

```
SELECT * FROM vartab WHERE IS_OBJECT(v);
```

```
+---+---------------+
| N | V             |
|---+---------------|
| 9 | {             |
|   |   "x": "abc", |
|   |   "y": false, |
|   |   "z": 10     |
|   | }             |
+---+---------------+
```
