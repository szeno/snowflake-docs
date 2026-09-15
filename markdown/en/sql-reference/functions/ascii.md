Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# ASCII

Returns the ASCII code for the first character of a string. If the string is empty, a value of `0` is returned.

See also:

> [CHAR](/sql-reference/functions/chr) , [UNICODE](/sql-reference/functions/unicode)

## Syntax

Copy code

```
ASCII( <input> )
```

## Arguments

`input`
:   The string for which the ASCII code for the first character in the string is returned.

## Returns

The value is an integer that is the numeric representation of the ASCII character. For example, if the
input is the letter ‘a’, then the return value is 97.

## Usage notes

The value 0 is returned for either of the following cases:

- The first character of the string contains the ASCII character corresponding to 0.
- The string is empty.

To distinguish between these two cases, use the LENGTH function to determine whether the string is empty.

## Examples

This example demonstrates the behavior for single ASCII characters, as well as special cases, such as multi-character strings, empty strings, and NULL values:

> Copy code
>
> ```
> SELECT column1, ASCII(column1)
>   FROM (values('!'), ('A'), ('a'), ('bcd'), (''), (null));
> +---------+----------------+
> | COLUMN1 | ASCII(COLUMN1) |
> |---------+----------------|
> | !       |             33 |
> | A       |             65 |
> | a       |             97 |
> | bcd     |             98 |
> |         |              0 |
> | NULL    |           NULL |
> +---------+----------------+
> ```
