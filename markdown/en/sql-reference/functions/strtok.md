Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# STRTOK

Tokenizes a given string and returns the requested part.

See also:
:   [SPLIT\_PART](/sql-reference/functions/split_part)

## Syntax

Copy code

```
STRTOK(<string> [,<delimiter>] [,<partNumber>])
```

## Arguments

**Required:**

`string`
:   Text to be tokenized.

**Optional:**

`delimiter`
:   Text representing the set of delimiters to tokenize on. Each character in the delimiter string is a separate delimiter.
    For example, if the delimiter is `'@.'`, then both `'@'` and `'.'` are treated as delimiters. This
    behavior differs from [SPLIT\_PART](/sql-reference/functions/split_part), which treats the entire delimiter as a single delimiter string.

    If the delimiter is empty, and the `string` is empty, then the function returns NULL. If the
    delimiter is empty, and the `string` is non-empty, then the whole string will be treated as one token.

    Default: A single space character

`partNumber`
:   Requested token, which is 1-based so that the first token is token number 1, not token number 0.
    If the token number is out of range, then NULL is returned.

    Default: 1

## Returns

The data type of the returned value is VARCHAR.

If the requested part doesn’t exist or any argument is NULL, then NULL is returned.

## Usage notes

Similar to Linux strtok(), STRTOK never returns an empty string as a token.
This behavior differs from [SPLIT\_PART](/sql-reference/functions/split_part), which can return empty strings
as parts when the input string starts or ends with the delimiter, or when
there are consecutive delimiters.

## Examples

The following examples call the STRTOK function:

- [Return the first token in a string](#return-the-first-token-in-a-string)
- [Use multiple delimiters to return different tokens](#use-multiple-delimiters-to-return-different-tokens)
- [Demonstrate indexing past the last possible token in the string](#demonstrate-indexing-past-the-last-possible-token-in-the-string)
- [Demonstrate how the first element can be past the end of the string](#demonstrate-how-the-first-element-can-be-past-the-end-of-the-string)
- [Call STRTOK with an empty delimiter](#call-strtok-with-an-empty-delimiter)
- [Demonstrate NULL values for arguments](#demonstrate-null-values-for-arguments)
- [Demonstrate differences between STRTOK and SPLIT\_PART](#demonstrate-differences-between-strtok-and-split-part)

### Return the first token in a string

The following simple example calls STRTOK to return the first token in a string:

Copy code

```
SELECT STRTOK('a.b.c', '.', 1);
```

```
+-------------------------+
| STRTOK('A.B.C', '.', 1) |
|-------------------------|
| a                       |
+-------------------------+
```

### Use multiple delimiters to return different tokens

The following example shows how to use multiple delimiters to return the first, second, and third tokens
when the delimiters are `@` and `.`:

Copy code

```
SELECT STRTOK('user@snowflake.com', '@.', 1);
```

```
+---------------------------------------+
| STRTOK('USER@SNOWFLAKE.COM', '@.', 1) |
|---------------------------------------|
| user                                  |
+---------------------------------------+
```

Copy code

```
SELECT STRTOK('user@snowflake.com', '@.', 2);
```

```
+---------------------------------------+
| STRTOK('USER@SNOWFLAKE.COM', '@.', 2) |
|---------------------------------------|
| snowflake                             |
+---------------------------------------+
```

Copy code

```
SELECT STRTOK('user@snowflake.com', '@.', 3);
```

```
+---------------------------------------+
| STRTOK('USER@SNOWFLAKE.COM', '@.', 3) |
|---------------------------------------|
| com                                   |
+---------------------------------------+
```

### Demonstrate indexing past the last possible token in the string

The following example demonstrates what happens when you index past the last possible token in the string:

Copy code

```
SELECT STRTOK('user@snowflake.com.', '@.', 4);
```

```
+----------------------------------------+
| STRTOK('USER@SNOWFLAKE.COM.', '@.', 4) |
|----------------------------------------|
| NULL                                   |
+----------------------------------------+
```

### Demonstrate how the first element can be past the end of the string

In this example, the input string is empty, and there are no elements. So, the first
element is past the end of the string, and the function returns NULL instead of an empty string:

Copy code

```
SELECT STRTOK('', '', 1);
```

```
+-------------------+
| STRTOK('', '', 1) |
|-------------------|
| NULL              |
+-------------------+
```

### Call STRTOK with an empty delimiter

Here is an example with an empty delimiter string:

Copy code

```
SELECT STRTOK('a.b', '', 1);
```

```
+----------------------+
| STRTOK('A.B', '', 1) |
|----------------------|
| a.b                  |
+----------------------+
```

### Demonstrate NULL values for arguments

The following examples specify NULL values for each of the arguments:

Copy code

```
SELECT STRTOK(NULL, '.', 1);
```

```
+----------------------+
| STRTOK(NULL, '.', 1) |
|----------------------|
| NULL                 |
+----------------------+
```

Copy code

```
SELECT STRTOK('a.b', NULL, 1);
```

```
+------------------------+
| STRTOK('A.B', NULL, 1) |
|------------------------|
| NULL                   |
+------------------------+
```

Copy code

```
SELECT STRTOK('a.b', '.', NULL);
```

```
+--------------------------+
| STRTOK('A.B', '.', NULL) |
|--------------------------|
| NULL                     |
+--------------------------+
```

### Demonstrate differences between STRTOK and SPLIT\_PART

This example demonstrates the difference between STRTOK and SPLIT\_PART when using repeated delimiters.
STRTOK treats each character in the delimiter string `'|-'` as a separate delimiter, splitting at every
`'|'` and `'-'` character. In contrast, SPLIT\_PART treats the entire delimiter string `'|-'`
as a single delimiter, so it only splits where that exact sequence appears:

Copy code

```
SELECT STRTOK('data1|%data2%-data3---data4', '|-', 1) AS strtok_1,
       STRTOK('data1|%data2%-data3---data4', '|-', 2) AS strtok_2,
       STRTOK('data1|%data2%-data3---data4', '|-', 3) AS strtok_3,
       STRTOK('data1|%data2%-data3---data4', '|-', 4) AS strtok_4,
       SPLIT_PART('data1|%data2%-data3---data4', '|-', 1) AS split_part_1,
       SPLIT_PART('data1|%data2%-data3---data4', '|-', 2) AS split_part_2,
       SPLIT_PART('data1|%data2%-data3---data4', '|-', 3) AS split_part_3;
```

```
+----------+----------+----------+----------+-----------------+--------------+--------------+
| STRTOK_1 | STRTOK_2 | STRTOK_3 | STRTOK_4 | SPLIT_PART_1    | SPLIT_PART_2 | SPLIT_PART_3 |
|----------+----------+----------+----------+-----------------+--------------+--------------|
| data1    | data2    | data3    | data4    | data1||data2    | data3---data4|              |
+----------+----------+----------+----------+-----------------+--------------+--------------+
```
