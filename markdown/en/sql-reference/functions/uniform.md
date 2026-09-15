Categories:
:   [Data generation functions](/sql-reference/functions-data-generation)

# UNIFORM

Generates a uniformly-distributed pseudo-random number in the inclusive
range [`min`, `max`].

## Syntax

Copy code

```
UNIFORM( <min> , <max> , <gen> )
```

## Arguments

`min`
:   A constant specifying the minimum value (inclusive) of the generated number.

`max`
:   A constant specifying the maximum value (inclusive) of the generated number.

`gen`
:   An expression that serves as a raw source of uniform random numbers,
    typically the [RANDOM](/sql-reference/functions/random) function. For more information, see the Data
    Generation Functions [Usage notes](/sql-reference/functions-data-generation#label-rand-dist-functions).

## Returns

If either or both of `min` or `max` is a floating-point number,
UNIFORM returns a floating-point number. If both `min` and
`max` are integers, UNIFORM returns an integer.

## Usage notes

This function is related to, but different from, the [RANDOM](/sql-reference/functions/random) function. Both
functions generate uniform distributions, but there are differences in the ranges of
the values returned.

- RANDOM generates pseudo-random 64-bit integers. It accepts an optional
  seed that allows sequences to be repeated.
- UNIFORM generates random integer or floating-point numbers in the
  specified range.

## Examples

The following examples demonstrate how to use the UNIFORM function. The values displayed in the output below might differ from
the values returned when you run these examples yourself.

This example generates five random integers in the range of 1 to 10 (inclusive):

Copy code

```
SELECT UNIFORM(1, 10, RANDOM()) FROM TABLE(GENERATOR(ROWCOUNT => 5));
```

```
+--------------------------+
| UNIFORM(1, 10, RANDOM()) |
|--------------------------|
|                        6 |
|                        1 |
|                        8 |
|                        5 |
|                        6 |
+--------------------------+
```

This example generates five floating-point numbers in the range of 0 to 1 (inclusive):

Copy code

```
SELECT UNIFORM(0::FLOAT, 1::FLOAT, RANDOM()) FROM TABLE(GENERATOR(ROWCOUNT => 5));
```

```
+---------------------------------------+
| UNIFORM(0::FLOAT, 1::FLOAT, RANDOM()) |
|---------------------------------------|
|                         0.1180758313  |
|                         0.4945805484  |
|                         0.7113092833  |
|                         0.06170806767 |
|                         0.01635235156 |
+---------------------------------------+
```

This example shows that if the `gen` argument is a constant, then the output is a constant:

Copy code

```
SELECT UNIFORM(1, 10, 1234) FROM TABLE(GENERATOR(ROWCOUNT => 5));
```

```
+----------------------+
| UNIFORM(1, 10, 1234) |
|----------------------|
|                    7 |
|                    7 |
|                    7 |
|                    7 |
|                    7 |
+----------------------+
```
