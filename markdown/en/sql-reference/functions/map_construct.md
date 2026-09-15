Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Map)

# MAP\_CONSTRUCT

Returns a [MAP](/sql-reference/data-types-structured) constructed from a series of alternating keys and values.

See also:
:   [MAP\_KEYS](/sql-reference/functions/map_keys), [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct), [OBJECT\_CONSTRUCT\_KEEP\_NULL\_STRUCTURED](/sql-reference/functions/object_construct_keep_null_structured)

## Syntax

Copy code

```
MAP_CONSTRUCT( <key_1>, <value_1> [ , <key_2>, <value_2> , ... ] )
```

## Arguments

`key_N`
:   The key in a key-value pair. A key must be a VARCHAR or numeric value. All of the keys are cast to a
    single, common key type.

`value_N`
:   The value that is associated with the key. All of the values are cast to a single, common value type.

## Returns

Returns a [MAP](/sql-reference/data-types-structured) whose key type is the common type of the keys
(VARCHAR or a numeric type) and whose value type is the common type of the values. For example,
`MAP_CONSTRUCT('a', 1, 'b', 2)` returns a `MAP(VARCHAR, NUMBER)` value.

## Usage notes

- You must specify an even number of arguments (one or more key-value pairs). Specifying an odd number of arguments
  returns an error.
- A key must be a VARCHAR or numeric value. Other key types (for example, BOOLEAN or DATE) aren’t supported and
  return an error.
- All of the keys are cast to a single, common key type, and all of the values are cast to a single, common value type.
  For example, in `MAP_CONSTRUCT(1, 'a', '2', 'b')` the keys are unified to a numeric type.
- The keys in a map must be unique. If two keys are equal, the function returns an error.
- If a key is NULL, the key-value pair is omitted from the resulting map.
- If a value is NULL, the key-value pair is kept.
- The entries in the resulting map are ordered by key.
- To construct a semi-structured [OBJECT](/sql-reference/data-types-semistructured) instead of a MAP, use
  [OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct) or [OBJECT\_CONSTRUCT\_KEEP\_NULL](/sql-reference/functions/object_construct_keep_null).

## Examples

Construct a map from alternating keys and values:

Copy code

```
SELECT MAP_CONSTRUCT('a', 1, 'b', 2) AS constructed_map;
```

```
+-----------------+
| CONSTRUCTED_MAP |
|-----------------|
| {               |
|   "a": 1,       |
|   "b": 2        |
| }               |
+-----------------+
```

The entries in the resulting map are ordered by key, regardless of the order of the arguments:

Copy code

```
SELECT MAP_KEYS(MAP_CONSTRUCT('b', 2, 'a', 1)) AS keys;
```

```
+-----------+
| KEYS      |
|-----------|
| [         |
|   "a",    |
|   "b"     |
| ]         |
+-----------+
```

Because a NULL key is omitted, the following statement constructs a map with a single entry:

Copy code

```
SELECT MAP_CONSTRUCT(NULL, 1, 'a', 2) AS constructed_map;
```

```
+-----------------+
| CONSTRUCTED_MAP |
|-----------------|
| {               |
|   "a": 2        |
| }               |
+-----------------+
```

Because the keys in a map must be unique, specifying a duplicate key returns an error:

Copy code

```
SELECT MAP_CONSTRUCT('a', 1, 'a', 2);
```

```
100103 (22000): Duplicate field key 'a'
```
