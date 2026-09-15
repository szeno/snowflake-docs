Categories:
:   [String functions (regular expressions)](/sql-reference/functions-regexp)

# [ NOT ] RLIKE

Performs a comparison to determine whether a string matches or does not match a specified pattern. Both inputs must be text expressions.

RLIKE is similar to the [[ NOT ] LIKE](/sql-reference/functions/like) function, but with POSIX extended regular expressions instead of SQL LIKE pattern syntax.
It supports more complex matching conditions than LIKE.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

Aliases:
:   [[ NOT ] REGEXP](/sql-reference/functions/regexp) (2nd syntax) , [REGEXP\_LIKE](/sql-reference/functions/regexp_like) (1st syntax)

See also: [String functions (regular expressions)](/sql-reference/functions-regexp)

> [REGEXP\_COUNT](/sql-reference/functions/regexp_count) , [REGEXP\_INSTR](/sql-reference/functions/regexp_instr) , [REGEXP\_REPLACE](/sql-reference/functions/regexp_replace) , [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr) , [REGEXP\_SUBSTR\_ALL](/sql-reference/functions/regexp_substr_all)
>
> [[ NOT ] ILIKE](/sql-reference/functions/ilike) , [[ NOT ] LIKE](/sql-reference/functions/like)

## Syntax

Copy code

```
-- 1st syntax
RLIKE( <subject> , <pattern> [ , <parameters> ] )

-- 2nd syntax
<subject> [ NOT ] RLIKE <pattern>
```

## Arguments

**Required:**

`subject`
:   The string to search for matches.

`pattern`
:   Pattern to match.

    For guidelines on specifying patterns, see [String functions (regular expressions)](/sql-reference/functions-regexp).

**Optional:**

`parameters`
> String of one or more characters that specifies the parameters used for searching for matches. Supported values:
>
> | Parameter | Description |
> | --- | --- |
> | `c` | Case-sensitive matching |
> | `i` | Case-insensitive matching |
> | `m` | Multi-line mode |
> | `e` | Extract submatches |
> | `s` | Single-line mode POSIX wildcard character `.` matches `\n` |
>
> Expand
>
> Show lessSee more
>
> Default: `c`
>
> For more information, see [Specifying the parameters for the regular expression](/sql-reference/functions-regexp#label-regexp-parameters-argument).

## Returns

Returns a BOOLEAN or NULL.

- When RLIKE is specified, the value is TRUE if there is a match. Otherwise, returns FALSE.
- When NOT RLIKE is specified, the value is TRUE if there is no match. Otherwise, returns FALSE.
- When either RLIKE or NOT RLIKE is specified, returns NULL if any argument is NULL.

# Usage Notes

- The function implicitly anchors a pattern at both ends (for example, `''` automatically becomes `'^$'`, and `'ABC'`
  automatically becomes `'^ABC$'`). For example, to match any string starting with `ABC`, the pattern is `'ABC.*'`.
- The backslash character (`\`) is the escape character. For more information, see [Specifying regular expressions in single-quoted string constants](/sql-reference/functions-regexp#label-regexp-escape-character-caveats).
- For more usage notes, see the [General usage notes](/sql-reference/functions-regexp#label-regexp-general-usage-notes) for regular expression functions.

## Collation Details

Arguments with collation specifications currently aren’t supported.

## Examples

Run the following commands to set up the data for the examples in this topic:

Copy code

```
CREATE OR REPLACE TABLE rlike_ex(city VARCHAR(20));
INSERT INTO rlike_ex VALUES ('Sacramento'), ('San Francisco'), ('San Jose'), (null);
```

### Examples that use the first syntax

The following examples perform case-insensitive pattern matching with wildcards:

Copy code

```
SELECT * FROM rlike_ex WHERE RLIKE(city, 'san.*', 'i');
```

```
+---------------+
| CITY          |
|---------------|
| San Francisco |
| San Jose      |
+---------------+
```

Copy code

```
SELECT * FROM rlike_ex WHERE NOT RLIKE(city, 'san.*', 'i');
```

```
+------------+
| CITY       |
|------------|
| Sacramento |
+------------+
```

The following examples determine if a string matches the format of a phone number and an email address.
In these examples, the regular expressions are specified in [dollar-quoted strings](/sql-reference/data-types-text#label-dollar-quoted-string-constants)
to avoid escaping the backslashes in the regular expression.

Copy code

```
SELECT RLIKE('800-456-7891',
             $$[2-9]\d{2}-\d{3}-\d{4}$$) AS matches_phone_number;
```

```
+----------------------+
| MATCHES_PHONE_NUMBER |
|----------------------|
| True                 |
+----------------------+
```

Copy code

```
SELECT RLIKE('jsmith@email.com',
             $$\w+@[a-zA-Z_]+\.[a-zA-Z]{2,3}$$) AS matches_email_address;
```

```
+-----------------------+
| MATCHES_EMAIL_ADDRESS |
|-----------------------|
| True                  |
+-----------------------+
```

The following examples perform the same matches but use
[single-quoted string constants](/sql-reference/data-types-text#label-single-quoted-string-constants) to specify the regular expressions.

Because the example uses single-quoted string constants,
[each backslash must be escaped with another backslash](/sql-reference/functions-regexp#label-regexp-escape-character-caveats).

Copy code

```
SELECT RLIKE('800-456-7891',
             '[2-9]\\d{2}-\\d{3}-\\d{4}') AS matches_phone_number;
```

```
+----------------------+
| MATCHES_PHONE_NUMBER |
|----------------------|
| True                 |
+----------------------+
```

Copy code

```
SELECT RLIKE('jsmith@email.com',
             '\\w+@[a-zA-Z_]+\\.[a-zA-Z]{2,3}') AS matches_email_address;
```

```
+-----------------------+
| MATCHES_EMAIL_ADDRESS |
|-----------------------|
| True                  |
+-----------------------+
```

Alternatively, rewrite the statements and avoid sequences that rely on the backslash character.

Copy code

```
SELECT RLIKE('800-456-7891',
             '[2-9][0-9]{2}-[0-9]{3}-[0-9]{4}') AS matches_phone_number;
```

```
+----------------------+
| MATCHES_PHONE_NUMBER |
|----------------------|
| True                 |
+----------------------+
```

Copy code

```
SELECT RLIKE('jsmith@email.com',
             '[a-zA-Z_]+@[a-zA-Z_]+\\.[a-zA-Z]{2,3}') AS matches_email_address;
```

```
+-----------------------+
| MATCHES_EMAIL_ADDRESS |
|-----------------------|
| True                  |
+-----------------------+
```

### Examples that use the second syntax

The following example performs case-insensitive pattern matching with wildcards:

Copy code

```
SELECT * FROM rlike_ex WHERE city RLIKE 'San.* [fF].*';
```

```
+---------------+
| CITY          |
|---------------|
| San Francisco |
+---------------+
```

### Additional examples

For additional examples of regular expressions, see [[ NOT ] REGEXP](/sql-reference/functions/regexp).
