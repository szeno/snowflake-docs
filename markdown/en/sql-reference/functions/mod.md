Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Rounding and Truncation)

# MOD

Returns the remainder of input `expr1` divided by input `expr2`.

Equivalent to the modulo [arithmetic operator](/sql-reference/operators-arithmetic) (for example, `expr1 % expr2`).

## Syntax

Copy code

```
MOD( <expr1> , <expr2> )
```

## Arguments

`expr1`
:   A numeric expression.

`expr2`
:   A numeric expression.

## Returns

Returns either an integer or a fixed-point decimal number.

## Usage notes

- Both `expr1` and `expr2` must be numeric expressions.
  They aren’t required to be integers.
- The returned value is the remainder from truncation-based division (rounding toward zero), not floor-based
  division (rounding down). Therefore, if `expr1` is negative, the returned value is negative. This
  behavior is different from some programming languages (such as Python), but consistent with standard SQL. For
  more information, see the [Modulo Wikipedia page](https://en.wikipedia.org/wiki/Modulo).

## Examples

The following example shows usage of the `MOD()` function on both integer
and non-integer values:

> Copy code
>
> ```
> SELECT MOD(3, 2) AS mod1, MOD(4.5, 1.2) AS mod2;
> ```
>
> Output:
>
> Copy code
>
> ```
> +------+------+
> | MOD1 | MOD2 |
> +------+------+
> |    1 |  0.9 |
> +------+------+
> ```

The following steps show how each result is calculated. Because `MOD()` uses truncation-based division
(rounding the quotient toward zero), the remainder is `expr1 - (TRUNC(expr1 / expr2) * expr2)`:

- `MOD(3, 2)`: `3 / 2` is `1.5`, which truncates to `1`. The remainder is `3 - (1 * 2) = 1`.
- `MOD(4.5, 1.2)`: `4.5 / 1.2` is `3.75`, which truncates to `3`. The remainder is `4.5 - (3 * 1.2) = 4.5 - 3.6 = 0.9`.

Because `MOD()` uses truncation-based division, a negative `expr1` produces a negative
remainder:

> Copy code
>
> ```
> SELECT MOD(-3, 2) AS neg_mod;
> ```
>
> Output:
>
> Copy code
>
> ```
> +---------+
> | NEG_MOD |
> +---------+
> |      -1 |
> +---------+
> ```

`MOD(-3, 2)`: `-3 / 2` is `-1.5`, which truncates to `-1`. The remainder is `-3 - (-1 * 2) = -3 + 2 = -1`.
