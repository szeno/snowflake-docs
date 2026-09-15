Categories:
:   [String & binary functions](/sql-reference/functions-string)

# COLLATE

Returns a copy of the original string, but with the specified `collation_specification` property instead of
the original `collation_specification` property.

This copy can be used in subsequent string comparisons, which will use the new `collation_specification`.

## Syntax

The COLLATE function can be called as a normal function:

Copy code

```
COLLATE(<string_expression>, '<collation_specification>')
```

The COLLATE function can be used as though it were an infix operator:

Copy code

```
<string_expression> COLLATE '<collation_specification>'
```

## Arguments

`string_expression`
:   The string to copy.

`collation_specification`
:   The collation to store with the copy of the string. For more information about collation
    specifiers, see [Collation specifications](/sql-reference/collation#label-collation-specification).

## Returns

Returns a copy of the original string, but with the specified
`collation_specification` property instead of the original
`collation_specification`.

## Usage notes

- Each VARCHAR contains a property that holds the collation specifier to use when comparing that VARCHAR to
  another VARCHAR. The COLLATE function copies the string, but applies the new collation specification
  rather than the original specification to the copy.

  The string itself is unchanged; only the collation specifier associated with the string is changed.
- When COLLATE is used as an infix operator, the `collation_specification` must be a constant string,
  not a general expression.

## Examples

The following examples show that calling the COLLATE function returns a copy of the string with a different
collation specification.

Note

For more examples that use the COLLATE function, see [Collation examples](/sql-reference/collation#label-collation-examples).

Create a table and insert a row. The collation specification of the value in the inserted row is `es`
(Spanish).

Copy code

```
CREATE OR REPLACE TABLE collation1 (v VARCHAR COLLATE 'es');
INSERT INTO collation1 (v) VALUES ('ñ');
```

This example shows that the COLLATE function does not change the string. The copied string in the third column is
lowercase, which is the same as the original string in the first column. However, the collation specification
of the value returned by COLLATE has changed from `es` to `es-ci`.

Copy code

```
SELECT v,
       COLLATION(v),
       COLLATE(v, 'es-ci'),
       COLLATION(COLLATE(v, 'es-ci'))
  FROM collation1;
```

```
+---+--------------+---------------------+--------------------------------+
| V | COLLATION(V) | COLLATE(V, 'ES-CI') | COLLATION(COLLATE(V, 'ES-CI')) |
|---+--------------+---------------------+--------------------------------|
| ñ | es           | ñ                   | es-ci                          |
+---+--------------+---------------------+--------------------------------+
```

This example shows that although the value returned by COLLATE is still a lowercase string, the `ci` collation
specifier is used when comparing that string to another string:

Copy code

```
SELECT v,
       v = 'ñ' AS "COMPARISON TO LOWER CASE",
       v = 'Ñ' AS "COMPARISON TO UPPER CASE",
       COLLATE(v, 'es-ci'),
       COLLATE(v, 'es-ci') = 'Ñ'
  FROM collation1;
```

```
+---+--------------------------+--------------------------+---------------------+---------------------------+
| V | COMPARISON TO LOWER CASE | COMPARISON TO UPPER CASE | COLLATE(V, 'ES-CI') | COLLATE(V, 'ES-CI') = 'Ñ' |
|---+--------------------------+--------------------------+---------------------+---------------------------|
| ñ | True                     | False                    | ñ                   | True                      |
+---+--------------------------+--------------------------+---------------------+---------------------------+
```

This example sorts the results using German collation.

Copy code

```
SELECT *
  FROM t1
  ORDER BY COLLATE(col1 , 'de');
```

The following two queries return the same result. The first uses COLLATE as a function, while the second uses
COLLATE as an infix operator:

Copy code

```
SELECT spanish_phrase FROM collation_demo 
  ORDER BY COLLATE(spanish_phrase, 'utf8');
```

Copy code

```
SELECT spanish_phrase FROM collation_demo 
  ORDER BY spanish_phrase COLLATE 'utf8';
```
