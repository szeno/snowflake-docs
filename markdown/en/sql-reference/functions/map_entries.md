Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Map)

# MAP\_ENTRIES

Returns an ARRAY value of key-value pair objects for each entry in a [MAP](/sql-reference/data-types-structured) value.

## Syntax

Copy code

```
MAP_ENTRIES( <map> )
```

## Arguments

`map`
:   The input MAP value.

## Returns

Returns an ARRAY value where each element is an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) with a `key` field and a
`value` field corresponding to an entry in the input MAP value.

If `map` is NULL, the function returns NULL.

If `map` is empty, the function returns an empty ARRAY value.

The order of the entries in the returned ARRAY value is undefined.

## Usage notes

- The function accepts exactly one argument. Calling the function with no arguments or more than one argument
  results in an error.

## Examples

Return the entries in a MAP value as key-value pair objects:

Copy code

```
SELECT MAP_ENTRIES({'a': 1, 'b': 2}::MAP(VARCHAR, INT)) AS entries;
```

```
+-----------------+
| ENTRIES         |
|-----------------|
| [               |
|   {             |
|     "key": "a", |
|     "value": 1  |
|   },            |
|   {             |
|     "key": "b", |
|     "value": 2  |
|   }             |
| ]               |
+-----------------+
```

Return an empty ARRAY value for an empty MAP value:

Copy code

```
SELECT MAP_ENTRIES({}::MAP(VARCHAR, INT)) AS entries;
```

```
+---------+
| ENTRIES |
|---------|
| []      |
+---------+
```

Return the entries in a MAP where the values are of type ARRAY:

Copy code

```
SELECT MAP_ENTRIES({'a': [1, 2, 3], 'b': [4, 5]}::MAP(VARCHAR, ARRAY(INT))) AS entries;
```

```
+-----------------+
| ENTRIES         |
|-----------------|
| [               |
|   {             |
|     "key": "a", |
|     "value": [  |
|       1,        |
|       2,        |
|       3         |
|     ]           |
|   },            |
|   {             |
|     "key": "b", |
|     "value": [  |
|       4,        |
|       5         |
|     ]           |
|   }             |
| ]               |
+-----------------+
```

Return NULL for a NULL input:

Copy code

```
SELECT MAP_ENTRIES(NULL::MAP(VARCHAR, INT)) AS entries;
```

```
+---------+
| ENTRIES |
|---------|
| NULL    |
+---------+
```
