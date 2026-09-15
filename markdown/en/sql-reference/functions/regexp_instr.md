Categories:
:   [String functions (regular expressions)](/sql-reference/functions-regexp)

# REGEXP\_INSTR

Returns the position of the specified occurrence of the regular expression pattern in the string subject.

See also [String functions (regular expressions)](/sql-reference/functions-regexp).

## Syntax

Copy code

```
REGEXP_INSTR( <subject> , <pattern> [ , <position> [ , <occurrence> [ , <option> [ , <regexp_parameters> [ , <group_num> ] ] ] ] ] )
```

## Arguments

**Required:**

`subject`
:   The string to search for matches.

`pattern`
:   Pattern to match.

    For guidelines on specifying patterns, see [String functions (regular expressions)](/sql-reference/functions-regexp).

**Optional:**

`position`
:   Number of characters from the beginning of the string where the function starts searching for matches.
    The value must be a positive integer.

    Default: `1` (the search for a match starts at the first character on the left)

`occurrence`
:   Specifies the first occurrence of the pattern from which to start returning matches.

    The function skips the first `occurrence - 1` matches. For example, if there are 5 matches and
    you specify `3` for the `occurrence` argument, the function ignores the first two matches and
    returns the third, fourth, and fifth matches.

    Default: `1`

`option`
:   Specifies whether to return the offset of the first character of the match (`0`) or the offset of the first character following the end of the match (`1`).

    Default: `0`

`regexp_parameters`
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
>
> Note
>
> By default, REGEXP\_INSTR returns the begin or end character offset for the entire matching part of the subject.
> However, if the `e` (for “extract”) parameter is specified, REGEXP\_INSTR returns the begin or end
> character offset for the part of the subject that matches the first sub-expression in the pattern.
> If `e` is specified but a `group_num` is not also specified, then the `group_num`
> defaults to 1 (the first group). If there is no sub-expression in the pattern, REGEXP\_INSTR behaves as
> if `e` was not set. For examples that use `e`, see [Examples](#examples) in this topic.

`group_num`
:   The `group_num` parameter specifies which group to extract. Groups are specified by using parentheses in
    the regular expression.

    If a `group_num` is specified, Snowflake allows extraction even if the `e` option was not
    also specified. The `e` option is implied.

    Snowflake supports up to 1024 groups.

    For examples that use `group_num`, see [Examples of capture groups](#label-regexp-instr-group-examples) in this topic.

## Returns

Returns a value of type NUMBER.

If no match is found, returns `0`.

## Usage notes

- Positions are 1-based, not 0-based. For example, the position of the letter “M” in “MAN” is 1, not 0.
- For additional usage notes, see the [General usage notes](/sql-reference/functions-regexp#label-regexp-general-usage-notes) for regular expression functions.

## Collation details

When the [2026\_04 BCR bundle](/release-notes/bcr-bundles/2026_04/bcr-2314)
is enabled, the function accepts arguments with a collation specification. The
collation has no effect on pattern matching: matching is always case-sensitive
unless you pass the `i` flag in the `parameters` argument.

## Examples

The following examples use the REGEXP\_INSTR function.

### Basic examples

Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE demo1 (id INT, string1 VARCHAR);
INSERT INTO demo1 (id, string1) VALUES
  (1, 'nevermore1, nevermore2, nevermore3.');
```

Search for a matching string. In this case, the string is `nevermore` followed by a single decimal digit
(for example, `nevermore1`). The example uses the [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr) function to show the matching
substring:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'nevermore\\d') AS substring,
       REGEXP_INSTR( string1, 'nevermore\\d') AS position
  FROM demo1
  ORDER BY id;
```

```
+----+-------------------------------------+------------+----------+
| ID | STRING1                             | SUBSTRING  | POSITION |
|----+-------------------------------------+------------+----------|
|  1 | nevermore1, nevermore2, nevermore3. | nevermore1 |        1 |
+----+-------------------------------------+------------+----------+
```

Search for a matching string, but starting at the fifth character in the string, rather than at the first character in the
string:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'nevermore\\d', 5) AS substring,
       REGEXP_INSTR( string1, 'nevermore\\d', 5) AS position
  FROM demo1
  ORDER BY id;
```

```
+----+-------------------------------------+------------+----------+
| ID | STRING1                             | SUBSTRING  | POSITION |
|----+-------------------------------------+------------+----------|
|  1 | nevermore1, nevermore2, nevermore3. | nevermore2 |       13 |
+----+-------------------------------------+------------+----------+
```

Search for a matching string, but look for the third match rather than the first match:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'nevermore\\d', 1, 3) AS substring,
       REGEXP_INSTR( string1, 'nevermore\\d', 1, 3) AS position
  FROM demo1
  ORDER BY id;
```

```
+----+-------------------------------------+------------+----------+
| ID | STRING1                             | SUBSTRING  | POSITION |
|----+-------------------------------------+------------+----------|
|  1 | nevermore1, nevermore2, nevermore3. | nevermore3 |       25 |
+----+-------------------------------------+------------+----------+
```

This query is nearly identical the previous query, but this one shows how to use the `option` argument to
indicate whether you want the position of the matching expression, or the position of the first character after the
matching expression:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'nevermore\\d', 1, 3) AS substring,
       REGEXP_INSTR( string1, 'nevermore\\d', 1, 3, 0) AS start_position,
       REGEXP_INSTR( string1, 'nevermore\\d', 1, 3, 1) AS after_position
  FROM demo1
  ORDER BY id;
```

```
+----+-------------------------------------+------------+----------------+----------------+
| ID | STRING1                             | SUBSTRING  | START_POSITION | AFTER_POSITION |
|----+-------------------------------------+------------+----------------+----------------|
|  1 | nevermore1, nevermore2, nevermore3. | nevermore3 |             25 |             35 |
+----+-------------------------------------+------------+----------------+----------------+
```

This query shows that if you search for an occurrence beyond the last actual occurrence, the position returned is 0:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'nevermore', 1, 4) AS substring,
       REGEXP_INSTR( string1, 'nevermore', 1, 4) AS position
  FROM demo1
  ORDER BY id;
```

```
+----+-------------------------------------+-----------+----------+
| ID | STRING1                             | SUBSTRING | POSITION |
|----+-------------------------------------+-----------+----------|
|  1 | nevermore1, nevermore2, nevermore3. | NULL      |        0 |
+----+-------------------------------------+-----------+----------+
```

### Examples of capture groups

This section shows how to use the “group” feature of regular expressions.

The first few examples in this section don’t use capture groups. The section starts with some simple examples,
then continues with examples that use capture groups.

These examples use the strings created below:

Copy code

```
CREATE OR REPLACE TABLE demo2 (id INT, string1 VARCHAR);

INSERT INTO demo2 (id, string1) VALUES
    (2, 'It was the best of times, it was the worst of times.'),
    (3, 'In    the   string   the   extra   spaces  are   redundant.'),
    (4, 'A thespian theater is nearby.');

SELECT * FROM demo2;
```

```
+----+-------------------------------------------------------------+
| ID | STRING1                                                     |
|----+-------------------------------------------------------------|
|  2 | It was the best of times, it was the worst of times.        |
|  3 | In    the   string   the   extra   spaces  are   redundant. |
|  4 | A thespian theater is nearby.                               |
+----+-------------------------------------------------------------+
```

The strings have the following characteristics:

- The string with an `id` of `2` has multiple occurrences of the word “the”.
- The string with an `id` of `3` has multiple occurrences of the word “the” with extra blank spaces
  between the words.
- The string with an `id` of `4` has the character sequence “the” inside multiple words (“thespian”
  and “theater”), but without the word “the” by itself.

This example looks for the first occurrence of the word `the`, followed by one or more non-word characters (for example,
the whitespace separating words), followed by one or more word characters.

“Word characters” include not only the letters a-z and A-Z, but also the
underscore (“\_”) and the decimal digits 0-9, but not whitespace, punctuation, and so on.

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'the\\W+\\w+') AS substring,
       REGEXP_INSTR(string1, 'the\\W+\\w+') AS position
  FROM demo2
  ORDER BY id;
```

```
+----+-------------------------------------------------------------+--------------+----------+
| ID | STRING1                                                     | SUBSTRING    | POSITION |
|----+-------------------------------------------------------------+--------------+----------|
|  2 | It was the best of times, it was the worst of times.        | the best     |        8 |
|  3 | In    the   string   the   extra   spaces  are   redundant. | the   string |        7 |
|  4 | A thespian theater is nearby.                               | NULL         |        0 |
+----+-------------------------------------------------------------+--------------+----------+
```

Starting from position 1 of the string, look for the second occurrence of the word `the`,
followed by one or more non-word characters, followed by one or more word characters.

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'the\\W+\\w+', 1, 2) AS substring,
       REGEXP_INSTR(string1, 'the\\W+\\w+', 1, 2) AS position
  FROM demo2
  ORDER BY id;
```

```
+----+-------------------------------------------------------------+-------------+----------+
| ID | STRING1                                                     | SUBSTRING   | POSITION |
|----+-------------------------------------------------------------+-------------+----------|
|  2 | It was the best of times, it was the worst of times.        | the worst   |       34 |
|  3 | In    the   string   the   extra   spaces  are   redundant. | the   extra |       22 |
|  4 | A thespian theater is nearby.                               | NULL        |        0 |
+----+-------------------------------------------------------------+-------------+----------+
```

This example is similar to the preceding example, but adds capture groups. Rather than returning the position of the
entire match, this query returns the position of only the group, which is the portion of the substring that matches the
part of the regular expression in parentheses. In this case, the returned value is the position of the word
after the second occurrence of the word `the`.

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'the\\W+(\\w+)', 1, 2,    'e', 1) AS substring,
       REGEXP_INSTR( string1, 'the\\W+(\\w+)', 1, 2, 0, 'e', 1) AS position
  FROM demo2
  ORDER BY id;
```

```
+----+-------------------------------------------------------------+-----------+----------+
| ID | STRING1                                                     | SUBSTRING | POSITION |
|----+-------------------------------------------------------------+-----------+----------|
|  2 | It was the best of times, it was the worst of times.        | worst     |       38 |
|  3 | In    the   string   the   extra   spaces  are   redundant. | extra     |       28 |
|  4 | A thespian theater is nearby.                               | NULL      |        0 |
+----+-------------------------------------------------------------+-----------+----------+
```

If you specify the `'e'` (extract) parameter, but don’t specify the `group_num`, then the `group_num`
defaults to `1`:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'the\\W+(\\w+)', 1, 2,    'e') AS substring,
       REGEXP_INSTR( string1, 'the\\W+(\\w+)', 1, 2, 0, 'e') AS position
  FROM demo2
  ORDER BY id;
```

```
+----+-------------------------------------------------------------+-----------+----------+
| ID | STRING1                                                     | SUBSTRING | POSITION |
|----+-------------------------------------------------------------+-----------+----------|
|  2 | It was the best of times, it was the worst of times.        | worst     |       38 |
|  3 | In    the   string   the   extra   spaces  are   redundant. | extra     |       28 |
|  4 | A thespian theater is nearby.                               | NULL      |        0 |
+----+-------------------------------------------------------------+-----------+----------+
```

If you specify a `group_num`, Snowflake assumes that you want to extract, even if you didn’t specify
`'e'` (extract) as one of the parameters:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'the\\W+(\\w+)', 1, 2,    '', 1) AS substring,
       REGEXP_INSTR( string1, 'the\\W+(\\w+)', 1, 2, 0, '', 1) AS position
  FROM demo2
  ORDER BY id;
```

```
+----+-------------------------------------------------------------+-----------+----------+
| ID | STRING1                                                     | SUBSTRING | POSITION |
|----+-------------------------------------------------------------+-----------+----------|
|  2 | It was the best of times, it was the worst of times.        | worst     |       38 |
|  3 | In    the   string   the   extra   spaces  are   redundant. | extra     |       28 |
|  4 | A thespian theater is nearby.                               | NULL      |        0 |
+----+-------------------------------------------------------------+-----------+----------+
```

This example shows how to retrieve the position of second word from the first, second, and third matches of
a two-word pattern in which the first word is `A`. This also shows that trying to go beyond the last
pattern causes Snowflake to return 0.

Create a table and insert data:

Copy code

```
CREATE TABLE demo3 (id INT, string1 VARCHAR);
INSERT INTO demo3 (id, string1) VALUES
  (5, 'A MAN A PLAN A CANAL');
```

Run the query:

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 1,    'e', 1) AS substring1,
       REGEXP_INSTR( string1, 'A\\W+(\\w+)', 1, 1, 0, 'e', 1) AS position1,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 2,    'e', 1) AS substring2,
       REGEXP_INSTR( string1, 'A\\W+(\\w+)', 1, 2, 0, 'e', 1) AS position2,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 3,    'e', 1) AS substring3,
       REGEXP_INSTR( string1, 'A\\W+(\\w+)', 1, 3, 0, 'e', 1) AS position3,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 4,    'e', 1) AS substring4,
       REGEXP_INSTR( string1, 'A\\W+(\\w+)', 1, 4, 0, 'e', 1) AS position4
  FROM demo3;
```

```
+----+----------------------+------------+-----------+------------+-----------+------------+-----------+------------+-----------+
| ID | STRING1              | SUBSTRING1 | POSITION1 | SUBSTRING2 | POSITION2 | SUBSTRING3 | POSITION3 | SUBSTRING4 | POSITION4 |
|----+----------------------+------------+-----------+------------+-----------+------------+-----------+------------+-----------|
|  5 | A MAN A PLAN A CANAL | MAN        |         3 | PLAN       |         9 | CANAL      |        16 | NULL       |         0 |
+----+----------------------+------------+-----------+------------+-----------+------------+-----------+------------+-----------+
```

This example shows how to retrieve the position of first, second, and third groups within the first occurrence of the pattern.
In this case, the returned values are the positions of the individual letters of the word `MAN`.

Copy code

```
SELECT id,
       string1,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1,    'e', 1) AS substring1,
       REGEXP_INSTR( string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 0, 'e', 1) AS position1,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1,    'e', 2) AS substring2,
       REGEXP_INSTR( string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 0, 'e', 2) AS position2,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1,    'e', 3) AS substring3,
       REGEXP_INSTR( string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 0, 'e', 3) AS position3
  FROM demo3;
```

```
+----+----------------------+------------+-----------+------------+-----------+------------+-----------+
| ID | STRING1              | SUBSTRING1 | POSITION1 | SUBSTRING2 | POSITION2 | SUBSTRING3 | POSITION3 |
|----+----------------------+------------+-----------+------------+-----------+------------+-----------|
|  5 | A MAN A PLAN A CANAL | M          |         3 | A          |         4 | N          |         5 |
+----+----------------------+------------+-----------+------------+-----------+------------+-----------+
```

### Additional examples

The following example matches occurrences of the word `was`. Matching begins at the first character in the string
and returns the position in the string of the character following the first occurrence:

Copy code

```
SELECT REGEXP_INSTR('It was the best of times, it was the worst of times',
                    '\\bwas\\b',
                    1,
                    1) AS result;
```

```
+--------+
| RESULT |
|--------|
|      4 |
+--------+
```

The following example returns the offset of the first character of the part of the string that matches the
pattern. Matching begins at the first character in the string and returns the first occurrence of the pattern:

Copy code

```
SELECT REGEXP_INSTR('It was the best of times, it was the worst of times',
                    'the\\W+(\\w+)',
                    1,
                    1,
                    0) AS result;
```

```
+--------+
| RESULT |
|--------|
|      8 |
+--------+
```

The following example is the same as the previous example, but uses the `e` parameter to return the
character offset for the part of the subject that matches the first subexpression in the pattern (the
first set of word characters after `the`):

Copy code

```
SELECT REGEXP_INSTR('It was the best of times, it was the worst of times',
                    'the\\W+(\\w+)',
                    1,
                    1,
                    0,
                    'e') AS result;
```

```
+--------+
| RESULT |
|--------|
|     12 |
+--------+
```

The following example matches occurrences of words ending in `st` preceded by two or more alphabetic characters
(case-insensitive). Matching begins at the fifteenth character in the string and returns the position in the string of
the character following the first occurrence (the beginning of `worst`):

Copy code

```
SELECT REGEXP_INSTR('It was the best of times, it was the worst of times',
                    '[[:alpha:]]{2,}st',
                    15,
                    1) AS result;
```

```
+--------+
| RESULT |
|--------|
|     38 |
+--------+
```

To run the next set of examples, create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE message(body VARCHAR(255));
INSERT INTO message VALUES
  ('Hellooo World'),
  ('How are you doing today?'),
  ('the quick brown fox jumps over the lazy dog'),
  ('PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS');
```

Return the offset of the first character in the first match that contains a
lowercase `o`:

Copy code

```
SELECT body,
       REGEXP_INSTR(body, '\\b\\S*o\\S*\\b') AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               |      1 |
| How are you doing today?                    |      1 |
| the quick brown fox jumps over the lazy dog |     11 |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     |      0 |
+---------------------------------------------+--------+
```

Return the offset of the first character in the first match that contains a
lowercase `o`, starting at the third character in the subject:

Copy code

```
SELECT body,
       REGEXP_INSTR(body, '\\b\\S*o\\S*\\b', 3) AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               |      3 |
| How are you doing today?                    |      9 |
| the quick brown fox jumps over the lazy dog |     11 |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     |      0 |
+---------------------------------------------+--------+
```

Return the offset of the first character in the third match that contains a
lowercase `o`, starting at the third character in the subject:

Copy code

```
SELECT body, REGEXP_INSTR(body, '\\b\\S*o\\S*\\b', 3, 3) AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               |      0 |
| How are you doing today?                    |     19 |
| the quick brown fox jumps over the lazy dog |     27 |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     |      0 |
+---------------------------------------------+--------+
```

Return the offset of the last character in the third match that contains a
lowercase `o`, starting at the third character in the subject:

Copy code

```
SELECT body, REGEXP_INSTR(body, '\\b\\S*o\\S*\\b', 3, 3, 1) AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               |      0 |
| How are you doing today?                    |     24 |
| the quick brown fox jumps over the lazy dog |     31 |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     |      0 |
+---------------------------------------------+--------+
```

Return the offset of the last character in the third match that contains a
lowercase `o`, starting at the third character in the subject, with case-insensitive matching:

Copy code

```
SELECT body, REGEXP_INSTR(body, '\\b\\S*o\\S*\\b', 3, 3, 1, 'i') AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               |      0 |
| How are you doing today?                    |     24 |
| the quick brown fox jumps over the lazy dog |     31 |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     |     35 |
+---------------------------------------------+--------+
```
