Categories:
:   [Conversion functions](/sql-reference/functions-conversion) , [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# TO\_ARRAY

Converts the input expression to an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) value.

## Syntax

Copy code

```
TO_ARRAY( <expr> )
```

## Arguments

`expr`
:   An expression of any data type.

## Returns

This function returns a value of type ARRAY or NULL:

> - If the input is an ARRAY, or a VARIANT containing an ARRAY value, the value is returned unchanged.
> - If `expr` is a NULL or [JSON null](/user-guide/semistructured-considerations#label-variant-null) value, the function returns NULL.
> - For any other value, the value returned is a single-element array that contains this value.

## Usage notes

To create an array that contains more than one element, you can use [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct)
or [STRTOK\_TO\_ARRAY](/sql-reference/functions/strtok_to_array).

## Examples

Create a table, and insert data by calling the TO\_ARRAY function:

Copy code

```
CREATE OR REPLACE TABLE array_demo_2 (
  ID INTEGER,
  array1 ARRAY,
  array2 ARRAY);

INSERT INTO array_demo_2 (ID, array1, array2)
  SELECT 1, TO_ARRAY(1), TO_ARRAY(3);

SELECT * FROM array_demo_2;
```

```
+----+--------+--------+
| ID | ARRAY1 | ARRAY2 |
|----+--------+--------|
|  1 | [      | [      |
|    |   1    |   3    |
|    | ]      | ]      |
+----+--------+--------+
```

Execute a query that shows the single-element arrays created during the insert and
the result of calling ARRAY\_CAT to concatenate the two arrays:

Copy code

```
SELECT array1, array2, ARRAY_CAT(array1, array2)
  FROM array_demo_2;
```

```
+--------+--------+---------------------------+
| ARRAY1 | ARRAY2 | ARRAY_CAT(ARRAY1, ARRAY2) |
|--------+--------+---------------------------|
| [      | [      | [                         |
|   1    |   3    |   1,                      |
| ]      | ]      |   3                       |
|        |        | ]                         |
+--------+--------+---------------------------+
```

This example demonstrates that TO\_ARRAY converts a string input expression to an array with a
single element, even when the input expression includes delimiters (such as commas):

Copy code

```
SELECT TO_ARRAY('snowman,snowball,snowcone') AS to_array_result;
```

```
+-------------------------------+
| TO_ARRAY_RESULT               |
|-------------------------------|
| [                             |
|   "snowman,snowball,snowcone" |
| ]                             |
+-------------------------------+
```

To convert the same string input expression into an array with multiple elements, you can use the
[STRTOK\_TO\_ARRAY](/sql-reference/functions/strtok_to_array) function:

Copy code

```
SELECT STRTOK_TO_ARRAY('snowman,snowball,snowcone', ',') AS strtok_to_array_result;
```

```
+------------------------+
| STRTOK_TO_ARRAY_RESULT |
|------------------------|
| [                      |
|   "snowman",           |
|   "snowball",          |
|   "snowcone"           |
| ]                      |
+------------------------+
```
