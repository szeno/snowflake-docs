Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# INSERT

Replaces a substring of the specified length, starting at the specified
position, with a new string or binary value.

This function should not be confused with the [INSERT](/sql-reference/sql/insert) DML command.

## Syntax

Copy code

```
INSERT( <base_expr>, <pos>, <len>, <insert_expr> )
```

## Arguments

`base_expr`
:   The string or BINARY expression for which you want to insert/replace
    characters.

`pos`
:   The offset at which to start inserting characters. This is 1-based,
    not 0-based. In other words, the first character in the string is
    considered to be at position 1, not position 0. For example, to insert
    at the beginning of the string, set `pos` to 1.

    Valid values are between 1 and one more than the length of the string
    (inclusive).

    Setting `pos` to one more than the length of the string
    makes the operation equivalent to an append. (This also requires that the
    `len` parameter be 0 because you should not try to delete any
    characters past the last character.)

`len`
:   The number of characters (starting at `pos`) that you want
    to replace. Valid values range from 0 to the number of characters between
    `pos` and the end of the string. If this is 0, it means add the
    new characters without deleting any existing characters.

`insert_expr`
:   The string to insert into the `base_expr`. If this string
    is empty, and if `len` is greater than zero, then effectively the
    operation becomes a delete (some characters are deleted, and none are added).

## Usage notes

- The `base_expr` and `insert_expr` should be the same data
  type; either both should be string (e.g. VARCHAR) or both should be binary.
- If any of the arguments are NULL, the returned value is NULL.

## Returns

Returns a string or BINARY that is equivalent to making a copy of
`base_expr`, deleting `len` characters starting at
`pos`, and then inserting `insert_expr` at `pos`.

Note that the original input `base_expr` is not changed; the function
returns a separate (modified) copy.

## Examples

This is a simple example:

> Copy code
>
> ```
> SELECT INSERT('abc', 1, 2, 'Z') as STR;
> +-----+
> | STR |
> |-----|
> | Zc  |
> +-----+
> ```

This example shows that the length of the replacement string can be different
from the length of the substring being replaced:

> Copy code
>
> ```
> SELECT INSERT('abcdef', 3, 2, 'zzz') as STR;
> +---------+
> | STR     |
> |---------|
> | abzzzef |
> +---------+
> ```

This shows what happens when the replacement string is empty (the function deletes the
specified number of characters starting at the start position, and does not
add any characters):

> Copy code
>
> ```
> SELECT INSERT('abc', 2, 1, '') as STR;
> +-----+
> | STR |
> |-----|
> | ac  |
> +-----+
> ```

This uses `INSERT` as an append operation, by adding characters immediately
after the last character in the original string:

> Copy code
>
> ```
> SELECT INSERT('abc', 4, 0, 'Z') as STR;
> +------+
> | STR  |
> |------|
> | abcZ |
> +------+
> ```

The following all return NULL because at least one of the arguments is NULL:

> Copy code
>
> ```
> SELECT INSERT(NULL, 1, 2, 'Z') as STR;
> +------+
> | STR  |
> |------|
> | NULL |
> +------+
> ```
>
> Copy code
>
> ```
> SELECT INSERT('abc', NULL, 2, 'Z') as STR;
> +------+
> | STR  |
> |------|
> | NULL |
> +------+
> ```
>
> Copy code
>
> ```
> SELECT INSERT('abc', 1, NULL, 'Z') as STR;
> +------+
> | STR  |
> |------|
> | NULL |
> +------+
> ```
>
> Copy code
>
> ```
> SELECT INSERT('abc', 1, 2, NULL) as STR;
> +------+
> | STR  |
> |------|
> | NULL |
> +------+
> ```
