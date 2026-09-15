Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_TO\_STRING

Returns an input array converted to a string by casting all values to strings (using [TO\_VARCHAR](/sql-reference/functions/to_char)) and concatenating them (using the string from the second argument to separate the
elements).

## Syntax

Copy code

```
ARRAY_TO_STRING( <array> , <separator_string> )
```

## Arguments

`array`
:   The array of elements to convert to a string.

`separator_string`
:   The string to put between each element, typically a space, comma, or other human-readable separator.

## Returns

This function returns a value of type VARCHAR.

## Usage notes

- A NULL argument returns NULL as a result.
- A NULL in an array is converted to an empty string in the result.
- To include a blank space between values, you must precede the space with the separator character
  (e.g. `', '`). See the examples below.

## Examples

Return various arrays as concatenated strings:

Copy code

```
SELECT column1,
       ARRAY_TO_STRING(PARSE_JSON(column1), '') AS no_separation,
       ARRAY_TO_STRING(PARSE_JSON(column1), ', ') AS comma_separated
  FROM VALUES
    (NULL),
    ('[]'),
    ('[1]'),
    ('[1, 2]'),
    ('[true, 1, -1.2e-3, "Abc", ["x","y"], {"a":1}]'),
    ('[, 1]'),
    ('[1, ]'),
    ('[1, , ,2]');
```

```
+-----------------------------------------------+---------------------------------+-------------------------------------------+
| COLUMN1                                       | NO_SEPARATION                   | COMMA_SEPARATED                           |
|-----------------------------------------------+---------------------------------+-------------------------------------------|
| NULL                                          | NULL                            | NULL                                      |
| []                                            |                                 |                                           |
| [1]                                           | 1                               | 1                                         |
| [1, 2]                                        | 12                              | 1, 2                                      |
| [true, 1, -1.2e-3, "Abc", ["x","y"], {"a":1}] | true1-0.0012Abc["x","y"]{"a":1} | true, 1, -0.0012, Abc, ["x","y"], {"a":1} |
| [, 1]                                         | 1                               | , 1                                       |
| [1, ]                                         | 1                               | 1,                                        |
| [1, , ,2]                                     | 12                              | 1, , , 2                                  |
+-----------------------------------------------+---------------------------------+-------------------------------------------+
```

This example returns an array that contains a NULL value as a concatenated string. First, create
a table and insert an array:

Copy code

```
CREATE TABLE test_array_to_string_with_null(a ARRAY);

INSERT INTO test_array_to_string_with_null
  SELECT (['A', NULL, 'B']);
```

Return the array as a concatenated string:

Copy code

```
SELECT a,
       ARRAY_TO_STRING(a, ''),
       ARRAY_TO_STRING(a, ', ')
  FROM test_array_to_string_with_null;
```

```
+--------------+------------------------+--------------------------+
| A            | ARRAY_TO_STRING(A, '') | ARRAY_TO_STRING(A, ', ') |
|--------------+------------------------+--------------------------|
| [            | AB                     | A, , B                   |
|   "A",       |                        |                          |
|   undefined, |                        |                          |
|   "B"        |                        |                          |
| ]            |                        |                          |
+--------------+------------------------+--------------------------+
```
