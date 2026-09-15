Categories:
:   [String & binary functions](/sql-reference/functions-string)

# SOUNDEX

Returns a string that contains a phonetic representation of the input string.

You can use this function to determine whether two strings (e.g. the family names `Levine` and `Lavine`, the words `to`
and `too`, etc.) have similar pronunciations in the English language.

This function uses the [Soundex phonetic algorithm](https://en.wikipedia.org/wiki/Soundex), which is described in [Soundex System](https://www.archives.gov/research/census/soundex). Note, however, that Snowflake
provides no special handling for surname prefixes (e.g. “Van”, “De”, “La”, etc.).

`SOUNDEX('Pfister')` returns `P236`. Because the first two letters (`P` and `f`) are adjacent and share the same
Soundex code number (`1`), the function ignores the Soundex code number for the second letter.

Some database systems (e.g. Teradata) use a variant that retains the Soundex code number for the second letter when the first and
second letters use the same number. For that variant, the string for `Pfister` is `P123` (not `P236`). To use that variant,
call the [SOUNDEX\_P123](/sql-reference/functions/soundex_p123) function instead.

See also:
:   [SOUNDEX\_P123](/sql-reference/functions/soundex_p123)

## Syntax

Copy code

```
SOUNDEX( <varchar_expr> )
```

## Arguments

`varchar_expr`
:   The string for which a representation of the pronunciation is returned. The string should use the Latin or Unicode character set.

## Returns

The returned value is a VARCHAR that contains the phonetic representation of the input string. In other words, the return value
is a string (not a sound) that represents the pronunciation (not the spelling) of the input string.

Note the following:

- The returned value starts with a letter that represents the first letter in the string followed by 3 digits (e.g. `s400`,
  `c130`).

  For more information about how the return value is calculated, see the [Soundex phonetic algorithm](https://en.wikipedia.org/wiki/Soundex) (in Wikipedia).
- As mentioned earlier, if you want to use the variant that retains the Soundex code number for the second letter when the first
  and second letters use the same number, call the [SOUNDEX\_P123](/sql-reference/functions/soundex_p123) function instead.

## Usage notes

- Because the function returns only four characters (one letter and three digits), the output is primarily determined by the
  first few syllables of the input, rather than the entire string.

  For example, the following statement compares three strings and returns the same SOUNDEX value for each string because, even
  though they have completely different spellings and meanings, they start with phonetically similar syllables:

  Copy code

  ```
  SELECT SOUNDEX('I love rock and roll music.'),
      SOUNDEX('I love rocks and gemstones.'),
      SOUNDEX('I leave a rock wherever I go.');
  +----------------------------------------+--------------------------+------------------------------------------+
  | SOUNDEX('I LOVE ROCK AND ROLL MUSIC.') | SOUNDEX('I LOVE ROCKS.') | SOUNDEX('I LEAVE A ROCK WHEREVER I GO.') |
  |----------------------------------------+--------------------------+------------------------------------------|
  | I416                                   | I416                     | I416                                     |
  +----------------------------------------+--------------------------+------------------------------------------+
  ```

## Examples

The following query returns SOUNDEX values for two names that are spelled differently, but are typically pronounced similarly:

> Copy code
>
> ```
> SELECT SOUNDEX('Marks'), SOUNDEX('Marx');
> +------------------+-----------------+
> | SOUNDEX('MARKS') | SOUNDEX('MARX') |
> |------------------+-----------------|
> | M620             | M620            |
> +------------------+-----------------+
> ```

The following query demonstrates how to use SOUNDEX to find potentially related rows in different tables:

> Create and load the tables:
>
> Copy code
>
> ```
> CREATE TABLE sounding_board (v VARCHAR);
> CREATE TABLE sounding_bored (v VARCHAR);
> INSERT INTO sounding_board (v) VALUES ('Marsha');
> INSERT INTO sounding_bored (v) VALUES ('Marcia');
> ```
>
> Look for related records without SOUNDEX:
>
> Copy code
>
> ```
> SELECT * 
>     FROM sounding_board AS board, sounding_bored AS bored 
>     WHERE bored.v = board.v;
> +---+---+
> | V | V |
> |---+---|
> +---+---+
> ```
>
> Look for related records using SOUNDEX:
>
> Copy code
>
> ```
> SELECT * 
>     FROM sounding_board AS board, sounding_bored AS bored 
>     WHERE SOUNDEX(bored.v) = SOUNDEX(board.v);
> +--------+--------+
> | V      | V      |
> |--------+--------|
> | Marsha | Marcia |
> +--------+--------+
> ```
