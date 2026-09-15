Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# BOOLXOR

Computes the Boolean XOR of two numeric expressions; that is, one of the expressions, but not both expressions,
is true. In accordance with Boolean semantics:

- Non-zero values, including negative numbers, are regarded as true.
- Zero values are regarded as false.

As a result, the function returns:

- `True` if one expression is non-zero and the other expression is zero.
- `False` if both expressions are non-zero or both expressions are zero.
- `NULL` if one or both expressions are NULL.

See also:
:   [BOOLAND](/sql-reference/functions/booland) , [BOOLNOT](/sql-reference/functions/boolnot) , [BOOLOR](/sql-reference/functions/boolor)

## Syntax

Copy code

```
BOOLXOR( <expr1> , <expr2> )
```

# Arguments

`expr1`
:   A numeric expression.

`expr2`
:   A numeric expression.

## Returns

This function returns a value of type BOOLEAN or NULL.

## Usage notes

This function rounds [floating-point numbers](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers).
Therefore, it might return unexpected results when it rounds non-zero floating-point numbers
to zero.

For examples of this behavior and workarounds, see [Compute Boolean XOR results for floating-point numbers](#label-boolxor-floating-point-examples).

## Examples

The following examples use the BOOLXOR function.

### Compute Boolean XOR results for integers and NULL values

The following query computes Boolean XOR results for integers and NULL values:

Copy code

```
SELECT BOOLXOR(2, 0),
       BOOLXOR(1, -1),
       BOOLXOR(0, 0),
       BOOLXOR(NULL, 3),
       BOOLXOR(NULL, 0),
       BOOLXOR(NULL, NULL);
```

```
+---------------+----------------+---------------+------------------+------------------+---------------------+
| BOOLXOR(2, 0) | BOOLXOR(1, -1) | BOOLXOR(0, 0) | BOOLXOR(NULL, 3) | BOOLXOR(NULL, 0) | BOOLXOR(NULL, NULL) |
|---------------+----------------+---------------+------------------+------------------+---------------------|
| True          | False          | False         | NULL             | NULL             | NULL                |
+---------------+----------------+---------------+------------------+------------------+---------------------+
```

### Compute Boolean XOR results for floating-point numbers

The following examples demonstrate how the function might return unexpected results for floating-point
numbers that round to zero.

For the following queries, a result of `False` might be expected for the following function calls, but they return
`True` because the function rounds non-zero floating-point values to zero:

Copy code

```
SELECT BOOLXOR(2, 0.3);
```

```
+-----------------+
| BOOLXOR(2, 0.3) |
|-----------------|
| True            |
+-----------------+
```

Copy code

```
SELECT BOOLXOR(-0.4, 5);
```

```
+------------------+
| BOOLXOR(-0.4, 5) |
|------------------|
| True             |
+------------------+
```

Similarly, a result of `True` might be expected for the following function calls, but they return
`False`:

Copy code

```
SELECT BOOLXOR(0, 0.3);
```

```
+-----------------+
| BOOLXOR(0, 0.3) |
|-----------------|
| False           |
+-----------------+
```

Copy code

```
SELECT BOOLXOR(-0.4, 0);
```

```
+------------------+
| BOOLXOR(-0.4, 0) |
|------------------|
| False            |
+------------------+
```

If required, you can work around this rounding behavior for positive floating-point values by using the
[CEIL](/sql-reference/functions/ceil) function. For example, the following query returns `False`:

Copy code

```
SELECT BOOLXOR(2, CEIL(0.3));
```

```
+-----------------------+
| BOOLXOR(2, CEIL(0.3)) |
|-----------------------|
| False                 |
+-----------------------+
```

For negative floating-point values, you can work around this rounding behavior by using the
[FLOOR](/sql-reference/functions/floor) function. For example, the following query returns `False`:

Copy code

```
SELECT BOOLXOR(FLOOR(-0.4), 5);
```

```
+-------------------------+
| BOOLXOR(FLOOR(-0.4), 5) |
|-------------------------|
| False                   |
+-------------------------+
```
