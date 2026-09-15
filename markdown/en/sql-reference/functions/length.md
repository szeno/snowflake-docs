Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# LENGTH, LEN

Returns the length of an input [string or binary](/sql-reference/data-types-text) value. For strings,
the length is the number of characters, and UTF-8 characters are counted as a single character. For binary,
the length is the number of bytes.

## Syntax

Copy code

```
LENGTH( <expression> )

LEN( <expression> )
```

## Arguments

`expression`
:   The input expression must be a string or binary value.

## Returns

The returned data type is INTEGER (more precisely, NUMBER(18, 0)).

## Collation details

- No impact.
  In languages in which one character is one letter and vice versa, the LENGTH function behaves the same with and without
  collation.
- In languages where the alphabet contains digraphs or trigraphs (such as “Dz” and “Dzs” in Hungarian), each character in each digraph and trigraph is treated as an independent character, not as part of a single multi-character letter.
  For example, although Hungarian treats “dz” as a single letter, Snowflake returns `2` for `LENGTH(COLLATE('dz', 'hu'))`.

## Examples

Create a table and insert VARCHAR values:

Copy code

```
CREATE OR REPLACE TABLE length_function_demo (s VARCHAR);

INSERT INTO length_function_demo VALUES
  (''),
  ('Joyeux Noël'),
  ('Merry Christmas'),
  ('Veselé Vianoce'),
  ('Wesołych Świąt'),
  ('圣诞节快乐'),
  (NULL);
```

Query the table using the LENGTH function:

Copy code

```
SELECT s, LENGTH(s) FROM length_function_demo;
```

```
+-----------------+-----------+
| S               | LENGTH(S) |
|-----------------+-----------|
|                 |         0 |
| Joyeux Noël     |        11 |
| Merry Christmas |        15 |
| Veselé Vianoce  |        14 |
| Wesołych Świąt  |        14 |
| 圣诞节快乐        |         5 |
| NULL            |      NULL |
+-----------------+-----------+
```

For the next example, create a table and insert BINARY data:

Copy code

```
CREATE OR REPLACE TABLE binary_demo_table (
  v VARCHAR,
  b_hex BINARY,
  b_base64 BINARY,
  b_utf8 BINARY);

INSERT INTO binary_demo_table (v) VALUES ('hello');

UPDATE binary_demo_table SET
  b_hex    = TO_BINARY(HEX_ENCODE(v), 'HEX'),
  b_base64 = TO_BINARY(BASE64_ENCODE(v), 'BASE64'),
  b_utf8   = TO_BINARY(v, 'UTF-8');

SELECT * FROM binary_demo_table;
```

```
+-------+------------+------------+------------+
| V     | B_HEX      | B_BASE64   | B_UTF8     |
|-------+------------+------------+------------|
| hello | 68656C6C6F | 68656C6C6F | 68656C6C6F |
+-------+------------+------------+------------+
```

Query the table using the LENGTH function:

Copy code

```
SELECT v, LENGTH(v),
       TO_VARCHAR(b_hex, 'HEX') AS b_hex, LENGTH(b_hex),
       TO_VARCHAR(b_base64, 'BASE64') AS b_base64, LENGTH(b_base64),
       TO_VARCHAR(b_utf8, 'UTF-8') AS b_utf8, LENGTH(b_utf8)
  FROM binary_demo_table;
```

```
+-------+-----------+------------+---------------+----------+------------------+--------+----------------+
| V     | LENGTH(V) | B_HEX      | LENGTH(B_HEX) | B_BASE64 | LENGTH(B_BASE64) | B_UTF8 | LENGTH(B_UTF8) |
|-------+-----------+------------+---------------+----------+------------------+--------+----------------|
| hello |         5 | 68656C6C6F |             5 | aGVsbG8= |                5 | hello  |              5 |
+-------+-----------+------------+---------------+----------+------------------+--------+----------------+
```
