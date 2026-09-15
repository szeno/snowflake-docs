Categories:
:   [Numeric functions](/sql-reference/functions-numeric)

# DIV0NULL

Performs division like the division operator (`/`), but returns 0 when the divisor is 0 or NULL (rather than reporting an
error or returning NULL).

See also:
:   [DIV0](/sql-reference/functions/div0)

## Syntax

Copy code

```
DIV0NULL( <dividend> , <divisor> )
```

## Arguments

`dividend`
:   Numeric expression that evaluates to the value that you want to divide.

`divisor`
:   Numeric expression that evaluates to the value that you want to divide by.

## Returns

The quotient. If the divisor is 0 or NULL, the function returns 0.

## Examples

As shown in the following example, the DIV0NULL function performs division like the division operator (`/`):

Copy code

```
SELECT 1/2;

+----------+
|      1/2 |
|----------|
| 0.500000 |
+----------+
```

Copy code

```
SELECT DIV0NULL(1, 2);

+----------------+
| DIV0NULL(1, 2) |
|----------------|
|       0.500000 |
+----------------+
```

Unlike the division operator, DIV0NULL returns a 0 (rather than reporting an error or returning NULL) when the divisor is 0 or
NULL.

Copy code

```
SELECT 1/0;
100051 (22012): Division by zero
```

Copy code

```
SELECT DIV0NULL(1, 0);

+----------------+
| DIV0NULL(1, 0) |
|----------------|
|       0.000000 |
+----------------+
```

Copy code

```
SELECT 1/NULL;

+--------+
| 1/NULL |
|--------|
|   NULL |
+--------+
```

Copy code

```
SELECT DIV0NULL(1, NULL);

+-------------------+
| DIV0NULL(1, NULL) |
|-------------------|
|          0.000000 |
+-------------------+
```
