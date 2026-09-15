Categories:
:   [Numeric functions](/sql-reference/functions-numeric)

# DIV0

Performs division like the division operator (`/`), but returns 0 when the divisor is 0 (rather than reporting an error).

See also:
:   [DIV0NULL](/sql-reference/functions/div0null)

## Syntax

Copy code

```
DIV0( <dividend> , <divisor> )
```

## Arguments

`dividend`
:   Numeric expression that evaluates to the value that you want to divide.

`divisor`
:   Numeric expression that evaluates to the value that you want to divide by.

## Returns

The quotient. If the divisor is 0, the function returns 0.

## Examples

As shown in the following example, the DIV0 function performs division like the division operator (`/`):

> Copy code
>
> ```
> SELECT 1/2;
> +----------+                                                                    
> |      1/2 |
> |----------|
> | 0.500000 |
> +----------+
> SELECT DIV0(1, 2);
> +------------+                                                                  
> | DIV0(1, 2) |
> |------------|
> |   0.500000 |
> +------------+
> ```

Unlike the division operator, DIV0 returns a 0 (rather than reporting an error) when the divisor is 0.

> Copy code
>
> ```
> select 1/0;
> 100051 (22012): Division by zero
> ```
>
> Copy code
>
> ```
> SELECT DIV0(1, 0);
> +------------+                                                                  
> | DIV0(1, 0) |
> |------------|
> |   0.000000 |
> +------------+
> ```
