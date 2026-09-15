Categories:
:   [Data generation functions](/sql-reference/functions-data-generation)

# SEQ1 / SEQ2 / SEQ4 / SEQ8

Returns a sequence of monotonically increasing integers, with wrap-around. Wrap-around occurs after the largest representable integer of the integer width (1, 2, 4, or 8 byte).

Important

This function uses sequences to produce a unique set of increasing integers, but does not necessarily produce a gap-free sequence. When operating on a large quantity of data, gaps can
appear in a sequence. If a fully ordered, gap-free sequence is required, consider using the [ROW\_NUMBER](/sql-reference/functions/row_number) window function.

For more details about sequences in Snowflake, see [Using Sequences](/user-guide/querying-sequences).

## Syntax

Copy code

```
SEQ1( [0|1] )

SEQ2( [0|1] )

SEQ4( [0|1] )

SEQ8( [0|1] )
```

## Usage notes

- If the optional sign argument is 0, the sequence continues at 0 after wrap-around. If the optional sign argument is 1, the sequence continues at the smallest representable number based
  on the given integer width.
- The default sign argument is 0.

## Examples

These are basic examples of using sequences:

> Copy code
>
> ```
> SELECT seq8() FROM table(generator(rowCount => 5));
>
> +--------+
> | SEQ8() |
> |--------|
> |      0 |
> |      1 |
> |      2 |
> |      3 |
> |      4 |
> +--------+
> ```
>
> Copy code
>
> ```
> SELECT * FROM (SELECT seq2(0), seq1(1) FROM table(generator(rowCount => 132))) ORDER BY seq2(0) LIMIT 7 OFFSET 125;
>
> +---------+---------+
> | SEQ2(0) | SEQ1(1) |
> |---------+---------|
> |     125 |     125 |
> |     126 |     126 |
> |     127 |     127 |
> |     128 |    -128 |
> |     129 |    -127 |
> |     130 |    -126 |
> |     131 |    -125 |
> +---------+---------+
> ```

This example shows how to use ROW\_NUMBER to generate a sequence without gaps:

> Copy code
>
> ```
> SELECT ROW_NUMBER() OVER (ORDER BY seq4())
>     FROM TABLE(generator(rowcount => 10));
> +-------------------------------------+
> | ROW_NUMBER() OVER (ORDER BY SEQ4()) |
> |-------------------------------------|
> |                                   1 |
> |                                   2 |
> |                                   3 |
> |                                   4 |
> |                                   5 |
> |                                   6 |
> |                                   7 |
> |                                   8 |
> |                                   9 |
> |                                  10 |
> +-------------------------------------+
> ```
