Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_\_<object\_type>\_

You can use this family of functions to perform strict casting of VARIANT values to values of other data types:

> - [AS\_ARRAY](/sql-reference/functions/as_array)
> - [AS\_BINARY](/sql-reference/functions/as_binary)
> - [AS\_BOOLEAN](/sql-reference/functions/as_boolean)
> - [AS\_CHAR , AS\_VARCHAR](/sql-reference/functions/as_char-varchar)
> - [AS\_DATE](/sql-reference/functions/as_date)
> - [AS\_DECIMAL , AS\_NUMBER](/sql-reference/functions/as_decimal-number)
> - [AS\_DOUBLE , AS\_REAL](/sql-reference/functions/as_double-real)
> - [AS\_INTEGER](/sql-reference/functions/as_integer)
> - [AS\_OBJECT](/sql-reference/functions/as_object)
> - [AS\_TIME](/sql-reference/functions/as_time)
> - [AS\_TIMESTAMP\_\*](/sql-reference/functions/as_timestamp)

See also:
:   [IS\_\*<object\_type>\*](/sql-reference/functions/is)

## General usage notes

- If the type of the value in the VARIANT argument doesn’t match the output
  value, then NULL is returned. For example, if the AS\_DATE function is passed a VARIANT value
  that doesn’t contain a DATE value, then NULL is returned.
- If the input is NULL, the output is NULL.

## Examples

The following examples use AS\_`object_type` functions.

### Cast values in VARIANT columns to different data types

Create the table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE multiple_types_example (
  array1 VARIANT,
  array2 VARIANT,
  boolean1 VARIANT,
  char1 VARIANT,
  varchar1 VARIANT,
  decimal1 VARIANT,
  double1 VARIANT,
  integer1 VARIANT,
  object1 VARIANT);

INSERT INTO multiple_types_example
  (array1, array2, boolean1, char1, varchar1,
   decimal1, double1, integer1, object1)
  SELECT
    TO_VARIANT(TO_ARRAY('Example')),
    TO_VARIANT(ARRAY_CONSTRUCT('Array-like', 'example')),
    TO_VARIANT(TRUE),
    TO_VARIANT('X'),
    TO_VARIANT('Y'),
    TO_VARIANT(1.23::DECIMAL(6, 3)),
    TO_VARIANT(3.21::DOUBLE),
    TO_VARIANT(15),
    TO_VARIANT(TO_OBJECT(PARSE_JSON('{"Tree": "Pine"}')));
```

Query the table and cast values in the VARIANT columns to values of different data types:

Copy code

```
SELECT AS_ARRAY(array1) AS array1,
       AS_ARRAY(array2) AS array2,
       AS_BOOLEAN(boolean1) AS boolean,
       AS_CHAR(char1) AS char,
       AS_VARCHAR(varchar1) AS varchar,
       AS_DECIMAL(decimal1, 6, 3) AS decimal,
       AS_DOUBLE(double1) AS double,
       AS_INTEGER(integer1) AS integer,
       AS_OBJECT(object1) AS object
  FROM multiple_types_example;
```

```
+-------------+-----------------+---------+------+---------+---------+--------+---------+------------------+
| ARRAY1      | ARRAY2          | BOOLEAN | CHAR | VARCHAR | DECIMAL | DOUBLE | INTEGER | OBJECT           |
|-------------+-----------------+---------+------+---------+---------+--------+---------+------------------|
| [           | [               | True    | X    | Y       |   1.230 |   3.21 |      15 | {                |
|   "Example" |   "Array-like", |         |      |         |         |        |         |   "Tree": "Pine" |
| ]           |   "example"     |         |      |         |         |        |         | }                |
|             | ]               |         |      |         |         |        |         |                  |
+-------------+-----------------+---------+------+---------+---------+--------+---------+------------------+
```

### Compute the average of numeric values in a VARIANT column

Compute the average of all numeric values from a VARIANT column in the `vartab` table:

Create the table and load data into it:

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

Show the data types of the values (some of which are numeric):

Copy code

```
SELECT n, AS_REAL(v), TYPEOF(v)
  FROM vartab
  ORDER BY n;
```

```
+---+------------+------------+
| N | AS_REAL(V) | TYPEOF(V)  |
|---+------------+------------|
| 1 |       NULL | NULL_VALUE |
| 2 |       NULL | NULL       |
| 3 |       NULL | BOOLEAN    |
| 4 |     -17    | INTEGER    |
| 5 |     123.12 | DECIMAL    |
| 6 |     191.2  | DOUBLE     |
| 7 |       NULL | VARCHAR    |
| 8 |       NULL | ARRAY      |
| 9 |       NULL | OBJECT     |
+---+------------+------------+
```

Use the AS\_REAL function with the [AVG](/sql-reference/functions/avg) function to compute the average of all numeric values
from the VARIANT column `v`:

Copy code

```
SELECT AVG(AS_REAL(v)) FROM vartab;
```

```
+-----------------+
| AVG(AS_REAL(V)) |
|-----------------|
|    99.106666667 |
+-----------------+
```
