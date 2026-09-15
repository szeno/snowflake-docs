Categories:
:   [String functions (regular expressions)](/sql-reference/functions-regexp)

# REGEXP\_REPLACE

Returns the subject with the specified pattern — or all occurrences of the pattern — either removed
or replaced by a replacement string.

## Syntax

Copy code

```
 REGEXP_REPLACE( <subject> ,
                 <pattern>
                   [ , <replacement>
                     [ , <position>
                       [ , <occurrence>
                         [ , <parameters> ]
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

`replacement`
:   String that replaces the substrings matched by the pattern. If an empty string is specified, the function removes all matched patterns and returns the resulting string.

    Default: `''` (empty string).

`position`
:   Number of characters from the beginning of the string where the function starts searching for matches.
    The value must be a positive integer.

    Default: `1` (the search for a match starts at the first character on the left)

`occurrence`
:   Specifies which occurrence of the pattern to replace. If `0` is specified, all occurrences are replaced.

    Default: `0` (all occurrences)

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

Returns a value of type VARCHAR. When the [2026\_04 BCR bundle](/release-notes/bcr-bundles/2026_04/bcr-2314)
is enabled and the subject is collated, the subject’s collation propagates to the return
value; apply `COLLATE ''` to the subject to get an uncollated result.

If no matches are found, returns the original subject.

Returns NULL if any argument is NULL.

## Usage notes

- The replacement string can contain backreferences to capture groups; for example, sub-expressions of the pattern. A capture group is a regular expression that is enclosed within parentheses (`( )`). The maximum number of capture groups is nine.

  Backreferences match expressions inside a capture group. Backreferences have the form `n` where `n` is a value from 0 to 9, inclusive, which refers to the matching instance of the capture group. For more information, see [Examples](#examples) (in this topic).
- Parentheses (`( )`) and square brackets (`[ ]`) currently must be double-escaped to parse them as literal strings.

  The example below shows how to remove parentheses:

  Copy code

  ```
  SELECT REGEXP_REPLACE('Customers - (NY)','\\(|\\)','') AS customers;
  ```

  ```
  +----------------+
  | CUSTOMERS      |
  |----------------|
  | Customers - NY |
  +----------------+
  ```
- For additional usage notes, see the [General usage notes](/sql-reference/functions-regexp#label-regexp-general-usage-notes) for regular expression functions.

## Collation details

When the [2026\_04 BCR bundle](/release-notes/bcr-bundles/2026_04/bcr-2314)
is enabled, the function accepts arguments with a collation specification. The
collation has no effect on pattern matching: matching is always case-sensitive
unless you pass the `i` flag in the `parameters` argument.

## Examples

The following example replaces all spaces in the string with nothing (that is, all spaces are removed):

Copy code

```
SELECT REGEXP_REPLACE('It was the best of times, it was the worst of times',
                      '( ){1,}',
                      '') AS result;
```

```
+------------------------------------------+
| RESULT                                   |
|------------------------------------------|
| Itwasthebestoftimes,itwastheworstoftimes |
+------------------------------------------+
```

The following example matches the string `times` and replaces it with the string `days`. Matching begins at the first
character in the string and replaces the second occurrence of the substring:

Copy code

```
SELECT REGEXP_REPLACE('It was the best of times, it was the worst of times',
                      'times',
                      'days',
                      1,
                      2) AS result;
```

```
+----------------------------------------------------+
| RESULT                                             |
|----------------------------------------------------|
| It was the best of times, it was the worst of days |
+----------------------------------------------------+
```

The following example uses backreferences to rearrange the string `firstname middlename lastname` as
`lastname, firstname middlename` and insert a comma between `lastname` and `firstname`:

Copy code

```
SELECT REGEXP_REPLACE('firstname middlename lastname',
                      '(.*) (.*) (.*)',
                      '\\3, \\1 \\2') AS name_sort;
```

```
+--------------------------------+
| NAME_SORT                      |
|--------------------------------|
| lastname, firstname middlename |
+--------------------------------+
```

The remaining examples use the data in the following table:

Copy code

```
CREATE OR REPLACE TABLE regexp_replace_demo(body VARCHAR(255));

INSERT INTO regexp_replace_demo values
  ('Hellooo World'),
  ('How are you doing today?'),
  ('the quick brown fox jumps over the lazy dog'),
  ('PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS');
```

The following example inserts the character `*` between every character of the subject, including the beginning and the end,
using an empty group (`()`), which finds a match between any two characters:

Copy code

```
SELECT body,
       REGEXP_REPLACE(body, '()', '*') AS replaced
  FROM regexp_replace_demo;
```

```
+---------------------------------------------+-----------------------------------------------------------------------------------------+
| BODY                                        | REPLACED                                                                                |
|---------------------------------------------+-----------------------------------------------------------------------------------------|
| Hellooo World                               | *H*e*l*l*o*o*o* *W*o*r*l*d*                                                             |
| How are you doing today?                    | *H*o*w* *a*r*e* *y*o*u* *d*o*i*n*g* *t*o*d*a*y*?*                                       |
| the quick brown fox jumps over the lazy dog | *t*h*e* *q*u*i*c*k* *b*r*o*w*n* *f*o*x* *j*u*m*p*s* *o*v*e*r* *t*h*e* *l*a*z*y* *d*o*g* |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | *P*A*C*K* *M*Y* *B*O*X* *W*I*T*H* *F*I*V*E* *D*O*Z*E*N* *L*I*Q*U*O*R* *J*U*G*S*         |
+---------------------------------------------+-----------------------------------------------------------------------------------------+
```

The following example removes all of the vowels by replacing them with nothing, regardless of their order or case:

Copy code

```
SELECT body,
       REGEXP_REPLACE(body, '[aeiou]', '', 1, 0, 'i') AS replaced
  FROM regexp_replace_demo;
```

```
+---------------------------------------------+----------------------------------+
| BODY                                        | REPLACED                         |
|---------------------------------------------+----------------------------------|
| Hellooo World                               | Hll Wrld                         |
| How are you doing today?                    | Hw r y dng tdy?                  |
| the quick brown fox jumps over the lazy dog | th qck brwn fx jmps vr th lzy dg |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PCK MY BX WTH FV DZN LQR JGS     |
+---------------------------------------------+----------------------------------+
```

The following example removes all words that contain the lowercase letter `o` from the subject by matching
a word boundary (`\b`), followed by zero or more word characters (`\S`), the letter `o`, and then zero or more
word characters until the next word boundary:

Copy code

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b') AS replaced
  FROM regexp_replace_demo;
```

```
+---------------------------------------------+-----------------------------------------+
| BODY                                        | REPLACED                                |
|---------------------------------------------+-----------------------------------------|
| Hellooo World                               |                                         |
| How are you doing today?                    |  are   ?                                |
| the quick brown fox jumps over the lazy dog | the quick   jumps  the lazy             |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS |
+---------------------------------------------+-----------------------------------------+
```

The following example replaces all words that contain the lowercase letter `o`, swapping
the letters in front of and behind the first instance of `o`, and replacing the `o` with the character
sequence `@@`:

Copy code

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1') AS replaced
  FROM regexp_replace_demo;
```

```
+---------------------------------------------+-------------------------------------------------+
| BODY                                        | REPLACED                                        |
|---------------------------------------------+-------------------------------------------------|
| Hellooo World                               | @@Helloo rld@@W                                 |
| How are you doing today?                    | w@@H are u@@y ing@@d day@@t?                    |
| the quick brown fox jumps over the lazy dog | the quick wn@@br x@@f jumps ver@@ the lazy g@@d |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS         |
+---------------------------------------------+-------------------------------------------------+
```

The following example is the same as the previous example, but the replacement starts at position `3` in the subject:

Copy code

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1', 3) AS replaced
  FROM regexp_replace_demo;
```

```
+---------------------------------------------+-------------------------------------------------+
| BODY                                        | REPLACED                                        |
|---------------------------------------------+-------------------------------------------------|
| Hellooo World                               | He@@lloo rld@@W                                 |
| How are you doing today?                    | How are u@@y ing@@d day@@t?                     |
| the quick brown fox jumps over the lazy dog | the quick wn@@br x@@f jumps ver@@ the lazy g@@d |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS         |
+---------------------------------------------+-------------------------------------------------+
```

The following example is the same as the previous example, but only the third occurrence is replaced, starting at position
`3` in the subject:

Copy code

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1', 3, 3) AS replaced
  FROM regexp_replace_demo;
```

```
+---------------------------------------------+----------------------------------------------+
| BODY                                        | REPLACED                                     |
|---------------------------------------------+----------------------------------------------|
| Hellooo World                               | Hellooo World                                |
| How are you doing today?                    | How are you doing day@@t?                    |
| the quick brown fox jumps over the lazy dog | the quick brown fox jumps ver@@ the lazy dog |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS      |
+---------------------------------------------+----------------------------------------------+
```

The following example is the same as the previous example, but it uses case-insensitive matching:

Copy code

```
SELECT body,
       REGEXP_REPLACE(body, '\\b(\\S*)o(\\S*)\\b', '\\2@@\\1', 3, 3, 'i') AS replaced
  FROM regexp_replace_demo;
```

```
+---------------------------------------------+----------------------------------------------+
| BODY                                        | REPLACED                                     |
|---------------------------------------------+----------------------------------------------|
| Hellooo World                               | Hellooo World                                |
| How are you doing today?                    | How are you doing day@@t?                    |
| the quick brown fox jumps over the lazy dog | the quick brown fox jumps ver@@ the lazy dog |
| PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | PACK MY BOX WITH FIVE DOZEN R@@LIQU JUGS     |
+---------------------------------------------+----------------------------------------------+
```
