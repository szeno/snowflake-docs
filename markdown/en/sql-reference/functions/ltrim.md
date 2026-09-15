Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# LTRIM

Removes leading characters, including whitespace, from a string.

Note

To remove characters in a string, you can use the [REPLACE](/sql-reference/functions/replace) function.

See also:
:   [RTRIM](/sql-reference/functions/rtrim) , [TRIM](/sql-reference/functions/trim)

## Syntax

Copy code

```
LTRIM( <expr> [, <characters> ] )
```

## Arguments

`expr`
:   The string expression to be trimmed.

`characters`
:   One or more characters to remove from the left side of `expr`.

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
  to remove whitespace. For example, `' $.'` removes all leading blank spaces, dollar
  signs, and periods from the input string.

## Collation details

[Collation](/sql-reference/collation) is supported when the optional second argument is omitted, or when it
contains only whitespace.

The collation specification of the returned value is the same as the collation specification of the first argument.

## Examples

Remove leading `0` and `#` characters from a string:

Copy code

```
SELECT LTRIM('#000000123', '0#');
```

```
+---------------------------+
| LTRIM('#000000123', '0#') |
|---------------------------|
| 123                       |
+---------------------------+
```

The remaining examples use the following table data. Also, the queries enclose the strings
in `>` and `<` characters to help you visualize the whitespace.

Copy code

```
CREATE OR REPLACE TABLE test_ltrim_function(column1 VARCHAR);

INSERT INTO test_ltrim_function VALUES ('  #Leading Spaces');
```

Remove leading whitespace from a string. This example does not specify the second
`characters` argument because the default is blank spaces.

Copy code

```
SELECT CONCAT('>', CONCAT(column1, '<')) AS original_value,
       CONCAT('>', CONCAT(LTRIM(column1), '<')) AS trimmed_value
  FROM test_ltrim_function;
```

```
+---------------------+-------------------+
| ORIGINAL_VALUE      | TRIMMED_VALUE     |
|---------------------+-------------------|
| >  #Leading Spaces< | >#Leading Spaces< |
+---------------------+-------------------+
```

Remove leading whitespace and `#` from a string. This example specifies the second
`characters` argument because it removes other characters in addition to
blank spaces.

Copy code

```
SELECT CONCAT('>', CONCAT(column1, '<')) AS original_value,
       CONCAT('>', CONCAT(LTRIM(column1, ' #'), '<')) AS trimmed_value
  FROM test_ltrim_function;
```

```
+---------------------+------------------+
| ORIGINAL_VALUE      | TRIMMED_VALUE    |
|---------------------+------------------|
| >  #Leading Spaces< | >Leading Spaces< |
+---------------------+------------------+
```
