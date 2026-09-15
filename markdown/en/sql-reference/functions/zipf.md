Categories:
:   [Data generation functions](/sql-reference/functions-data-generation)

# ZIPF

Returns a Zipf-distributed integer, for `N` elements and characteristic exponent `s`.

## Syntax

Copy code

```
ZIPF( <s> , <N> , <gen> )
```

## Usage notes

- The computational cost of choosing a single random number is logarithmic in the argument `N`. More importantly, the memory cost is linear for `N`. Because of this, the argument
  `N` is limited to the inclusive range `[1, 16777215]`.
- `gen` specifies the generator expression for the function. For more information, see [Usage notes](/sql-reference/functions-data-generation#label-rand-dist-functions).
- The first two arguments (`s` and `N`) must be constants.

## Examples

Copy code

```
SELECT zipf(1, 10, random()) FROM table(generator(rowCount => 10));

+-----------------------+
| ZIPF(1, 10, RANDOM()) |
|-----------------------|
|                     9 |
|                     7 |
|                     1 |
|                     8 |
|                     8 |
|                     2 |
|                     3 |
|                     8 |
|                     2 |
|                     5 |
+-----------------------+
```

Copy code

```
SELECT zipf(1, 10, 1234) FROM table(generator(rowCount => 10));

+-------------------+
| ZIPF(1, 10, 1234) |
|-------------------|
|                 4 |
|                 4 |
|                 4 |
|                 4 |
|                 4 |
|                 4 |
|                 4 |
|                 4 |
|                 4 |
|                 4 |
+-------------------+
```
