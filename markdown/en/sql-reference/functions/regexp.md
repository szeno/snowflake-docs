Categories:
:   [String functions (regular expressions)](/sql-reference/functions-regexp)

# [ NOT ] REGEXP

Performs a comparison to determine whether a string matches or does not match a specified pattern. Both inputs
must be text expressions.

REGEXP is similar to the [[ NOT ] LIKE](/sql-reference/functions/like) function, but with POSIX extended regular expressions instead of SQL LIKE pattern syntax.
It supports more complex matching conditions than LIKE.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

Aliases:
:   [[ NOT ] RLIKE](/sql-reference/functions/rlike) (2nd syntax)

See also: [String functions (regular expressions)](/sql-reference/functions-regexp)

> [REGEXP\_COUNT](/sql-reference/functions/regexp_count) , [REGEXP\_INSTR](/sql-reference/functions/regexp_instr) , [REGEXP\_REPLACE](/sql-reference/functions/regexp_replace) , [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr)
>
> [[ NOT ] ILIKE](/sql-reference/functions/ilike) , [[ NOT ] LIKE](/sql-reference/functions/like)

## Syntax

Copy code

```
<subject> [ NOT ] REGEXP <pattern>
```

## Arguments

**Required:**

`subject`
:   The string to search for matches.

`pattern`
:   Pattern to match.

    For guidelines on specifying patterns, see [String functions (regular expressions)](/sql-reference/functions-regexp).

## Returns

Returns a BOOLEAN or NULL.

- When REGEXP is specified, the value is TRUE if there is a match. Otherwise, returns FALSE.
- When NOT REGEXP is specified, the value is TRUE if there is no match. Otherwise, returns FALSE.
- When either REGEXP or NOT REGEXP is specified, returns NULL if any argument is NULL.

# Usage Notes

- The function implicitly anchors a pattern at both ends (for example, `''` automatically becomes `'^$'`, and `'ABC'`
  automatically becomes `'^ABC$'`). For example, to match any string starting with `ABC`, the pattern is `'ABC.*'`.
- The backslash character (`\`) is the escape character. For more information, see [Specifying regular expressions in single-quoted string constants](/sql-reference/functions-regexp#label-regexp-escape-character-caveats).
- For more usage notes, see the [General usage notes](/sql-reference/functions-regexp#label-regexp-general-usage-notes) for regular expression functions.

## Collation Details

Arguments with collation specifications currently aren’t supported.

## Examples

The example below shows how to use REGEXP with a simple wildcard expression:

Create a table and load data:

Copy code

```
CREATE OR REPLACE TABLE strings (v VARCHAR(50));
INSERT INTO strings (v) VALUES
  ('San Francisco'),
  ('San Jose'),
  ('Santa Clara'),
  ('Sacramento');
```

Use wildcards to search for a pattern:

Copy code

```
SELECT v
  FROM strings
  WHERE v REGEXP 'San* [fF].*'
  ORDER BY v;
```

```
+---------------+
| V             |
|---------------|
| San Francisco |
+---------------+
```

The backslash character `\` is the escape character in regular expressions, and specifies special
characters or groups of characters. For example, `\s` is the regular expression for whitespace.

The Snowflake string parser, which parses literal strings, also treats backslash as an escape character. For
example, a backslash is used as part of the sequence of characters that specifies a tab character. Thus to create a
string that contains a single backslash, you must specify two backslashes. For example, compare the string in
the input statement below with the corresponding string in the output:

Copy code

```
INSERT INTO strings (v) VALUES
  ('Contains embedded single \\backslash');
```

Copy code

```
SELECT *
  FROM strings
  ORDER BY v;
```

```
+-------------------------------------+
| V                                   |
|-------------------------------------|
| Contains embedded single \backslash |
| Sacramento                          |
| San Francisco                       |
| San Jose                            |
| Santa Clara                         |
+-------------------------------------+
```

This example shows how to search for strings that start with `San`, where `San` is a complete word (for example, not
part of `Santa`). `\b` is the escape sequence for a word boundary.

Copy code

```
SELECT v, v REGEXP 'San\\b.*' AS matches
  FROM strings
  ORDER BY v;
```

```
+-------------------------------------+---------+
| V                                   | MATCHES |
|-------------------------------------+---------|
| Contains embedded single \backslash | False   |
| Sacramento                          | False   |
| San Francisco                       | True    |
| San Jose                            | True    |
| Santa Clara                         | False   |
+-------------------------------------+---------+
```

This example shows how to search for a blank followed by a backslash. Note that the single backslash to search for
is represented by four backslashes below; for REGEXP to look for a literal backslash, that backslash must be
escaped, so you need two backslashes. The string parser requires that each of those backslashes be escaped, so the
expression contains four backslashes to represent the one backslash that the expression is searching for:

Copy code

```
SELECT v, v REGEXP '.*\\s\\\\.*' AS matches
  FROM strings
  ORDER BY v;
```

```
+-------------------------------------+---------+
| V                                   | MATCHES |
|-------------------------------------+---------|
| Contains embedded single \backslash | True    |
| Sacramento                          | False   |
| San Francisco                       | False   |
| San Jose                            | False   |
| Santa Clara                         | False   |
+-------------------------------------+---------+
```

The following example is the same as the preceding example, except that it uses `$$` as a string delimiter to tell the
string parser that the string is a literal and that backslashes should not be interpreted as escape sequences. (The
backslashes are still interpreted as escape sequences by REGEXP.)

Copy code

```
SELECT v, v REGEXP $$.*\s\\.*$$ AS MATCHES
  FROM strings
  ORDER BY v;
```

```
+-------------------------------------+---------+
| V                                   | MATCHES |
|-------------------------------------+---------|
| Contains embedded single \backslash | True    |
| Sacramento                          | False   |
| San Francisco                       | False   |
| San Jose                            | False   |
| Santa Clara                         | False   |
+-------------------------------------+---------+
```
