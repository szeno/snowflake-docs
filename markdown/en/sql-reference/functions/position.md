Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# POSITION

Searches for the first occurrence of the first argument in the second argument and, if successful, returns the position (1-based) of the first argument in the second argument.

If you need to find the position beyond the first occurrence (for example, the third occurrence), you can use the [REGEXP\_INSTR](/sql-reference/functions/regexp_instr) function.

Aliases:
:   [CHARINDEX](/sql-reference/functions/charindex)

    Note that the CHARINDEX function does not support one of the syntax variations that POSITION supports.

## Syntax

Copy code

```
POSITION( <expr1>, <expr2> [ , <start_pos> ] )

POSITION( <expr1> IN <expr2> )
```

## Arguments

**Required:**

`expr1`
:   A string or binary expression representing the value to look for.

`expr2`
:   A string or binary expression representing the value to search.

**Optional:**

`start_pos`
:   A number indicating the position at which to start the search (with `1` representing the start of `expr2`).

    Default: `1`

## Returns

This function returns a value of type NUMBER.

If any argument is NULL, the function returns NULL.

## Usage notes

- If the string or binary value is not found, the function returns `0`.
- If the specified optional `start_pos` is beyond the end of the second argument (the string to
  search), the function returns `0`.
- If the first argument is empty (for example, an empty string), the function returns `1`.
- The data types of the first two arguments must be the same (either two strings or two binary values).

## Collation details

This function does not support the following collation specifications:

- `pi` (punctuation-insensitive).
- `cs-ai` (case-sensitive, accent-insensitive).

## Examples

The following examples use the POSITION function.

### VARCHAR expressions

Find the first occurrence of ‘an’ in ‘banana’:

Copy code

```
SELECT POSITION('an', 'banana', 1);
```

```
+-----------------------------+
| POSITION('AN', 'BANANA', 1) |
|-----------------------------|
|                           2 |
+-----------------------------+
```

Find the first occurrence of ‘an’ in ‘banana’ at or after position 3. This search finds the second occurrence of ‘an’.

Copy code

```
SELECT POSITION('an', 'banana', 3);
```

```
+-----------------------------+
| POSITION('AN', 'BANANA', 3) |
|-----------------------------|
|                           4 |
+-----------------------------+
```

Search for various characters, including unicode characters, in strings:

Copy code

```
SELECT n, h, POSITION(n IN h) FROM pos;
```

```
+--------+---------------------+------------------+
| N      | H                   | POSITION(N IN H) |
|--------+---------------------+------------------|
|        |                     |                1 |
|        | sth                 |                1 |
| 43     | 41424344            |                5 |
| a      | NULL                |             NULL |
| dog    | catalog             |                0 |
| log    | catalog             |                5 |
| lésine | le péché, la lésine |               14 |
| nicht  | Ich weiß nicht      |               10 |
| sth    |                     |                0 |
| ☃c     | ☃a☃b☃c☃d            |                5 |
| ☃☃     | bunch of ☃☃☃☃       |               10 |
| ❄c     | ❄a☃c❄c☃             |                5 |
| NULL   | a                   |             NULL |
| NULL   | NULL                |             NULL |
+--------+---------------------+------------------+
```

### BINARY expressions

Because the values below are hexadecimal representations, a single BINARY byte is represented as two hex
digits.

In this example, the returned value is `3` because ‘EF’ matches the 3rd
byte (the first byte is ‘AB’; the second byte is ‘CD’, and the third byte
is ‘EF’):

Copy code

```
SELECT POSITION(X'EF', X'ABCDEF');
```

```
+----------------------------+
| POSITION(X'EF', X'ABCDEF') |
|----------------------------|
|                          3 |
+----------------------------+
```

In this example, there is no match. Although the sequence ‘BC’ appears to be
in the value being searched, the ‘B’ is the second nybble of the first
byte, and the ‘C’ is the first nybble of the second byte. No byte actually
contains ‘BC’, so the returned value is `0` (not found).

Copy code

```
SELECT POSITION(X'BC', X'ABCD');
```

```
+--------------------------+
| POSITION(X'BC', X'ABCD') |
|--------------------------|
|                        0 |
+--------------------------+
```
