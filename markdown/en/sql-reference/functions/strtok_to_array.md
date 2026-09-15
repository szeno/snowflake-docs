Categories:
:   [String & binary functions](/sql-reference/functions-string) (General) , [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Conversion/Casting)

# STRTOK\_TO\_ARRAY

Tokenizes the given string using the given set of delimiters and returns the tokens as an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array)
value.

## Syntax

Copy code

```
STRTOK_TO_ARRAY( <string> [ , <delimiter> ] )
```

## Arguments

**Required:**

`string`
:   Text to be tokenized.

**Optional:**

`delimiter`
:   Set of delimiters.

    Default: A single space character.

## Returns

This function returns a value of type ARRAY or NULL.

The function returns an empty array if tokenization produces no tokens.

If either argument is a NULL or [JSON null](/user-guide/semistructured-considerations#label-variant-null) value, the function returns NULL.

## Examples

The following example uses the STRTOK\_TO\_ARRAY function to split a string into an array:

Copy code

```
SELECT STRTOK_TO_ARRAY('a.b.c', '.') AS string_to_array;
```

```
+-----------------+
| STRING_TO_ARRAY |
|-----------------|
| [               |
|   "a",          |
|   "b",          |
|   "c"           |
| ]               |
+-----------------+
```

The following example tokenizes on multiple delimiters (`.` and `@`):

Copy code

```
SELECT STRTOK_TO_ARRAY('user@snowflake.com', '.@') AS multiple_delimiters;
```

```
+---------------------+
| MULTIPLE_DELIMITERS |
|---------------------|
| [                   |
|   "user",           |
|   "snowflake",      |
|   "com"             |
| ]                   |
+---------------------+
```
