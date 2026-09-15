Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_MAX

Given an input [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array), returns the element with the highest value that is not a SQL NULL. If the input ARRAY
is empty or contains only SQL NULL elements, this function returns NULL.

## Syntax

Copy code

```
ARRAY_MAX( <array> )
```

## Arguments

`array`
:   The input ARRAY.

## Returns

This function returns a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) that contains the element with the highest value that is not a SQL NULL.

The function returns NULL if `array` is NULL, empty, or contains only SQL NULL elements.

## Usage notes

- A SQL NULL is distinct from an explicit null value in semi-structured data (for example, a [JSON null](/user-guide/semistructured-considerations#label-variant-null)
  in JSON data). Explicit null values are considered when identifying the element with the highest value.

- The function determines the element to return by comparing the elements in the array. The function supports comparing elements
  of the same data type or of the following data types:

  - Elements of the NUMBER and FLOAT data types.
  - Elements of the TIMESTAMP\_LTZ and TIMESTAMP\_TZ data types.

  If the array contains elements of other data types, [cast](/sql-reference/functions/cast) the elements to a common data type,
  as shown in the example below.

## Examples

The following example returns a VARIANT containing the element with the highest value in an
[ARRAY constant](/sql-reference/data-types-semistructured#label-array-constant):

Copy code

```
SELECT ARRAY_MAX([20, 0, NULL, 10, NULL]);
```

```
+------------------------------------+
| ARRAY_MAX([20, 0, NULL, 10, NULL]) |
|------------------------------------|
| 20                                 |
+------------------------------------+
```

The following example demonstrates that a JSON null is handled differently than a SQL NULL. If `array` contains a JSON
null, the function returns the JSON null.

Copy code

```
SELECT ARRAY_MAX([NULL, PARSE_JSON('null'), NULL]);
```

```
+--------------------------------------------------+
| ARRAY_MAX([20, 0, PARSE_JSON('NULL'), 10, NULL]) |
|--------------------------------------------------|
| null                                             |
+--------------------------------------------------+
```

The following example demonstrates that the function returns NULL if the input ARRAY is empty:

Copy code

```
SELECT ARRAY_MAX([]);
```

```
+---------------+
| ARRAY_MAX([]) |
|---------------|
| NULL          |
+---------------+
```

The following example demonstrates that the function returns NULL if the input ARRAY contains only SQL NULLs:

Copy code

```
SELECT ARRAY_MAX([NULL, NULL, NULL]);
```

```
+-------------------------+
| ARRAY_MAX([NULL, NULL]) |
|-------------------------|
| NULL                    |
+-------------------------+
```

To determine the maximum value in an array with elements of different data types, [cast](/sql-reference/functions/cast) the elements
to the same data type. The following example casts a DATE element to a TIMESTAMP element to determine the maximum value in the array:

Copy code

```
SELECT ARRAY_MAX([date1::TIMESTAMP, timestamp1]) AS array_max
  FROM (
      VALUES ('1999-01-01'::DATE, '2023-12-09 22:09:26.000000000'::TIMESTAMP),
             ('2023-12-09'::DATE, '1999-01-01 22:09:26.000000000'::TIMESTAMP)
          AS t(date1, timestamp1)
      );
```

```
+---------------------------+
| ARRAY_MAX                 |
|---------------------------|
| "2023-12-09 22:09:26.000" |
| "2023-12-09 00:00:00.000" |
+---------------------------+
```
