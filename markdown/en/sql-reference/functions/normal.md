Categories:
:   [Data generation functions](/sql-reference/functions-data-generation)

# NORMAL

Generates a normally-distributed pseudo-random floating point number with specified
`mean` and `stddev` (standard deviation).

## Syntax

Copy code

```
NORMAL( <mean> , <stddev> , <gen> )
```

## Arguments

`mean`
:   A constant specifying the value that the output values should be centered on.

`stddev`
:   A constant specifying the width of one standard deviation.

    For example, if you specify a mean of 0.0 and a standard deviation of 1.0,
    approximately 68.2% of returned values from multiple calls will be between
    -1.0 and +1.0 (i.e. within one standard deviation of the mean).

    Similarly, if you choose a mean of 5.0 and a standard deviation of 2, then
    approximately 68.2% of values will be between 3.0 and 7.0.

`gen`
:   An expression that serves as a raw source of uniform random numbers,
    typically the `RANDOM` function. For more information, see the Data
    Generation Functions [Usage notes](/sql-reference/functions-data-generation#label-rand-dist-functions).

## Returns

Returns a random floating-point number. The accumulated results of a large
number of repeated calls approximate a normal distribution.

## Usage notes

This function is related to, but different from, the
[RANDOM](/sql-reference/functions/random) function, both in the ranges
of the values returned and their distribution.

- `RANDOM` generates random 64-bit integers in a uniform distribution.
  It accepts an optional seed that allows random sequences to be repeated.

  When `RANDOM` is called a large number of times, the results are more or less
  evenly distributed over the range of possible values. For example, the number of
  results with values between 1000 and 2000 is similar to the number of
  values between 2000 and 3000.
- `NORMAL` generates random integer or floating-point numbers centered on the
  specified mean, with the specified standard deviation.

  When `NORMAL` is called a large number of times, the distribution of the
  results is likely to approximate a “normal” curve (a “bell-shaped curve”).
  The center of the curve and its “breadth” are influenced by the `mean`
  and `stddev` parameters. Values closer to the specified mean are more
  likely to occur than values far from the mean.

## Examples

This shows typical usage with a mean of 0 and a standard deviation of 1:

> Copy code
>
> ```
> SELECT normal(0, 1, random()) FROM table(generator(rowCount => 5));
>
> +------------------------+
> | NORMAL(0, 1, RANDOM()) |
> |------------------------|
> |           0.227384164  |
> |           0.9945290748 |
> |          -0.2045078571 |
> |          -1.594607893  |
> |          -0.8213296842 |
> +------------------------+
> ```

This shows that if the `gen` parameter is a constant, then the
output is a constant:

> Copy code
>
> ```
> SELECT normal(0, 1, 1234) FROM table(generator(rowCount => 5));
>
> +--------------------+
> | NORMAL(0, 1, 1234) |
> |--------------------|
> |      -0.6604156716 |
> |      -0.6604156716 |
> |      -0.6604156716 |
> |      -0.6604156716 |
> |      -0.6604156716 |
> +--------------------+
> ```
