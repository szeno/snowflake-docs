# String functions (regular expressions)

These string functions perform operations that match a regular expression (often referred to as a “regex”).

## List of regex functions

| Function | Notes |
| --- | --- |
| [[ NOT ] REGEXP](/sql-reference/functions/regexp) | Alias for RLIKE. |
| [REGEXP\_COUNT](/sql-reference/functions/regexp_count) |  |
| [REGEXP\_EXTRACT\_ALL](/sql-reference/functions/regexp_substr_all) | Alias for REGEXP\_SUBSTR\_ALL. |
| [REGEXP\_INSTR](/sql-reference/functions/regexp_instr) |  |
| [REGEXP\_LIKE](/sql-reference/functions/regexp_like) | Alias for RLIKE. |
| [REGEXP\_REPLACE](/sql-reference/functions/regexp_replace) |  |
| [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr) |  |
| [REGEXP\_SUBSTR\_ALL](/sql-reference/functions/regexp_substr_all) |  |
| [[ NOT ] RLIKE](/sql-reference/functions/rlike) |  |

Expand

Show lessSee more

## General usage notes

In these notes, “subject” refers to the string to operate on and “pattern” refers to the regular expression:

- The subject is typically a variable column, while the pattern is typically a constant, but this is not required; every argument
  to a regular expression function can be either a constant or variable.
- Patterns support most of the POSIX ERE (Extended Regular Expression) syntax. For details, see the
  [POSIX basic and extended](http://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended) section (in Wikipedia).

  One exception is that the regular expression functions don’t support non-greedy quantifiers, for example `*?`, `??`,
  and `+?`.
- Patterns also support the following Perl backslash-sequences:

  - `\d`: decimal digit (0-9).
  - `\D`: not a decimal digit.
  - `\s`: whitespace character.
  - `\S`: not a whitespace character.
  - `\w`: “word” character (a-z, A-Z, underscore (“\_”), or decimal digit).
  - `\W`: not a word character.
  - `\b`: word boundary.
  - `\B`: not a word boundary.

  For details, see the [Character classes](http://en.wikipedia.org/wiki/Regular_expression#Character_classes) section (in Wikipedia) or the
  [Backslash sequences](http://perldoc.perl.org/perlrecharclass.html#Backslash-sequences) section (in the Perl documentation).

  Note

  In [single-quoted string constants](/sql-reference/data-types-text#label-single-quoted-string-constants), you must escape the backslash character in
  the backslash-sequence. For example, to specify `\d`, use `\\d`. For details, see
  [Specifying regular expressions in single-quoted string constants](#label-regexp-escape-character-caveats) (in this topic).

  You do not need to escape backslashes if you are delimiting the string with
  [pairs of dollar signs ($$)](/sql-reference/data-types-text#label-dollar-quoted-string-constants) (rather than single quotes).
- By default, the POSIX wildcard character `.` (in the pattern) does not include newline characters `\n` (in the subject) as matches.

  To also match newline characters, either replace `.` with `(.|\n)` in the `pattern` argument, or use the `s` parameter in the `parameters` argument (described
  below).
- All the regular expression functions support Unicode. A single Unicode character always counts as one character (that is, the POSIX meta-character `.` matches exactly one Unicode character),
  regardless of the byte-length of the corresponding binary representation of that character. Also, for functions that take or return subject offsets, a single Unicode character counts as 1.

## Specifying the parameters for the regular expression

Most regular expression functions support an optional `parameters` argument. The `parameters` argument is a VARCHAR string that specifies the matching
behavior of the regular expression function. The following parameters are supported:

| Parameter | Description |
| --- | --- |
| `c` | Enables case-sensitive matching. |
| `i` | Enables case-insensitive matching. |
| `m` | Enables multi-line mode (that is, meta-characters `^` and `$` mark the beginning and end of any line of the subject). By default, multi-line mode is disabled (that is, `^` and `$` mark the beginning and end of the entire subject). |
| `e` | Extracts submatches; applies only to [REGEXP\_INSTR](/sql-reference/functions/regexp_instr), [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr), [REGEXP\_SUBSTR\_ALL](/sql-reference/functions/regexp_substr_all), and the aliases for these functions. |
| `s` | Enables the POSIX wildcard character `.` to match `\n`. By default, wildcard character matching is disabled. |

Expand

Show lessSee more

The default string is `c`, which specifies:

- Case-sensitive matching.
- Single-line mode.
- No submatch extraction, except for [REGEXP\_REPLACE](/sql-reference/functions/regexp_replace), which always uses submatch extraction.
- POSIX wildcard character `.` does not match `\n` newline characters.

When specifying multiple parameters, enter the string with no spaces or delimiters.
For example, `ims` specifies case-insensitive matching in multi-line mode with POSIX wildcard matching.

If both `c` and `i` are included in the `parameters` string, the one that occurs last in the string dictates whether the function performs case-sensitive or case-insensitive
matching. For example, `ci` specifies case-insensitive matching because the `i` occurs last in the string.

The following example shows how the results can be different for case-sensitive and case-insensitive matching.
The [REGEXP\_COUNT](/sql-reference/functions/regexp_count) function returns no matches for `snow` and `SNOW` for case-sensitive matching (`c` parameter,
the default) and one match for case-insensitive matching (`i` parameter):

Copy code

```
SELECT REGEXP_COUNT('snow', 'SNOW', 1, 'c') AS case_sensitive_matching,
       REGEXP_COUNT('snow', 'SNOW', 1, 'i') AS case_insensitive_matching;
```

```
+-------------------------+---------------------------+
| CASE_SENSITIVE_MATCHING | CASE_INSENSITIVE_MATCHING |
|-------------------------+---------------------------|
|                       0 |                         1 |
+-------------------------+---------------------------+
```

Use the [REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr) function with the `e` parameter to look for the word
`Release`, followed by one or more non-word characters, followed by one or more digits, and then return
the substring that matches the digits:

Copy code

```
SELECT REGEXP_SUBSTR('Release 24', 'Release\\W+(\\d+)', 1, 1, 'e') AS release_number;
```

```
+----------------+
| RELEASE_NUMBER |
|----------------|
| 24             |
+----------------+
```

For more examples that use parameters, see [REGEXP\_INSTR](/sql-reference/functions/regexp_instr), [REGEXP\_LIKE](/sql-reference/functions/regexp_like),
[REGEXP\_SUBSTR](/sql-reference/functions/regexp_substr), [REGEXP\_SUBSTR\_ALL](/sql-reference/functions/regexp_substr_all), and [[ NOT ] RLIKE](/sql-reference/functions/rlike).

## Matching characters that are metacharacters

In regular expressions, some characters are treated as metacharacters that have a specific meaning. For example:

- `.` is a
  [metacharacter that matches any single character](https://en.wikipedia.org/wiki/Regular_expression#POSIX_basic_and_extended).
- `*` is a [quantifier](https://en.wikipedia.org/wiki/Regular_expression#Basic_concepts) that matches zero or more instances
  of the preceding element. For example, `BA*` matches `B`, `BA`, `BAA`, and so on.
- `?` is a quantifier that matches zero or one instance of the preceding element.

To match the actual character (for example, an actual period, asterisk, or question mark), you must escape the metacharacter with a
backslash (for example, `\.`, `\*`, `\?`, and so on).

Note

If you are using the regular expression in a [single-quoted string constant](/sql-reference/data-types-text#label-single-quoted-string-constants),
you must escape the backslash with a second backslash (for example, `\\.`, `\\*`, `\\?`, and so on). For details, see
[Specifying regular expressions in single-quoted string constants](#label-regexp-escape-character-caveats)

For example, suppose that you need to find an open parenthesis (`(`) in a string. One way to specify this is to use a backslash
to escape the character in the pattern (for example, `\(`).

If you are specifying the pattern as a [single-quoted string constant](/sql-reference/data-types-text#label-single-quoted-string-constants), you must also
[escape that backslash with a second backslash](/sql-reference/data-types-text#label-single-quoted-string-constants-escape-sequences).

The following pattern matches a sequence of alphanumeric characters that appear inside parentheses (for example, `(NY)`):

Copy code

```
SELECT REGEXP_SUBSTR('Customers - (NY)','\\([[:alnum:]]+\\)') AS location;
```

```
+----------+
| LOCATION |
|----------|
| (NY)     |
+----------+
```

For additional examples, see [Example of using metacharacters in a single-quoted string constant](#label-regexp-escape-character-caveats-metacharacter).

Note that you do not need to escape the backslash character if you are using a
[dollar-quoted string constant](/sql-reference/data-types-text#label-dollar-quoted-string-constants):

Copy code

```
SELECT REGEXP_SUBSTR('Customers - (NY)',$$\([[:alnum:]]+\)$$) AS location;
```

```
+----------+
| LOCATION |
|----------|
| (NY)     |
+----------+
```

## Using backreferences

Snowflake does not support backreferences in regular expression patterns (known as “squares” in formal language theory); however, backreferences are supported in the replacement string of the
[REGEXP\_REPLACE](/sql-reference/functions/regexp_replace) function.

## Specifying an empty pattern

In most regexp functions, an empty pattern (that is, `''`) matches nothing, not even an empty subject.

The exceptions are [REGEXP\_LIKE](/sql-reference/functions/regexp_like) and its aliases [[ NOT ] REGEXP](/sql-reference/functions/regexp) and [[ NOT ] RLIKE](/sql-reference/functions/rlike),
in which the empty pattern matches the empty subject because the pattern is implicitly anchored at both ends
(that is, `''` automatically becomes `'^$'`).

An empty group (that is, subexpression `()`), matches the space in between characters, including the beginning and end of the subject.

## Specifying regular expressions in dollar-quoted string constants

If you are using a string constant to specify the regular expression for a function, you can use a
[dollar-quoted string constant](/sql-reference/data-types-text#label-dollar-quoted-string-constants) to avoid
[escaping the backslash characters in the regular expression](#label-regexp-escape-character-caveats). (If you are using
[single-quoted string constants](/sql-reference/data-types-text#label-single-quoted-string-constants), you need to escape the backslashes.)

The content of a dollar-quoted string constant is always interpreted literally.

For example, when escaping a [metacharacter](#label-regex-metacharacter), you only need to use a single backslash:

Copy code

```
SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, $$\?$$);
```

When using a [backreference](#label-regex-backreferences), you only need to use a single backslash:

Copy code

```
SELECT w2, REGEXP_REPLACE(w2, '(.old)', $$very \1$$)
  FROM wildcards
  ORDER BY w2;
```

## Specifying regular expressions in single-quoted string constants

If you are using a regular expression in a [single-quoted string constant](/sql-reference/data-types-text#label-single-quoted-string-constants), you must
escape any backslashes in [backslash-sequences](#label-regexp-general-usage-notes) with a second backslash.

Note

To avoid escaping backslashes in a regular expression, you can use a
[dollar-quoted string constant](#label-regexp-double-dollar-sign-strings), rather than a single-quoted string constant.

For example:

- If you are [escaping a metacharacter](#label-regex-metacharacter) with a backslash, you must escape the backslash with
  a second backslash. See [Example of using metacharacters in a single-quoted string constant](#label-regexp-escape-character-caveats-metacharacter).
- If you are using a [backslash-sequence](#label-regexp-general-usage-notes), you must escape the backslash in the sequence.
- If you are using a [backreference](#label-regex-backreferences), you must escape the backslash in the backreference.
  See [Example of using backreferences in a single-quoted string constant](#label-regexp-escape-character-caveats-backreference).

### Example of using metacharacters in a single-quoted string constant

This example uses the backslash as part of an escape sequence in a regular expression that searches for a question mark (`?`).

Create a table and insert a row that contains a single backslash in one column and a question mark in another column:

Copy code

```
CREATE OR REPLACE TABLE wildcards (w VARCHAR, w2 VARCHAR);
INSERT INTO wildcards (w, w2) VALUES ('\\', '?');
```

The following query searches for the question mark literal. The search uses a regular expression, and the question mark is a
meta-character in regular expressions, so the search must escape the question mark to treat it as a literal. Because the
backslash appears in a string literal, the backslash itself must also be escaped:

Copy code

```
SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, '\\?');
```

```
+----+
| W2 |
|----|
| ?  |
+----+
```

The following query makes it easier to see that the regular expression is composed of two characters (the backslash escape
character and the question mark):

Copy code

```
SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, '\\' || '?');
```

```
+----+
| W2 |
|----|
| ?  |
+----+
```

In the previous example, the extra backslash was needed only because the escape character was part of a string literal.
It was not needed for the regular expression itself. The following SELECT statement does not need to parse a string literal as
part of the SQL command string, and therefore does not need the extra escape character that the string literal needed:

Copy code

```
SELECT w, w2, w || w2 AS escape_sequence, w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, w || w2);
```

```
+---+----+-----------------+----+
| W | W2 | ESCAPE_SEQUENCE | W2 |
|---+----+-----------------+----|
| \ | ?  | \?              | ?  |
+---+----+-----------------+----+
```

### Example of using backreferences in a single-quoted string constant

If you use a [backreference](#label-regex-backreferences) (for example, `\1`) in a string literal, you must escape the backslash
that is a part of that backreference. For example, to specify the backreference `\1` in a replacement string literal of
[REGEXP\_REPLACE](/sql-reference/functions/regexp_replace), use `\\1`.

The following example uses the table created earlier. The SELECT uses a backreference to replace each occurrence of the regular
expression `.old` with a copy of the matched string preceded by the word “very”:

Copy code

```
INSERT INTO wildcards (w, w2) VALUES (NULL, 'When I am cold, I am bold.');
```

Copy code

```
SELECT w2, REGEXP_REPLACE(w2, '(.old)', 'very \\1')
  FROM wildcards
  ORDER BY w2;
```

```
+----------------------------+------------------------------------------+
| W2                         | REGEXP_REPLACE(W2, '(.OLD)', 'VERY \\1') |
|----------------------------+------------------------------------------|
| ?                          | ?                                        |
| When I am cold, I am bold. | When I am very cold, I am very bold.     |
+----------------------------+------------------------------------------+
```
