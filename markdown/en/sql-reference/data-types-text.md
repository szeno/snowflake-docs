# String & binary data types

This topic describes the string/text data types, including binary strings, supported in Snowflake, along with the supported formats for string constants/literals.

## Data types for text strings

Snowflake supports the following data types for text (that is, character) strings.

### VARCHAR

VARCHAR values hold Unicode UTF-8 characters.

Note

In some systems outside of Snowflake, data types such as CHAR and VARCHAR store ASCII, while data types such as NCHAR and
NVARCHAR store Unicode.

In Snowflake, VARCHAR and all other string data types store Unicode UTF-8 characters. There is no difference with respect to
Unicode handling between CHAR and NCHAR data types. Synonyms such as NCHAR are primarily for syntax compatibility when porting
DDL commands to Snowflake.

When you declare a column of type VARCHAR, you can specify an optional parameter `(N)`, which is the maximum number of
characters to store. For example:

Copy code

```
CREATE TABLE t1 (v VARCHAR(134217728));
```

If no length is specified, the default is 16777216.

Note

The 16777216 default applies to columns created through SQL DDL. Some clients create VARCHAR columns
at the maximum length instead. For example, when Snowpark infers a table’s schema (such as when you
save a DataFrame with an inferred schema), it creates string columns as `VARCHAR(134217728)`. In that
case, `INFORMATION_SCHEMA.COLUMNS` reports a `CHARACTER_MAXIMUM_LENGTH` of 134217728, not 16777216.

Although a VARCHAR value’s maximum length is specified in characters, a VARCHAR value is also limited to a maximum of
134217728 bytes (128 MB). The maximum number of Unicode characters that can be stored in a VARCHAR column is as follows:

Single-byte:
:   134217728

Multi-byte:
:   Between 67108864 (2 bytes per character) and 33554432 (4 bytes per character)

For example, if you declare a column as `VARCHAR(134217728)`, the column can hold a maximum of 67,108,864 2-byte Unicode characters,
even though you specified a maximum length of `134217728`.

When choosing the maximum length for a VARCHAR column, consider the following:

- **Storage:** A column consumes storage for only the amount of actual data stored. For example, a 1-character string in a
  `VARCHAR(134217728)` column only consumes a single character.
- **Performance:** There is no performance difference between using the full-length VARCHAR declaration `VARCHAR(134217728)` and a
  smaller length.

  In any relational database, SELECT statements in which a WHERE clause references VARCHAR columns or string columns aren’t
  as fast as SELECT statements filtered using a date or numeric column condition.
- **Tools for working with data:** Some BI/ETL tools define the maximum size of the VARCHAR data in storage or in memory. If you
  know the maximum size for a column, you can limit the size when you add the column.
- **Collation:** When you specify a [collation](/sql-reference/collation) for a VARCHAR column, the number of characters
  that are allowed varies, depending on the number of bytes each character takes and the collation specification of the column.

  When comparing values in a collated column,
  [Snowflake follows the Unicode Collation Algorithm (UCA)](/sql-reference/collation#label-collation-character-weights). This algorithm affects the
  maximum number of characters allowed. Currently, around 1.5 million to 8 million characters are allowed in a VARCHAR column
  that is defined with a maximum size and a collation specification.

  As an example, the following table shows how the maximum number of characters can vary for a `VARCHAR(134217728)` column, depending
  on the number of bytes per character and the collation specification used:

  | Number of bytes per character | Collation specification | Maximum number of characters allowed (approximate) |
  | --- | --- | --- |
  | 1 byte | `en-ci` or `en-ci-pi-ai` | Around 56 million characters |
  | 1 byte | `en` | Around 32 million characters |
  | 2 bytes | `en-ci-pi-ai` | Around 64 million characters |
  | 2 bytes | `en-ci` or `en-ci-pi` | Around 21.6 million characters |
  | 2 bytes | `en` | Around 12 million characters |

  Expand

  Show lessSee more

### CHAR, CHARACTER, NCHAR

Synonymous with VARCHAR, except that if the length is not specified, `CHAR(1)` is the default.

Note

Snowflake currently deviates from common CHAR semantics in that strings shorter than the maximum length are not space-padded at the end.

### STRING, TEXT, VARCHAR2, NVARCHAR, NVARCHAR2, CHAR VARYING, NCHAR VARYING

Synonymous with VARCHAR.

### String examples in table columns

Copy code

```
CREATE OR REPLACE TABLE test_text(
  vm VARCHAR(134217728),
  vd VARCHAR,
  v50 VARCHAR(50),
  cm CHAR(134217728),
  cd CHAR,
  c10 CHAR(10),
  sm STRING(134217728),
  sd STRING,
  s20 STRING(20),
  tm TEXT(134217728),
  td TEXT,
  t30 TEXT(30));

DESC TABLE test_text;
```

```
+------+--------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type               | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+--------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| VM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| VD   | VARCHAR(16777216)  | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| V50  | VARCHAR(50)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| CM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| CD   | VARCHAR(1)         | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| C10  | VARCHAR(10)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| SM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| SD   | VARCHAR(16777216)  | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| S20  | VARCHAR(20)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| TM   | VARCHAR(134217728) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| TD   | VARCHAR(16777216)  | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| T30  | VARCHAR(30)        | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+--------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

## Data types for binary strings

Snowflake supports the following data types for binary strings.

### BINARY

The maximum length is 64 MB (67,108,864 bytes). Unlike VARCHAR, the BINARY data type has no notion of Unicode characters,
so the length is always measured in terms of bytes.

BINARY values are limited to 64 MB so that they fit within 128 MB when converted to hexadecimal strings, for example using
`TO_CHAR(<binary_expression>, 'HEX')`.

When you declare a column of type BINARY, you can specify an optional parameter `(N)`, which is the maximum number of
bytes to store. For example:

Copy code

```
CREATE TABLE b1 (b BINARY(33554432));
```

If no length is specified, the default is 8388608.

### VARBINARY

VARBINARY is synonymous with BINARY.

### Internal representation

The BINARY data type holds a sequence of 8-bit bytes.

When Snowflake displays BINARY data values, Snowflake often represents each
byte as two hexadecimal characters. For example, the word `HELP` might be
displayed as `48454C50`, where `48` is the hexadecimal equivalent of
the ASCII (Unicode) letter `H`, `45` is the hexadecimal representation of
the letter `E`, and so on.

For more information about entering and displaying BINARY data, see
[Binary input and output](/sql-reference/binary-input-output).

### Binary examples in table columns

Copy code

```
CREATE OR REPLACE TABLE test_binary(
  bd BINARY,
  b100 BINARY(100),
  vbd VARBINARY);

DESC TABLE test_binary;
```

```
+------+-----------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type            | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+-----------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| BD   | BINARY(8388608) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| B100 | BINARY(100)     | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| VBD  | BINARY(8388608) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+-----------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

## String constants

*Constants* (also known as *literals*) refer to fixed data values. String constants in Snowflake must always be enclosed between
delimiter characters. Snowflake supports using either of the following to delimit string constants:

- [Single quotes](#label-single-quoted-string-constants)
- [Pairs of dollar signs](#label-dollar-quoted-string-constants)

### Single-quoted string constants

A string constant can be enclosed between single quote delimiters (for example, `'This is a string'`). To include
a single quote character within a string constant, type two adjacent single quotes (for example, `''`).

For example:

Copy code

```
SELECT 'Today''s sales projections', '-''''-';
```

```
+------------------------------+----------+
| 'TODAY''S SALES PROJECTIONS' | '-''''-' |
|------------------------------+----------|
| Today's sales projections    | -''-     |
+------------------------------+----------+
```

Note

Two single quotes is not the same as the double quote character (`"`), which is used (as needed) for delimiting object identifiers. For more information, see
[Identifier requirements](/sql-reference/identifiers-syntax).

#### Escape sequences in single-quoted string constants

To include a single quote or other special characters (for example, newlines) in a single-quoted string constant, you must escape these
characters by using *backslash escape sequences*. A backslash escape sequence is a sequence of characters that begins with a
backslash (`\`).

Note

If the string contains many single quotes, backslashes, or other special characters, you can use a
[dollar-quoted string constant](#label-dollar-quoted-string-constants) instead to avoid escaping these characters.

You can also use escape sequences to insert ASCII characters by specifying their
[code points](https://en.wikipedia.org/wiki/Code_point) (the numeric values that correspond to those characters) in octal or
hexadecimal. For example, in ASCII, the code point for the space character is 32, which is 20 in hexadecimal. To specify a space,
you can use the hexadecimal escape sequence `\x20`.

You can also use escape sequences to insert Unicode characters, for example `\u26c4`.

The following table lists the supported escape sequences in four categories: simple, octal, hexadecimal, and Unicode:

> | Escape sequence | Character represented |
> | --- | --- |
> | **Simple escape sequences** |  |
> | `\'` | A single quote (`'`) character. |
> | `\"` | A double quote (`"`) character. |
> | `\\` | A backslash (`\`) character. |
> | `\b` | A backspace character. |
> | `\f` | A formfeed character. |
> | `\n` | A newline (linefeed) character. |
> | `\r` | A carriage return character. |
> | `\t` | A tab character. |
> | `\0` | An ASCII NUL character. |
> | **Octal escape sequences** |  |
> | `\ooo` | ASCII character in octal notation (that is, where each `o` represents an octal digit). |
> | **Hexadecimal escape sequences** |  |
> | `\xhh` | ASCII character in hexadecimal notation (that is, where each `h` represents a hexadecimal digit). |
> | **Unicode escape sequences** |  |
> | `\uhhhh` | Unicode character in hexadecimal notation (that is, where each `h` represents a hexadecimal digit). The number of hexadecimal digits must be exactly four. |
>
> Expand
>
> Show lessSee more

As shown in the table above, if a string constant must include a backslash character (for example, `C:\` in a Windows path or `\d` in
a [regular expression](/sql-reference/functions-regexp#label-regexp-general-usage-notes)), you must escape the backslash with a second backslash. For
example, to include `\d` in a regular expression in a string constant, use `\\d`.

If a backslash is used in sequences other than the ones listed above, the backslash is ignored. For example, the
sequence of characters `'\z'` is interpreted as `'z'`.

The following example demonstrates how to use backslash escape sequences. This includes examples of specifying:

- A tab character.
- A newline.
- A backslash.
- The octal and hexadecimal escape sequences for an exclamation mark (code point 33, which is `\041` in octal and `\x21` in
  hexadecimal).
- The Unicode escape sequence for a small image of a snowman.
- Something that is not a valid escape sequence.

Copy code

```
SELECT $1, $2 FROM
  VALUES
    ('Tab','Hello\tWorld'),
    ('Newline','Hello\nWorld'),
    ('Backslash','C:\\user'),
    ('Octal','-\041-'),
    ('Hexadecimal','-\x21-'),
    ('Unicode','-\u26c4-'),
    ('Not an escape sequence', '\z');
```

```
+------------------------+---------------+
| $1                     | $2            |
|------------------------+---------------|
| Tab                    | Hello   World |
| Newline                | Hello         |
|                        | World         |
| Backslash              | C:\user       |
| Octal                  | -!-           |
| Hexadecimal            | -!-           |
| Unicode                | -⛄-          |
| Not an escape sequence | z             |
+------------------------+---------------+
```

### Dollar-quoted string constants

In some cases, you might need to specify a string constant that contains:

- Single quote characters.
- Backslash characters (for example, in a [regular expression](/sql-reference/functions-regexp)).
- Newline characters (for example, in the body of a stored procedure or function that you specify in
  [CREATE PROCEDURE](/sql-reference/sql/create-procedure) or [CREATE FUNCTION](/sql-reference/sql/create-function)).

In these cases, you can avoid [escaping these characters](#label-single-quoted-string-constants-escape-sequences) by using
a pair of dollar signs (`$$`) rather than a single quote (`'`) to delimit the beginning and ending of the string.

In a dollar-quoted string constant, you can include quotes, backslashes, newlines and any other special character (except for
double-dollar signs) without escaping those characters. The content of a dollar-quoted string constant is always interpreted
literally.

The following examples are equivalent ways of specifying string constants:

| Example using single quote delimiters | Example using double dollar sign delimiters |
| --- | --- |
| Copy code  ``` 'string with a \' character' ``` | Copy code  ``` $$string with a ' character$$ ``` |
| Copy code  ``` 'regular expression with \\ characters: \\d{2}-\\d{3}-\\d{4}' ``` | Copy code  ``` $$regular expression with \ characters: \d{2}-\d{3}-\d{4}$$ ``` |
| Copy code  ``` 'string with a newline\ncharacter' ``` | Copy code  ``` $$string with a newline character$$ ``` |

Expand

Show lessSee more

The following example uses a dollar-quoted string constant that contains newlines and several
[escape sequences](#label-single-quoted-string-constants-escape-sequences):

Copy code

```
SELECT $1, $2 FROM VALUES (
  'row1',
  $$a
                                  ' \ \t
                                  \x21 z $ $$);
```

```
+------+---------------------------------------------+
| $1   | $2                                          |
|------+---------------------------------------------|
| row1 | a                                           |
|      |                                   ' \ \t    |
|      |                                   \x21 z $  |
+------+---------------------------------------------+
```

In this example, the escape sequences are interpreted as their individual characters
(for example, a backslash followed by a `t`), rather than as escape sequences.
