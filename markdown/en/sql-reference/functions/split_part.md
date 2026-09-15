Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# SPLIT\_PART

Splits a given string at a specified character and returns the requested part.

To return all characters after a specified character, you can use the [POSITION](/sql-reference/functions/position)
and [SUBSTR](/sql-reference/functions/substr) functions. For an example, see
[Returning substrings for email, phone, and date strings](/sql-reference/functions/substr#label-substr-function-return-substrings-after-specified-character).

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

See also:
:   [SPLIT](/sql-reference/functions/split), [STRTOK](/sql-reference/functions/strtok)

## Syntax

Copy code

```
SPLIT_PART(<string>, <delimiter>, <partNumber>)
```

## Arguments

`string`
:   Text to be split into parts.

`delimiter`
:   Text representing the delimiter to split by. The entire delimiter string is treated as a single delimiter,
    even if it contains multiple characters. This behavior differs from [STRTOK](/sql-reference/functions/strtok), which treats each
    character in the delimiter as a separate delimiter.

`partNumber`
:   Requested part of the split, which is 1-based so that the first token is token number 1,
    not token number 0.

    If the value is negative, the parts are counted backward from the end of the string.

## Returns

This function returns a value of type VARCHAR.

If any argument is NULL, the function returns NULL.

## Usage notes

- If the `partNumber` is out of range, the returned value is an empty string.
- If the string starts or is terminated with the delimiter, the system
  considers empty space before or after the delimiter, respectively, as a
  valid part of the split result. For an example, see the [Examples](#examples) section below.
  This means SPLIT\_PART can return empty strings as parts, unlike [STRTOK](/sql-reference/functions/strtok), which never returns empty strings.
- If the `partNumber` is 0, it is treated as 1. In other words, it gets the first element of the split.
  To avoid confusion over whether indexes are 1-based or 0-based, Snowflake recommends avoiding the use of 0
  as a synonym for 1.
- If the delimiter is an empty string, then after the split, the returned value is the input string (the
  string isn’t split).

## Collation details

The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.

This function does not support the following collation specifications:

- `pi` (punctuation-insensitive).
- `cs-ai` (case-sensitive, accent-insensitive).

## Examples

The following examples call the SPLIT\_PART function:

- [Demonstrate the parts returned for different part number values](#demonstrate-the-parts-returned-for-different-part-number-values)
- [Return the first and last part of an IP address](#return-the-first-and-last-part-of-an-ip-address)
- [Demonstrate the delimiter as the first character](#demonstrate-the-delimiter-as-the-first-character)
- [Demonstrate a multi-character delimiter](#demonstrate-a-multi-character-delimiter)
- [Demonstrate the delimiter as an empty string](#demonstrate-the-delimiter-as-an-empty-string)
- [Demonstrate differences between STRTOK and SPLIT\_PART](#demonstrate-differences-between-strtok-and-split-part)

### Demonstrate the parts returned for different part number values

The following example shows the portions returned by different `partNumber` values:

Copy code

```
SELECT column1 part_number_value, column2 portion
  FROM VALUES
    (0, SPLIT_PART('11.22.33', '.',  0)),
    (1, SPLIT_PART('11.22.33', '.',  1)),
    (2, SPLIT_PART('11.22.33', '.',  2)),
    (3, SPLIT_PART('11.22.33', '.',  3)),
    (4, SPLIT_PART('11.22.33', '.',  4)),
    (-1, SPLIT_PART('11.22.33', '.',  -1)),
    (-2, SPLIT_PART('11.22.33', '.',  -2)),
    (-3, SPLIT_PART('11.22.33', '.',  -3)),
    (-4, SPLIT_PART('11.22.33', '.',  -4));
```

```
+-------------------+---------+
| PART_NUMBER_VALUE | PORTION |
|-------------------+---------|
|                 0 | 11      |
|                 1 | 11      |
|                 2 | 22      |
|                 3 | 33      |
|                 4 |         |
|                -1 | 33      |
|                -2 | 22      |
|                -3 | 11      |
|                -4 |         |
+-------------------+---------+
```

### Return the first and last part of an IP address

The following example returns the first and last parts of the localhost IP address `127.0.0.1`:

Copy code

```
SELECT SPLIT_PART('127.0.0.1', '.', 1) AS first_part,
       SPLIT_PART('127.0.0.1', '.', -1) AS last_part;
```

```
+------------+-----------+
| FIRST_PART | LAST_PART |
|------------+-----------|
| 127        | 1         |
+------------+-----------+
```

### Demonstrate the delimiter as the first character

The following example returns the first and second parts of a string of characters that are separated by vertical bars. The
delimiter is the first part of the input string, so the first element after the split is an empty string.

Copy code

```
SELECT SPLIT_PART('%a%b%c%', '|', 1) AS first_part,
       SPLIT_PART('%a%b%c%', '|', 2) AS last_part;
```

```
+------------+-----------+
| FIRST_PART | LAST_PART |
|------------+-----------|
|            | a         |
+------------+-----------+
```

### Demonstrate a multi-character delimiter

The following example shows a multi-character delimiter:

Copy code

```
SELECT SPLIT_PART('aaa--bbb-BBB--ccc', '--', 2) AS multi_character_delimiter;
```

```
+---------------------------+
| MULTI_CHARACTER_DELIMITER |
|---------------------------|
| bbb-BBB                   |
+---------------------------+
```

### Demonstrate the delimiter as an empty string

The following example shows that if the delimiter is an empty string, then after the split, there is still only one
string:

Copy code

```
SELECT column1 part_number_value, column2 portion
  FROM VALUES
    (1, SPLIT_PART('user@snowflake.com', '',  1)),
    (-1, SPLIT_PART('user@snowflake.com', '', -1)),
    (2, SPLIT_PART('user@snowflake.com', '',  2)),
    (-2, SPLIT_PART('user@snowflake.com', '', -2));
```

```
+-------------------+--------------------+
| PART_NUMBER_VALUE | PORTION            |
|-------------------+--------------------|
|                 1 | user@snowflake.com |
|                -1 | user@snowflake.com |
|                 2 |                    |
|                -2 |                    |
+-------------------+--------------------+
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
