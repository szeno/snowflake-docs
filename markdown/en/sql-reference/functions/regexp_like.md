Categories:
:   [String functions (regular expressions)](/sql-reference/functions-regexp)

# REGEXP\_LIKE

Performs a comparison to determine whether a string matches a specified pattern. Both inputs
must be text expressions.

REGEXP\_LIKE is similar to the [LIKE](/sql-reference/functions/like) function, but with
[POSIX extended regular expressions](http://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended)
instead of SQL LIKE pattern syntax. REGEXP\_LIKE supports more complex matching conditions than LIKE.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

Aliases:
:   [RLIKE](/sql-reference/functions/rlike) (1st syntax)

## Syntax

Copy code

```
REGEXP_LIKE( <subject> , <pattern> [ , <parameters> ] )
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

# Returns

Returns a BOOLEAN value or NULL:

- Returns TRUE if there is a match.
- Returns FALSE if there isn’t a match.
- Returns NULL if any argument is NULL.

# Usage Notes

- The function implicitly anchors a pattern at both ends (for example, `''` automatically becomes `'^$'`, and `'ABC'`
  automatically becomes `'^ABC$'`). For example, to match any string starting with `ABC`, the pattern is `'ABC.*'`.
- The backslash character (`\`) is the escape character. For more information, see [Specifying regular expressions in single-quoted string constants](/sql-reference/functions-regexp#label-regexp-escape-character-caveats).
- For more usage notes, see the [General usage notes](/sql-reference/functions-regexp#label-regexp-general-usage-notes) for regular expression functions.

## Collation Details

Arguments with collation specifications currently aren’t supported.

## Examples

The following examples use the REGEXP\_LIKE function:

- [Run basic regular expression queries on strings](#label-regexp-like-example-strings)
- [Run regular expression queries on strings with special characters](#label-regexp-like-example-special-characters)

For additional examples of regular expressions, see [REGEXP](/sql-reference/functions/regexp).

### Run basic regular expression queries on strings

Create a table with names of cities:

Copy code

```
CREATE OR REPLACE TABLE cities(city VARCHAR(20));

INSERT INTO cities VALUES
  ('Sacramento'),
  ('San Francisco'),
  ('San Luis Obispo'),
  ('San Jose'),
  ('Santa Barbara'),
  ('Palo Alto'),
  (NULL);
```

You can use `.*` as a wildcard to match as many characters as possible. The following example matches the
pattern `Fran` anywhere in the string value:

Copy code

```
SELECT * FROM cities WHERE REGEXP_LIKE(city, '.*Fran.*');
```

```
+---------------+
| CITY          |
|---------------|
| San Francisco |
+---------------+
```

The following example uses the `i` parameter for case-insensitive matching:

Copy code

```
SELECT * FROM cities WHERE REGEXP_LIKE(city, '.*fran.*', 'i');
```

```
+---------------+
| CITY          |
|---------------|
| San Francisco |
+---------------+
```

To find a pattern that matches the beginning of a string value, run a query that uses a wildcard:

Copy code

```
SELECT * FROM cities WHERE REGEXP_LIKE(city, 'san.*', 'i');
```

```
+-----------------+
| CITY            |
|-----------------|
| San Francisco   |
| San Luis Obispo |
| San Jose        |
| Santa Barbara   |
+-----------------+
```

To run a case-sensitive query with a wildcard, omit the `i` parameter:

Copy code

```
SELECT * FROM cities WHERE REGEXP_LIKE(city, 'san.*');
```

```
+------+
| CITY |
|------|
+------+
```

You can use the `\w+` metacharacter to match one word and `\s` metacharacter to match one whitespace character, such
as a space or a tab. The following query searches for the values that include one word, followed by a whitespace
character, followed by one word:

Copy code

```
SELECT * FROM cities WHERE REGEXP_LIKE(city, '\\w+\\s\\w+');
```

```
+---------------+
| CITY          |
|---------------|
| San Francisco |
| San Jose      |
| Santa Barbara |
| Palo Alto     |
+---------------+
```

The output for the query doesn’t include `San Luis Obispo` because that value has three words with
a space between the first and second words instead of only two words with a space in between them.

In a regular expression, you can often use an uppercase metacharacter to negate the meaning of a lowercase metacharacter. For
example, run a query that searches for the values that don’t include a whitespace character between two words by using the
`\S` metacharacter:

Copy code

```
SELECT * FROM cities WHERE REGEXP_LIKE(city, '\\w+\\S\\w+');
```

```
+------------+
| CITY       |
|------------|
| Sacramento |
+------------+
```

### Run regular expression queries on strings with special characters

The examples in this section search for values with special characters, which are characters other than
a-z, A-Z, underscore (“\_”), or decimal digit.

To search for a metacharacter, escape the metacharacter. For more information, see
[Specifying regular expressions in single-quoted string constants](/sql-reference/functions-regexp#label-regexp-escape-character-caveats).

Create a table, and then insert some values with special characters:

Copy code

```
CREATE OR REPLACE TABLE regex_special_characters(v VARCHAR(20));

INSERT INTO regex_special_characters VALUES
  ('Snow'),
  ('Sn.ow'),
  ('Sn@ow'),
  ('Sn$ow'),
  ('Sn\\ow');
```

The first inserted value doesn’t contain special characters.

To show the data, query the table:

Copy code

```
SELECT * FROM regex_special_characters;
```

```
+-------+
| V     |
|-------|
| Snow  |
| Sn.ow |
| Sn@ow |
| Sn$ow |
| Sn\ow |
+-------+
```

You can search for any special character by using the `\W` Perl backslash-sequence, which searches
for characters that aren’t “word” characters. For example, the following query searches for the values
in the table that have special characters:

Copy code

```
SELECT *
  FROM regex_special_characters
  WHERE REGEXP_LIKE(v, '.*\\W.*');
```

```
+-------+
| V     |
|-------|
| Sn.ow |
| Sn@ow |
| Sn$ow |
| Sn\ow |
+-------+
```

To [search for metacharacters](/sql-reference/functions-regexp#label-regex-metacharacter) in a single-quoted string constant, you must
escape the metacharacter with two backslashes. For example, the following query searches for the values that
contain the `$` metacharacter:

Copy code

```
SELECT *
  FROM regex_special_characters
  WHERE REGEXP_LIKE(v, '.*\\$.*');
```

```
+-------+
| V     |
|-------|
| Sn$ow |
+-------+
```

If you search for a backslash, an additional backslash escape character is required. For example, the following
query searches for the values that contain the `\` or the `.` metacharacter:

Copy code

```
SELECT *
  FROM regex_special_characters
  WHERE REGEXP_LIKE(v, '.*(\\.|\\\\).*');
```

```
+-------+
| V     |
|-------|
| Sn.ow |
| Sn\ow |
+-------+
```
