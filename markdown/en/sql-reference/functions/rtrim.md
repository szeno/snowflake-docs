Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# RTRIM

Removes trailing characters, including whitespace, from a string.

Note

To remove characters in a string, you can use the [REPLACE](/sql-reference/functions/replace) function.

See also:
:   [LTRIM](/sql-reference/functions/ltrim) , [TRIM](/sql-reference/functions/trim)

## Syntax

Copy code

```
RTRIM(<expr> [, <characters> ])
```

## Arguments

`expr`
:   The string expression to be trimmed.

`characters`
:   One or more characters to remove from the right side of `expr`:

    The default value is `' '` (a single blank space character).
    If no characters are specified, only blank spaces are removed.

## Returns

This function returns a value of VARCHAR data type or NULL. If either argument is NULL, returns NULL.

## Usage notes

- You can specify the characters in `characters` in any order.
- A specification of `' '` in `characters` does not remove other whitespace
  characters (such as tabulation characters, end-of-line characters, and so on). Explicitly
  specify these characters to remove them.

- When `characters` is specified, you must explicitly specify the characters
  to remove whitespace. For example, `' $.'` removes all trailing blank spaces, dollar
  signs, and periods from the input string.

## Collation details

[Collation](/sql-reference/collation) is supported when the optional second argument is omitted, or when it
contains only whitespace.

The collation specification of the returned value is the same as the collation specification of the first argument.

## Examples

Remove trailing `0` and `.` characters from a string:

Copy code

```
SELECT RTRIM('$125.00', '0.');
```

```
+------------------------+
| RTRIM('$125.00', '0.') |
|------------------------|
| $125                   |
+------------------------+
```

The remaining examples use the following table data. Also, the queries enclose the strings
in `>` and `<` characters to help you visualize the whitespace.

Copy code

```
CREATE OR REPLACE TABLE test_rtrim_function(column1 VARCHAR);

INSERT INTO test_rtrim_function VALUES ('Trailing Spaces#  ');
```

Remove trailing whitespace from a string. This example does not specify the second
`characters` argument because the default is blank spaces.

Copy code

```
SELECT CONCAT('>', CONCAT(column1, '<')) AS original_value,
       CONCAT('>', CONCAT(RTRIM(column1), '<')) AS trimmed_value
  FROM test_rtrim_function;
```

```
+----------------------+--------------------+
| ORIGINAL_VALUE       | TRIMMED_VALUE      |
|----------------------+--------------------|
| >Trailing Spaces#  < | >Trailing Spaces#< |
+----------------------+--------------------+
```

Remove leading whitespace and `#` from a string. This example specifies the second
`characters` argument because it removes other characters in addition to
blank spaces.

Copy code

```
SELECT CONCAT('>', CONCAT(column1, '<')) AS original_value,
       CONCAT('>', CONCAT(RTRIM(column1, '# '), '<')) AS trimmed_value
  FROM test_rtrim_function;
```

```
+----------------------+-------------------+
| ORIGINAL_VALUE       | TRIMMED_VALUE     |
|----------------------+-------------------|
| >Trailing Spaces#  < | >Trailing Spaces< |
+----------------------+-------------------+
```
