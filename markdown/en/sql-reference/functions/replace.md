Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# REPLACE

Removes all occurrences of a specified substring, and optionally replaces them with another substring.

## Syntax

Copy code

```
REPLACE( <subject> , <pattern> [ , <replacement> ] )
```

## Arguments

`subject`
:   The subject is the string in which to do the replacements. Typically,
    this is a column, but it can be a literal.

`pattern`
:   This is the substring that you want to replace. Typically, this is a literal,
    but it can be a column or expression. Note that this is not a “regular
    expression”; if you want to use regular expressions to search for a
    pattern, use the [REGEXP\_REPLACE](/sql-reference/functions/regexp_replace) function.

`replacement`
:   This is the value used as a replacement for the `pattern`. If this
    is omitted, or is an empty string, then the `REPLACE` function simply
    deletes all occurrences of the `pattern`.

## Returns

The returned value is the string after all replacements have been done.

## Usage notes

- If `replacement` is not specified, `subject` is returned with all occurrences of `pattern` removed.
- If `replacement` is specified, `subject` is returned with all occurrences of `pattern` replaced by `replacement`.
- If any of the arguments is a NULL, the result is also a NULL.

Note

Only occurrences in the original `subject` are considered. A `pattern` that occurs in the result is not removed/replaced.

## Collation details

The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.

This function does not support the following collation specifications:

- `pi` (punctuation-insensitive).
- `cs-ai` (case-sensitive, accent-insensitive).

## Examples

Replace the string `down` with the string `up`:

> Copy code
>
> ```
> SELECT REPLACE('down', 'down', 'up');
> ```
>
> ```
> +-------------------------------+
> | REPLACE('DOWN', 'DOWN', 'UP') |
> |-------------------------------|
> | up                            |
> +-------------------------------+
> ```

Replace the substring `Athens` in the string `Vacation in Athens` with the substring
`Rome`:

> Copy code
>
> ```
> SELECT REPLACE('Vacation in Athens', 'Athens', 'Rome');
> ```
>
> ```
> +-------------------------------------------------+
> | REPLACE('VACATION IN ATHENS', 'ATHENS', 'ROME') |
> |-------------------------------------------------|
> | Vacation in Rome                                |
> +-------------------------------------------------+
> ```

Replace the substring `bc` in the string `abcd` with an empty substring:

> Copy code
>
> ```
> SELECT REPLACE('abcd', 'bc');
> ```
>
> ```
> +-----------------------+
> | REPLACE('ABCD', 'BC') |
> |-----------------------|
> | ad                    |
> +-----------------------+
> ```

Replace the values in a table with new values.

> Create and populate a table:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE TABLE replace_example(
> >   subject VARCHAR(10),
> >   pattern VARCHAR(10),
> >   replacement VARCHAR(10));
> >
> > INSERT INTO replace_example VALUES
> >   ('old car', 'old car', 'new car'),
> >   ('sad face', 'sad', 'happy'),
> >   ('snowman', 'snow', 'fire');
> > ```
>
> Replace strings in a value with a specified replacement:
>
> > Copy code
> >
> > ```
> > SELECT subject,
> >        pattern,
> >        replacement,
> >        REPLACE(subject, pattern, replacement) AS new
> >   FROM replace_example
> >   ORDER BY subject;
> > ```
> >
> > ```
> > +----------+---------+-------------+------------+
> > | SUBJECT  | PATTERN | REPLACEMENT | NEW        |
> > |----------+---------+-------------+------------|
> > | old car  | old car | new car     | new car    |
> > | sad face | sad     | happy       | happy face |
> > | snowman  | snow    | fire        | fireman    |
> > +----------+---------+-------------+------------+
> > ```
>
> The output shows the following replacements:
>
> - The string `old car` was replaced by the string `new car`.
> - In the string `sad face`, the substring `sad` was replaced by the substring `happy` to create the new string
>   `happy face`.
> - In the string `snowman`, the substring `snow` was replaced by the substring `fire` to create the new string
>   `fireman`.
