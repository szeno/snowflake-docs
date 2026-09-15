Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_REPEAT

Returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) value containing a specified number of copies of an element.

## Syntax

Copy code

```
ARRAY_REPEAT( <element> , <count> )
```

## Arguments

`element`
:   The value to repeat in the output array.

    The value can be of any [semi-structured data type](/sql-reference/data-types-semistructured) — for example, VARIANT, ARRAY,
    OBJECT — or any standard Snowflake data type — for example, NUMBER, VARCHAR, BOOLEAN, DATE.

    [Structured types](/sql-reference/data-types-structured), such as MAP, aren’t supported.

`count`
:   An INTEGER expression specifying the number of times to repeat `element`.

## Returns

The function returns a [semi-structured ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) value containing `count` copies of
`element`.

If `count` is NULL, the function returns NULL.

## Usage notes

- If `count` is 0 or a negative number, the function returns an empty ARRAY.
- If `element` is NULL, the function returns an ARRAY of `count` NULL values.
- The `element` value is implicitly converted to VARIANT in the resulting ARRAY.

## Examples

The following example repeats an INTEGER value three times:

Copy code

```
SELECT ARRAY_REPEAT(42, 3);
```

```
+---------------------+
| ARRAY_REPEAT(42, 3) |
|---------------------|
| [                   |
|   42,               |
|   42,               |
|   42                |
| ]                   |
+---------------------+
```

The following example repeats a STRING value:

Copy code

```
SELECT ARRAY_REPEAT('hello', 2);
```

```
+--------------------------+
| ARRAY_REPEAT('hello', 2) |
|--------------------------|
| [                        |
|   "hello",               |
|   "hello"                |
| ]                        |
+--------------------------+
```

The following example repeats an ARRAY value to create a nested ARRAY:

Copy code

```
SELECT ARRAY_REPEAT([1, 2], 2);
```

```
+-------------------------+
| ARRAY_REPEAT([1, 2], 2) |
|-------------------------|
| [                       |
|   [                     |
|     1,                  |
|     2                   |
|   ],                    |
|   [                     |
|     1,                  |
|     2                   |
|   ]                     |
| ]                       |
+-------------------------+
```

The following example shows that a count of 0 returns an empty ARRAY value:

Copy code

```
SELECT ARRAY_REPEAT('x', 0);
```

```
+----------------------+
| ARRAY_REPEAT('x', 0) |
|----------------------|
| []                   |
+----------------------+
```

The following example shows that a NULL count returns NULL:

Copy code

```
SELECT ARRAY_REPEAT('hi', NULL);
```

```
+--------------------------+
| ARRAY_REPEAT('hi', NULL) |
|--------------------------|
| NULL                     |
+--------------------------+
```
