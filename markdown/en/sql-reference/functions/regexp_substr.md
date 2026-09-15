Categories:
:   [String functions (regular expressions)](/sql-reference/functions-regexp)

# REGEXP\_SUBSTR

Returns the substring that matches a [regular expression](/sql-reference/functions-regexp)
within a string.

## Syntax

Copy code

```
REGEXP_SUBSTR( <subject> ,
               <pattern>
                 [ , <position>
                   [ , <occurrence>
                     [ , <regex_parameters>
                       [ , <group_num> ]
                     ]
                   ]
                 ]
)
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

`regex_parameters`
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
> By default, REGEXP\_SUBSTR returns the entire matching part of the subject.
> However, if the `e` (for “extract”) parameter is specified, REGEXP\_SUBSTR returns the
> part of the subject that matches the first group in the pattern.
> If `e` is specified but a `group_num` is not also specified, then the `group_num`
> defaults to 1 (the first group). If there is no sub-expression in the pattern, REGEXP\_SUBSTR behaves as
> if `e` was not set. For examples that use `e`, see [Examples](#examples) in this topic.

`group_num`
:   Specifies which group to extract. Groups are specified by using parentheses in
    the regular expression.

    If a `group_num` is specified, Snowflake allows extraction even if the `'e'` option was not
    also specified. The `'e'` is implied.

    Snowflake supports up to 1024 groups.

    For examples that use `group_num`, see the [Examples](#examples) in this topic.

## Returns

The function returns a value of type VARCHAR that is the matching substring. When the
[2026\_04 BCR bundle](/release-notes/bcr-bundles/2026_04/bcr-2314) is enabled and
the subject is collated, the subject’s collation propagates to the return value; apply
`COLLATE ''` to the subject to get an uncollated result.

The function returns NULL in the following cases:

- No match is found.
- Any argument is NULL.

## Usage notes

For additional information on using regular expressions, see [String functions (regular expressions)](/sql-reference/functions-regexp).

## Collation details

When the [2026\_04 BCR bundle](/release-notes/bcr-bundles/2026_04/bcr-2314)
is enabled, the function accepts arguments with a collation specification. The
collation has no effect on pattern matching: matching is always case-sensitive
unless you pass the `i` flag in the `parameters` argument.

## Examples

The documentation of the [REGEXP\_INSTR](/sql-reference/functions/regexp_instr) function contains many examples that use both REGEXP\_SUBSTR and
REGEXP\_INSTR. You might want to look at those examples, too.

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

The following examples call the REGEXP\_SUBSTR function:

- [Calling the REGEXP\_SUBSTR function in a SELECT list](#label-regexp-substr-examples-select-list)
- [Calling the REGEXP\_SUBSTR function in a WHERE clause](#label-regexp-substr-examples-where-clause)

### Calling the REGEXP\_SUBSTR function in a SELECT list

Call the REGEXP\_SUBSTR function in a SELECT list to extract or display values that match a pattern.

This example looks for first occurrence of the word `the`, followed by one or more non-word characters — for example,
the whitespace separating words — followed by one or more word characters.

“Word characters” include not only the letters a-z and A-Z, but also the
underscore (“\_”) and the decimal digits 0-9, but not whitespace, punctuation, and so on.

Copy code

```
SELECT id,
       REGEXP_SUBSTR(string1, 'the\\W+\\w+') AS result
  FROM demo2
  ORDER BY id;
```

```
+----+--------------+
| ID | RESULT       |
|----+--------------|
|  2 | the best     |
|  3 | the   string |
|  4 | NULL         |
+----+--------------+
```

Starting from position 1 of the string, look for the second occurrence of the word `the`,
followed by one or more non-word characters, followed by one or more word characters.

Copy code

```
SELECT id,
       REGEXP_SUBSTR(string1, 'the\\W+\\w+', 1, 2) AS result
  FROM demo2
  ORDER BY id;
```

```
+----+-------------+
| ID | RESULT      |
|----+-------------|
|  2 | the worst   |
|  3 | the   extra |
|  4 | NULL        |
+----+-------------+
```

Starting from position 1 of the string, look for the second occurrence of the word `the`,
followed by one or more non-word characters, followed by one or more word characters.

Rather than returning the entire match, return only the “group” (for example, the portion of the substring that matches the
part of the regular expression in parentheses). In this case, the returned value should be the word after “the”.

Copy code

```
SELECT id,
       REGEXP_SUBSTR(string1, 'the\\W+(\\w+)', 1, 2, 'e', 1) AS result
  FROM demo2
  ORDER BY id;
```

```
+----+--------+
| ID | RESULT |
|----+--------|
|  2 | worst  |
|  3 | extra  |
|  4 | NULL   |
+----+--------+
```

This example shows how to retrieve the second word from the first, second, and third matches of
a two-word pattern in which the first word is `A`. This example also shows that trying to
go beyond the last pattern causes Snowflake to return NULL.

First, create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE test_regexp_substr (string1 VARCHAR);;
INSERT INTO test_regexp_substr (string1) VALUES ('A MAN A PLAN A CANAL');
```

Run the query:

Copy code

```
SELECT REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 1, 'e', 1) AS result1,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 2, 'e', 1) AS result2,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 3, 'e', 1) AS result3,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w+)', 1, 4, 'e', 1) AS result4
  FROM test_regexp_substr;
```

```
+---------+---------+---------+---------+
| RESULT1 | RESULT2 | RESULT3 | RESULT4 |
|---------+---------+---------+---------|
| MAN     | PLAN    | CANAL   | NULL    |
+---------+---------+---------+---------+
```

This example shows how to retrieve the first, second, and third groups within the first occurrence of the pattern.
In this case, the returned values are the individual letters of the word `MAN`.

Copy code

```
SELECT REGEXP_SUBSTR(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 1) AS result1,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 2) AS result2,
       REGEXP_SUBSTR(string1, 'A\\W+(\\w)(\\w)(\\w)', 1, 1, 'e', 3) AS result3
  FROM test_regexp_substr;
```

```
+---------+---------+---------+
| RESULT1 | RESULT2 | RESULT3 |
|---------+---------+---------|
| M       | A       | N       |
+---------+---------+---------+
```

Here are some additional examples.

Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE message(body VARCHAR(255));

INSERT INTO message VALUES
  ('Hellooo World'),
  ('How are you doing today?'),
  ('the quick brown fox jumps over the lazy dog'),
  ('PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS');
```

Return the first match that contains a lowercase `o` by matching a word boundary (`\b`),
followed by zero or more word characters (`\S`), the letter `o`, and then zero or more
word characters until the next word boundary:

Copy code

```
SELECT body,
       REGEXP_SUBSTR(body, '\\b\\S*o\\S*\\b') AS result
  FROM message;
```

```
+---------------------------------------------+---------+
| BODY                                        | RESULT  |
|---------------------------------------------+---------|
| Hellooo World                               | Hellooo |
| How are you doing today?                    | How     |
| the quick brown fox jumps over the lazy dog | brown   |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | NULL    |
+---------------------------------------------+---------+
```

Return the first match that contains a lowercase `o`, starting at the third character
in the subject:

Copy code

```
SELECT body,
       REGEXP_SUBSTR(body, '\\b\\S*o\\S*\\b', 3) AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               | llooo  |
| How are you doing today?                    | you    |
| the quick brown fox jumps over the lazy dog | brown  |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | NULL   |
+---------------------------------------------+--------+
```

Return the third match that contains a lowercase `o`, starting at the third character
in the subject:

Copy code

```
SELECT body,
       REGEXP_SUBSTR(body, '\\b\\S*o\\S*\\b', 3, 3) AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               | NULL   |
| How are you doing today?                    | today  |
| the quick brown fox jumps over the lazy dog | over   |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | NULL   |
+---------------------------------------------+--------+
```

Return the third match that contains a lowercase `o`, starting at the third character in
the subject, with case-insensitive matching:

Copy code

```
SELECT body,
       REGEXP_SUBSTR(body, '\\b\\S*o\\S*\\b', 3, 3, 'i') AS result
  FROM message;
```

```
+---------------------------------------------+--------+
| BODY                                        | RESULT |
|---------------------------------------------+--------|
| Hellooo World                               | NULL   |
| How are you doing today?                    | today  |
| the quick brown fox jumps over the lazy dog | over   |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | LIQUOR |
+---------------------------------------------+--------+
```

This example shows that you can explicitly omit any regular expression parameters by specifying empty string.

Copy code

```
SELECT body,
       REGEXP_SUBSTR(body, '(H\\S*o\\S*\\b).*', 1, 1, '') AS result
  FROM message;
```

```
+---------------------------------------------+--------------------------+
| BODY                                        | RESULT                   |
|---------------------------------------------+--------------------------|
| Hellooo World                               | Hellooo World            |
| How are you doing today?                    | How are you doing today? |
| the quick brown fox jumps over the lazy dog | NULL                     |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | NULL                     |
+---------------------------------------------+--------------------------+
```

The following example illustrates overlapping occurrences. First, create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE overlap (
  id NUMBER,
  a STRING);

INSERT INTO overlap VALUES (1, ',abc,def,ghi,jkl,');
INSERT INTO overlap VALUES (2, ',abc,,def,,ghi,,jkl,');

SELECT * FROM overlap;
```

```
+----+----------------------+
| ID | A                    |
|----+----------------------|
|  1 | ,abc,def,ghi,jkl,    |
|  2 | ,abc,,def,,ghi,,jkl, |
+----+----------------------+
```

Run a query that finds the second occurrence of the following pattern in each row: a punctuation mark
followed by digits and letters, followed by a punctuation mark.

Copy code

```
SELECT id,
       REGEXP_SUBSTR(a,'[[:punct:]][[:alnum:]]+[[:punct:]]', 1, 2) AS result
  FROM overlap;
```

```
+----+--------+
| ID | RESULT |
|----+--------|
|  1 | ,ghi,  |
|  2 | ,def,  |
+----+--------+
```

The following example creates a JSON object from an Apache HTTP Server access log using pattern matching and concatenation.
First, create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE test_regexp_log (logs VARCHAR);

INSERT INTO test_regexp_log (logs) VALUES
  ('127.0.0.1 - - [10/Jan/2018:16:55:36 -0800] "GET / HTTP/1.0" 200 2216'),
  ('192.168.2.20 - - [14/Feb/2018:10:27:10 -0800] "GET /cgi-bin/try/ HTTP/1.0" 200 3395');

SELECT * from test_regexp_log
```

```
+-------------------------------------------------------------------------------------+
| LOGS                                                                                |
|-------------------------------------------------------------------------------------|
| 127.0.0.1 - - [10/Jan/2018:16:55:36 -0800] "GET / HTTP/1.0" 200 2216                |
| 192.168.2.20 - - [14/Feb/2018:10:27:10 -0800] "GET /cgi-bin/try/ HTTP/1.0" 200 3395 |
+-------------------------------------------------------------------------------------+
```

Run a query:

Copy code

```
SELECT '{ "ip_addr":"'
       || REGEXP_SUBSTR (logs,'\\b\\d{1,3}\.\\d{1,3}\.\\d{1,3}\.\\d{1,3}\\b')
       || '", "date":"'
       || REGEXP_SUBSTR (logs,'([\\w:\/]+\\s[+\-]\\d{4})')
       || '", "request":"'
       || REGEXP_SUBSTR (logs,'\"((\\S+) (\\S+) (\\S+))\"', 1, 1, 'e')
       || '", "status":"'
       || REGEXP_SUBSTR (logs,'(\\d{3}) \\d+', 1, 1, 'e')
       || '", "size":"'
       || REGEXP_SUBSTR (logs,'\\d{3} (\\d+)', 1, 1, 'e')
       || '"}' as Apache_HTTP_Server_Access
  FROM test_regexp_log;
```

```
+-----------------------------------------------------------------------------------------------------------------------------------------+
| APACHE_HTTP_SERVER_ACCESS                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------------------------------|
| { "ip_addr":"127.0.0.1", "date":"10/Jan/2018:16:55:36 -0800", "request":"GET / HTTP/1.0", "status":"200", "size":"2216"}                |
| { "ip_addr":"192.168.2.20", "date":"14/Feb/2018:10:27:10 -0800", "request":"GET /cgi-bin/try/ HTTP/1.0", "status":"200", "size":"3395"} |
+-----------------------------------------------------------------------------------------------------------------------------------------+
```

### Calling the REGEXP\_SUBSTR function in a WHERE clause

Call the REGEXP\_SUBSTR function in a WHERE clause to filter for rows that contain values that match a pattern.
By using the function, you can avoid multiple OR conditions.

The following example queries the `demo2` table you created previously to return rows that include either
the string `best` or the string `thespian`. Add `IS NOT NULL` to the condition to return rows that
match the pattern. That is, the rows where the REGEXP\_SUBSTR function didn’t return `NULL`:

Copy code

```
SELECT id, string1
  FROM demo2
  WHERE REGEXP_SUBSTR(string1, '(best|thespian)') IS NOT NULL;
```

```
+----+------------------------------------------------------+
| ID | STRING1                                              |
|----+------------------------------------------------------|
|  2 | It was the best of times, it was the worst of times. |
|  4 | A thespian theater is nearby.                        |
+----+------------------------------------------------------+
```

You can use AND conditions to find rows that match multiple patterns. For example, the following query returns
rows that include either the string `best` or the string `thespian` and start with the string `It`:

Copy code

```
SELECT id, string1
  FROM demo2
  WHERE REGEXP_SUBSTR(string1, '(best|thespian)') IS NOT NULL
    AND REGEXP_SUBSTR(string1, '^It') IS NOT NULL;
```

```
+----+------------------------------------------------------
| ID | STRING1                                              |
|----+------------------------------------------------------|
|  2 | It was the best of times, it was the worst of times. |
+----+------------------------------------------------------+
```
