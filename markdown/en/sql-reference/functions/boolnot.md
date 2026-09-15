Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# BOOLNOT

Computes the Boolean NOT of a single numeric expression. In accordance with Boolean semantics:

- Non-zero values, including negative numbers, are regarded as true.
- Zero values are regarded as false.

As a result, the function returns:

- `True` if the expression is zero.
- `False` if the expression is non-zero.
- `NULL` if the expression is NULL.

See also:
:   [BOOLAND](/sql-reference/functions/booland) , [BOOLOR](/sql-reference/functions/boolor) , [BOOLXOR](/sql-reference/functions/boolxor)

## Syntax

Copy code

```
BOOLNOT( <expr> )
```

## Arguments

`expr`
:   A numeric expression.

## Returns

This function returns a value of type BOOLEAN or NULL.

## Usage Notes

This function rounds [floating-point numbers](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers).
Therefore, it might return unexpected results for floating-point numbers that round to zero.

For examples of this behavior and workarounds, see [Compute Boolean NOT results for floating-point numbers](#label-boolnot-floating-point-examples).

## Examples

The following examples use the BOOLNOT function.

### Compute Boolean NOT results for integers and NULL values

The following query computes Boolean NOT results for integers and NULL values:

Copy code

```
SELECT BOOLNOT(0),
       BOOLNOT(10),
       BOOLNOT(NULL);
```

```
+------------+-------------+---------------+
| BOOLNOT(0) | BOOLNOT(10) | BOOLNOT(NULL) |
|------------+-------------+---------------|
| True       | False       | NULL          |
+------------+-------------+---------------+
```

### Compute Boolean NOT results for floating-point numbers

The following examples demonstrate how the function might return unexpected results for floating-point
numbers that round to zero.

For the following queries, a result of `False` might be expected for the following function calls, but they return
`True` because the function rounds non-zero floating-point values to zero:

Copy code

```
SELECT BOOLNOT(0.3);
```

```
+--------------+
| BOOLNOT(0.3) |
|--------------|
| True         |
+--------------+
```

Copy code

```
SELECT BOOLNOT(-0.4);
```

```
+---------------+
| BOOLNOT(-0.4) |
|---------------|
| True          |
+---------------+
```

If required, you can work around this rounding behavior for positive floating-point values by using the
[CEIL](/sql-reference/functions/ceil) function. For example, the following query returns `False`:

Copy code

```
SELECT BOOLNOT(CEIL(0.3));
```

```
+--------------------+
| BOOLNOT(CEIL(0.3)) |
|--------------------|
| False              |
+--------------------+
```

For negative floating-point values, you can work around this rounding behavior by using the
:[NOT logical operator](/sql-reference/operators-logical) instead of the function. For example,
the following query returns `False`:

Copy code

```
SELECT NOT -0.4;
```

```
+----------+
| NOT -0.4 |
|----------|
| False    |
+----------+
```
