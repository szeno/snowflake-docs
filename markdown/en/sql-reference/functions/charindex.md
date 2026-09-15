Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# CHARINDEX

Searches for the first occurrence of the first argument in the second argument and, if successful, returns the position (1-based) of the first argument in the second argument.

Aliases:
:   [POSITION](/sql-reference/functions/position)

    Note that the CHARINDEX function does not support one of the syntax variations that POSITION supports.

## Syntax

Copy code

```
CHARINDEX( <expr1>, <expr2> [ , <start_pos> ] )
```

## Arguments

**Required:**

`expr1`
:   A string or binary expression representing the value to look for.

`expr2`
:   A string or binary expression representing the value to search.

**Optional:**

`start_pos`
:   A number indicating the position from where to start the search (with `1` representing the start of `expr2`).

    Default: `1`

## Usage notes

- If any arguments are NULL, the function returns NULL.
- If the string or binary value is not found, the function returns `0`.
- If the specified optional `start_pos` is beyond the end of the second argument (the string to
  search), the function returns `0`.
- If the first argument is empty (e.g. an empty string), the function returns `1`.
- The data types of the first two arguments should be the same; either both
  should be strings or both should be binary values.

## Collation details

This function does not support the following collation specifications:

- `pi` (punctuation-insensitive).
- `cs-ai` (case-sensitive, accent-insensitive).

## Examples

### VARCHAR expressions

Find the first occurrence of ‘an’ in ‘banana’:

> Copy code
>
> ```
> select charindex('an', 'banana', 1);
> +------------------------------+
> | CHARINDEX('AN', 'BANANA', 1) |
> |------------------------------|
> |                            2 |
> +------------------------------+
> ```

Find the first occurrence of ‘an’ in ‘banana’ at or after position 3. This search finds the second occurrence of ‘an’.

> Copy code
>
> ```
> select charindex('an', 'banana', 3);
> +------------------------------+
> | CHARINDEX('AN', 'BANANA', 3) |
> |------------------------------|
> |                            4 |
> +------------------------------+
> ```

Search for various characters, including unicode characters, in strings:

> Copy code
>
> ```
> SELECT n, h, CHARINDEX(n, h) FROM pos;
>
> +--------+---------------------+-----------------+
> | N      | H                   | CHARINDEX(N, H) |
> |--------+---------------------+-----------------|
> |        |                     |               1 |
> |        | sth                 |               1 |
> | 43     | 41424344            |               5 |
> | a      | NULL                |            NULL |
> | dog    | catalog             |               0 |
> | log    | catalog             |               5 |
> | lésine | le péché, la lésine |              14 |
> | nicht  | Ich weiß nicht      |              10 |
> | sth    |                     |               0 |
> | ☃c     | ☃a☃b☃c☃d            |               5 |
> | ☃☃     | bunch of ☃☃☃☃       |              10 |
> | ❄c     | ❄a☃c❄c☃             |               5 |
> | NULL   | a                   |            NULL |
> | NULL   | NULL                |            NULL |
> +--------+---------------------+-----------------+
> ```

### BINARY expressions

Note that because the values below are hexadecimal representations, a single BINARY byte is represented as two hex
digits.

In this example, the returned value is 3 because ‘EF’ matches the 3rd
byte (the first byte is ‘AB’; the second byte is ‘CD’, and the third byte
is ‘EF’):

> Copy code
>
> ```
> SELECT CHARINDEX(X'EF', X'ABCDEF');
> +-----------------------------+
> | CHARINDEX(X'EF', X'ABCDEF') |
> |-----------------------------|
> |                           3 |
> +-----------------------------+
> ```

In this example, there is no match. Although the sequence ‘BC’ appears to be
in the value being searched, the ‘B’ is the second nybble of the first
byte, and the ‘C’ is the first nybble of the second byte; no byte actually
contains ‘BC’, so the returned value is 0 (not found).

> Copy code
>
> ```
> SELECT CHARINDEX(X'BC', X'ABCD');
> +---------------------------+
> | CHARINDEX(X'BC', X'ABCD') |
> |---------------------------|
> |                         0 |
> +---------------------------+
> ```
