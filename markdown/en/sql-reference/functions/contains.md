Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# CONTAINS

Returns true if `expr1` contains `expr2`. Both expressions must be text or binary expressions.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

## Syntax

Copy code

```
CONTAINS( <expr1> , <expr2> )
```

## Arguments

`expr1`
:   The string to search in.

`expr2`
:   The string to search for.

## Returns

Returns a BOOLEAN or NULL:

- Returns TRUE if `expr2` is found inside `expr1`.
- Returns FALSE if `expr2` is not found inside `expr1`.
- Returns NULL if either input expression is NULL.

## Usage notes

For comparisons that match a string against more than one specified pattern, you can use the following functions:

- [ILIKE ANY](/sql-reference/functions/ilike_any)
- [LIKE ALL](/sql-reference/functions/like_all)
- [LIKE ANY](/sql-reference/functions/like_any)

## Collation details

The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.

This function does not support the following collation specifications:

- `pi` (punctuation-insensitive).
- `cs-ai` (case-sensitive, accent-insensitive).

## Examples

These examples use the CONTAINS function.

### Determine whether column values contain a string

Create a table with a single column that contains string values.

Copy code

```
CREATE OR REPLACE TABLE strings_test (s VARCHAR);

INSERT INTO strings_test values
  ('coffee'),
  ('ice tea'),
  ('latte'),
  ('tea'),
  (NULL);

SELECT * from strings_test;
```

```
+---------+
| S       |
|---------|
| coffee  |
| ice tea |
| latte   |
| tea     |
| NULL    |
+---------+
```

Determine whether the values in column `s` contain the string `te`:

Copy code

```
SELECT * FROM strings_test WHERE CONTAINS(s, 'te');
```

```
+---------+
| S       |
|---------|
| ice tea |
| latte   |
| tea     |
+---------+
```

### Use CONTAINS with collation

In the following example, CONTAINS returns different results for the same argument
values with different collation specifications.

Copy code

```
SELECT CONTAINS(COLLATE('ñ', 'en-ci-ai'), 'n'),
       CONTAINS(COLLATE('ñ', 'es-ci-ai'), 'n');
```

```
+-----------------------------------------+-----------------------------------------+
| CONTAINS(COLLATE('Ñ', 'EN-CI-AI'), 'N') | CONTAINS(COLLATE('Ñ', 'ES-CI-AI'), 'N') |
|-----------------------------------------+-----------------------------------------|
| True                                    | False                                   |
+-----------------------------------------+-----------------------------------------+
```
